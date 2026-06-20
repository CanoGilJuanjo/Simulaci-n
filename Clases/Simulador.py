import pygame
import random
from Persona import Persona
from Comida import Comida
from Agua import Agua
from Cultivo import Cultivo
from Casa import Casa 

class Simulador:
    """Clase principal que maneja la simulación"""
    
    def __init__(self, ancho: int = 1200, alto: int = 800, fps: int = 60):
        pygame.init()
        
        self.ancho = ancho
        self.alto = alto
        self.fps = fps
        self.reloj = pygame.time.Clock()
        
        # Pantalla
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Simulador de Personas")
        
        # Listas de elementos
        self.personas: list[Persona] = []
        self.comida: list[Comida] = []
        self.agua: list[Agua] = []
        self.cultivos: list[Cultivo] = []
        self.casas: list[Casa] = []
        # Contador de ciclos
        self.ciclo = 0
        self.año = 0
        self.generador_comida = 0
        self.generador_agua = 0
        
        # Colores
        self.COLOR_FONDO = (20, 20, 30)
        self.COLORES_PERSONALIDAD = {
            'feliz': (0, 200, 0),
            'enfadado': (200, 0, 0),
            'tímido': (100, 100, 255),
            'sociable': (255, 200, 0)
        }
    
    def agregar_persona(self, nombre: str, personalidad: str, x: float = None, y: float = None, sexo: str = None):
        """Añade una nueva persona al simulador"""
        if x is None:
            x = random.randint(50, self.ancho - 50)
        if y is None:
            y = random.randint(50, self.alto - 50)
        
        persona = Persona(nombre, personalidad, x, y, sexo=sexo)
        self.personas.append(persona)
        return persona
    
    def actualizar(self):
        """Actualiza el estado de la simulación"""
        self.ciclo += 1
        self.año = self.ciclo / 142.85
        
        # 1. Actualizar necesidades de personas vivas
        for persona in self.personas:
            if persona.vivo:
                persona.actualizar_necesidades()
        
        # 2. Ejecutar acciones inmediatas y limpiar objetivos de descanso
        for persona in self.personas:
            if not persona.vivo:
                continue
            accion = persona.decidir_accion()
            if accion == 'comer_almacenado':
                persona.comer_almacenado() 
                persona.objetivo = None  # Se queda quieto tras comer lo guardado
            elif accion == 'descansar':
                persona.descansar()
                persona.objetivo = None

        # 3. Validar y limpiar objetivos ANTES de asignar nuevos o de moverse
        # Si un objetivo ya no es válido (ej. otra persona se comió la comida), lo reseteamos
        for persona in self.personas:
            if persona.vivo and persona.objetivo:
                if not persona.objetivo_valido():
                    persona.objetivo = None

        # 4. Asignar objetivos a personas que realmente lo necesitan y van a moverse
        for persona in self.personas:
            if not persona.vivo:
                continue
            
            # CORRECCIÓN: Solo asignamos objetivo si la acción requiere desplazarse
            if persona.debe_buscar_objetivo():
                # Si no tiene objetivo, o si era comida/agua y ya llegó muy cerca, busca uno nuevo
                if not persona.objetivo or (isinstance(persona.objetivo, (Comida, Agua)) and 
                   persona.distancia_a(persona.objetivo.x, persona.objetivo.y) < 5):
                    self._asignar_objetivo(persona)
            else:
                # Si la acción es descansar o comer almacenado, se asegura de limpiar el objetivo
                persona.objetivo = None
        
        # 5. Mover personas hacia sus objetivos (solo si mantienen un objetivo válido)
        for persona in self.personas:
            if persona.vivo and persona.objetivo:
                self._mover_hacia_objetivo(persona)
        
        # Generar comida aleatoriamente
        if len(self.cultivos) == 0:
            self.generador_comida += 1.5
            if self.generador_comida >= 100:
                nueva_comida = Comida.generar_aleatorio(self.ancho, self.alto)
                self.comida.append(nueva_comida)
                self.generador_comida = 0
        else:
            self.generador_comida += 0.5
            if self.generador_comida >= 100:
                nueva_comida = Comida.generar_aleatorio(self.ancho, self.alto)
                self.comida.append(nueva_comida)
                self.generador_comida = 0

        # Generar agua en conjuntos
        self.generador_agua += 1
        if self.generador_agua >= 100:
            conjunto_agua = Agua.generar_conjunto(self.ancho, self.alto)
            self.agua.extend(conjunto_agua)
            self.generador_agua = 0
        
        # Interacciones: personas comen comida cercana
        for persona in self.personas:
            if not persona.vivo:
                continue
            for comida in self.comida[:]:
                if comida.es_consumida_por(persona):
                    self.comida.remove(comida)
                    persona.objetivo = None
        
        # Interacciones: personas socializan
        self._procesar_socializacion()
        
        # Interacciones: búsqueda de pareja
        self._procesar_busqueda_pareja()
        
        # Reproducción
        self._procesar_reproduccion()

        # Interacciones: personas beben o recogen agua
        for persona in self.personas:
            if not persona.vivo: continue
            
            for fuente in self.agua[:]:
                if persona.distancia_a(fuente.x, fuente.y) < 15:
                    accion = persona.decidir_accion()
                    
                    # 1. Si viene a recoger agua para su huerto
                    if accion == 'buscar_agua_cultivo':
                        persona.agua_inventario = 3  # Coge 3 de agua de golpe para no hacer tantos viajes
                        fuente.cantidad -= 10
                        persona.objetivo = None
                        
                        if fuente.cantidad <= 0:
                            fuente.agotada = True
                            if fuente in self.agua:
                                self.agua.remove(fuente)
                    
                    # 2. Si viene a beber porque tiene sed
                    else:
                        if fuente.es_bebida_por(persona):
                            if fuente.agotada and fuente in self.agua:
                                self.agua.remove(fuente)
                            persona.objetivo = None
        # Interacciones: Regar cultivos
        for persona in self.personas:
            if not persona.vivo: continue
            
            # Si tiene agua guardada, busca si está cerca de su cultivo para regarlo
            if persona.agua_inventario > 0:
                for cultivo in persona.cultivos:
                    if persona.distancia_a(cultivo.x, cultivo.y) < 15 and cultivo.agua_almacenada < 3:
                        cultivo.agua_almacenada += persona.agua_inventario
                        persona.agua_inventario = 0
                        persona.objetivo = None
                        break
        
        # Limpiar comida y agua consumidas
        self.comida = [c for c in self.comida if not c.consumida]
        self.agua = [a for a in self.agua if not a.agotada]
        self.cultivos = [c for c in self.cultivos if c.dueño is not None]

        # --- PROCESAR CULTIVOS Y AGRICULTURA ---
        for persona in self.personas:
            if not persona.vivo: continue
            accion = persona.decidir_accion()
            
            # Plantar cultivo
            if accion == 'crear_cultivo':
                if len(persona.cultivos) < 2:
                    nuevo_cultivo = Cultivo(persona.x, persona.y, persona)
                    persona.cultivos.append(nuevo_cultivo)
                    self.cultivos.append(nuevo_cultivo)
                    persona.comida_almacenada -= 1
                    persona.objetivo = None
                    print(f"🌱 {persona.nombre} ha creado un cultivo. (Total: {len(persona.cultivos)})")
            else:
                persona.objetivo = None # Cancela si por algún motivo ya tiene 2
            
            # 🏠 Construir casa
            if accion == 'crear_casa':
                nueva_casa = Casa(persona.x, persona.y, persona)
                persona.casa = nueva_casa
                self.casas.append(nueva_casa)
                persona.comida_almacenada -= 1  # Gasta una unidad de comida como recurso
                persona.objetivo = None
                print(f"🏠 {persona.nombre} ha construido una hermosa casa.")

        # Los cultivos crecen y tiran comida
        for cultivo in self.cultivos:
            comida_nueva = cultivo.procesar()
            if comida_nueva:
                self.comida.extend(comida_nueva)
        
        # Eliminar personas muertas y procesar HERENCIA
        for p in self.personas:
            if not p.vivo:
                print(f"💀 {p.nombre} ha muerto a los {p.edad:.2f} años en el año: {self.año:.2f}")
                
                # Sistema de Herencia
                heredero = None
                if p.pareja and p.pareja.vivo:
                    heredero = p.pareja
                else:
                    hijos_vivos = [h for h in p.hijos if h.vivo]
                    if hijos_vivos:
                        heredero = random.choice(hijos_vivos)
                
                for cultivo in p.cultivos:
                    if heredero:
                        cultivo.dueño = heredero
                        heredero.cultivos.append(cultivo)
                    else:
                        cultivo.dueño = None # El cultivo queda abandonado si no hay herederos
                
                # Sistema de Herencia de Cultivos
                for cultivo in p.cultivos:
                    if heredero and len(heredero.cultivos) < 2:
                        cultivo.dueño = heredero
                        heredero.cultivos.append(cultivo)
                        print(f"🌱 El cultivo de {p.nombre} ha sido heredado por {heredero.nombre}.")
                    else:
                        cultivo.dueño = None # El cultivo queda abandonado si el heredero ya tiene 2 o no hay heredero
                        print(f"🍂 Un cultivo de {p.nombre} ha quedado abandonado por exceso de límite o falta de herederos.")
                
                # 🏠 Sistema de Herencia para Casas
                if p.casa:
                    if heredero and not heredero.casa:
                        p.casa.dueño = heredero
                        heredero.casa = p.casa
                        print(f"🏠 La casa de {p.nombre} ha sido heredada por {heredero.nombre}.")
                    else:
                        p.casa.dueño = None
                        if p.casa in self.casas:
                            self.casas.remove(p.casa) # Se limpia si no hay nadie sin techo que la reclame

        self.personas = [p for p in self.personas if p.vivo]
    
    def _asignar_objetivo(self, persona: Persona):
        """Asigna un nuevo objetivo a una persona según su acción decidida"""
        # Limpiar objetivo inválido si existe
        if not persona.objetivo_valido():
            persona.objetivo = None
        
        accion = persona.decidir_accion()
        
        if accion in ['comer_almacenado', 'crear_cultivo']:
            persona.objetivo = None
        elif accion == 'buscar_pareja':
            persona.objetivo = self._encontrar_pareja_potencial(persona)
        elif accion == 'buscar_comida':
            persona.objetivo = self._encontrar_comida_cercana(persona)
        elif accion in ['buscar_agua', 'buscar_agua_cultivo']:
            persona.objetivo = self._encontrar_agua_cercana(persona)
        elif accion == 'socializar':
            persona.objetivo = self._encontrar_persona_cercana(persona)
        elif accion == 'regar_cultivo':
            # Buscar el cultivo que necesita agua
            cultivos_necesitados = [c for c in persona.cultivos if c.agua_almacenada < 3]
            if cultivos_necesitados:
                persona.objetivo = cultivos_necesitados[0]
        elif accion == 'ir_a_casa':
            # 🏠 Destino: Casa propia
            persona.objetivo = persona.casa
    
    def _encontrar_comida_cercana(self, persona: Persona) -> Comida:
        """Encuentra la comida más cercana a una persona"""
        if not self.comida:
            return None
        
        comida_cercana = min(self.comida, key=lambda c: persona.distancia_a(c.x, c.y))
        return comida_cercana
    
    def _encontrar_agua_cercana(self, persona: Persona) -> Agua:
        """Encuentra la fuente de agua más cercana a una persona"""
        if not self.agua:
            return None
        
        agua_cercana = min(self.agua, key=lambda a: persona.distancia_a(a.x, a.y))
        return agua_cercana
    
    def _encontrar_persona_cercana(self, persona: Persona) -> Persona:
        """Encuentra otra persona para socializar"""
        otras_personas = [p for p in self.personas if p != persona]
        
        if not otras_personas:
            return None
        
        # Preferencia según personalidad
        if persona.personalidad == 'enfadado':
            # Las personas enfadadas evitan a otros (50% de probabilidad de socializar)
            if random.random() < 0.5:
                return None
        
        # Encontrar persona más cercana que sea compatible
        persona_cercana = min(otras_personas, key=lambda p: persona.distancia_a(p.x, p.y))
        return persona_cercana
    
    def _mover_hacia_objetivo(self, persona: Persona):
        """Mueve una persona hacia su objetivo"""
        if not persona.objetivo:
            return
        
        # Determinar coordenadas del objetivo
        objetivo_x, objetivo_y = persona.objetivo.x, persona.objetivo.y
        
        # Calcular dirección
        dx = objetivo_x - persona.x
        dy = objetivo_y - persona.y
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        
        if distancia > 1:
            # Normalizar y aplicar velocidad
            dx = (dx / distancia) * persona.velocidad
            dy = (dy / distancia) * persona.velocidad
            
            persona.x += dx
            persona.y += dy
            
            # Mantener dentro del mapa
            persona.x = max(0, min(persona.x, self.ancho))
            persona.y = max(0, min(persona.y, self.alto))
    
    def _procesar_socializacion(self):
        """Procesa la interacción social entre personas cercanas"""
        RANGO_INTERACCION = 30
        
        for i, persona1 in enumerate(self.personas):
            for persona2 in self.personas[i+1:]:
                if not persona1.vivo or not persona2.vivo:
                    continue
                distancia = persona1.distancia_a(persona2.x, persona2.y)
                
                # Si están lo bastante cerca, pueden socializar
                if distancia < RANGO_INTERACCION:
                    # Solo si ambas quieren socializar
                    if persona1.decidir_accion() == 'socializar' and persona2.decidir_accion() == 'socializar':
                        persona1.hablar_con(persona2)
                        persona1.objetivo = None
                        persona2.objetivo = None
    
    def _encontrar_pareja_potencial(self, persona: Persona) -> Persona:
        """Encuentra una potencial pareja para una persona"""
        parejas_potenciales = [
            p for p in self.personas 
            if p != persona and p.vivo and p.puede_reproducirse and not p.pareja and p.sexo != persona.sexo
        ]
        
        if not parejas_potenciales:
            return None
        
        # Preferencia por relaciones positivas
        parejas_potenciales.sort(
            key=lambda p: (persona.relaciones.get(p, 0), -persona.distancia_a(p.x, p.y)),
            reverse=True
        )
        
        # Retornar la mejor opción (mejor relación y más cercana)
        return parejas_potenciales[0] if parejas_potenciales[0] != persona else None
    
    def _procesar_busqueda_pareja(self):
        """Procesa la búsqueda y formación de parejas"""
        RANGO_PAREJA = 50
        
        for i, persona1 in enumerate(self.personas):
            if not persona1.vivo or persona1.pareja or not persona1.puede_reproducirse:
                continue
            
            for persona2 in self.personas[i+1:]:
                if not persona2.vivo or persona2.pareja or not persona2.puede_reproducirse:
                    continue
                
                distancia = persona1.distancia_a(persona2.x, persona2.y)
                
                # Si están lo bastante cerca y la acción es buscar pareja
                if distancia < RANGO_PAREJA:
                    if persona1.decidir_accion() == 'buscar_pareja' and persona2.decidir_accion() == 'buscar_pareja':
                        # Intenta formar pareja
                        if persona1.formar_pareja_con(persona2):
                            print(f"💕 {persona1.nombre} y {persona2.nombre} formaron pareja")
                            persona1.objetivo = None
                            persona2.objetivo = None
    
    def _procesar_reproduccion(self):
        """Procesa la reproducción de parejas"""
        RANGO_REPRODUCCION = 20
        
        for persona in self.personas[:]:  # Copia la lista para evitar modificaciones durante iteración
            if not persona.vivo or not persona.pareja:
                continue
            
            pareja = persona.pareja
            if not pareja.vivo:
                persona.disolver_pareja()
                continue
            
            # Calcular distancia con la pareja
            distancia = persona.distancia_a(pareja.x, pareja.y)
            
            # Si están juntos y pueden tener hijos
            if distancia < RANGO_REPRODUCCION and persona.puede_tener_hijos() and pareja.puede_tener_hijos():
                # Probabilidad de reproducción (1 en 500 ciclos aproximadamente)
                if random.random() < 0.01:
                    # Solo el que tiene "sexo femenino" da a luz
                    if hasattr(persona, 'sexo') and persona.sexo == 'femenino':
                        hijo = persona.reproducirse_con(pareja)
                        self.personas.append(hijo)
                        print(f"👶 {hijo.nombre} nació de {persona.nombre} y {pareja.nombre}")
                    elif hasattr(pareja, 'sexo') and pareja.sexo == 'femenino':
                        hijo = pareja.reproducirse_con(persona)
                        self.personas.append(hijo)
                        print(f"👶 {hijo.nombre} nació de {pareja.nombre} y {persona.nombre}")
    
    def dibujar(self):
        """Dibuja la simulación en pantalla"""
        self.pantalla.fill(self.COLOR_FONDO)
        
        # Dibujar agua
        for fuente in self.agua:
            pygame.draw.circle(self.pantalla, (0, 100, 255), (int(fuente.x), int(fuente.y)), 8)
            pygame.draw.circle(self.pantalla, (0, 150, 255), (int(fuente.x), int(fuente.y)), 8, 2)
        
        # Dibujar comida
        for comida in self.comida:
            pygame.draw.circle(self.pantalla, (255, 165, 0), (int(comida.x), int(comida.y)), 6)
            pygame.draw.circle(self.pantalla, (255, 200, 0), (int(comida.x), int(comida.y)), 6, 1)
        # Dibujar cultivos (antes de dibujar personas)
        for cultivo in self.cultivos:
            color_cultivo = (139, 69, 19) # Marrón tierra
            pygame.draw.rect(self.pantalla, color_cultivo, (int(cultivo.x) - 10, int(cultivo.y) - 10, 20, 20))
            # Indicador visual si tiene agua
            if cultivo.agua_almacenada > 0:
                pygame.draw.circle(self.pantalla, (0, 200, 255), (int(cultivo.x), int(cultivo.y)), 4)

        # 🏠 Dibujar Casas (antes de dibujar personas)
        for casa in self.casas:
            color_casa = (130, 130, 130)
            if casa.dueño:
                color_casa = self.COLORES_PERSONALIDAD.get(casa.dueño.personalidad, (130, 130, 130))
            
            # Estructura cuadrada
            pygame.draw.rect(self.pantalla, color_casa, (int(casa.x) - 15, int(casa.y) - 10, 30, 22), 2)
            # Tejado triangular
            pygame.draw.polygon(self.pantalla, color_casa, [
                (int(casa.x) - 18, int(casa.y) - 10),
                (int(casa.x), int(casa.y) - 24),
                (int(casa.x) + 18, int(casa.y) - 10)
            ], 2)

        # Dibujar personas
        for persona in self.personas:
            color = self.COLORES_PERSONALIDAD.get(persona.personalidad, (255, 255, 255))
            
            # Circulo principal
            pygame.draw.circle(self.pantalla, color, (int(persona.x), int(persona.y)), 10)
            pygame.draw.circle(self.pantalla, (255, 255, 255), (int(persona.x), int(persona.y)), 10, 2)
            
            # Linea hacia el objetivo
            if persona.objetivo:
                pygame.draw.line(self.pantalla, color, 
                                (int(persona.x), int(persona.y)), 
                                (int(persona.objetivo.x), int(persona.objetivo.y)), 1)
            
            # Nombre
            fuente = pygame.font.Font(None, 18)
            texto = fuente.render(persona.nombre, True, (255, 255, 255))
            self.pantalla.blit(texto, (int(persona.x) - 15, int(persona.y) - 28))
            
            # Barras de necesidad bajo la persona
            self._dibujar_barra_necesidad(persona.x, persona.y, persona.hambre, (255, 0, 0), -3)
            self._dibujar_barra_necesidad(persona.x, persona.y, persona.sed, (0, 150, 255), -6)
        
        # Dibujar información
        self._dibujar_info()
        
        pygame.display.flip()
    
    def _dibujar_barra_necesidad(self, x: float, y: float, valor: float, color: tuple, offset: int):
        """Dibuja una barra pequeña que representa una necesidad"""
        ancho_barra = 20
        alto_barra = 2
        
        # Barra de fondo
        pygame.draw.rect(self.pantalla, (100, 100, 100), 
                        (x - ancho_barra/2, y + 15 + offset, ancho_barra, alto_barra))
        
        # Barra de valor
        valor_normalizado = max(0, min(100, valor))
        ancho_valor = (valor_normalizado / 100) * ancho_barra
        pygame.draw.rect(self.pantalla, color, 
                        (x - ancho_barra/2, y + 15 + offset, ancho_valor, alto_barra))
    
    def _dibujar_info(self):
        """Dibuja información en la pantalla"""
        fuente_grande = pygame.font.Font(None, 24)
        fuente_pequena = pygame.font.Font(None, 18)
        
        # Información general
        info_textos = [
            f"Ciclo: {self.ciclo} - Años: {self.año:.2f}",
            f"Personas: {len(self.personas)} | Comida: {len(self.comida)} | Agua: {len(self.agua)}",
        ]
        
        for i, texto in enumerate(info_textos):
            superficie = fuente_grande.render(texto, True, (255, 255, 255))
            self.pantalla.blit(superficie, (10, 10 + i * 30))
        
        # Información de cada persona
        y_offset = 80
        for persona in self.personas:
            color_pers = self.COLORES_PERSONALIDAD.get(persona.personalidad, (255, 255, 255))
            
            info_persona = f"{persona.nombre} ({persona.personalidad}): H:{persona.hambre:.0f} S:{persona.sed:.0f} Sol:{persona.soledad:.0f} E:{persona.energia:.0f}"
            
            superficie = fuente_pequena.render(info_persona, True, color_pers)
            self.pantalla.blit(superficie, (10, y_offset))
            
            # Mostrar objetivo
            if persona.objetivo:
                if isinstance(persona.objetivo, Comida):
                    objetivo_texto = "Objetivo: Comida"
                elif isinstance(persona.objetivo, Agua):
                    objetivo_texto = "Objetivo: Agua"
                elif isinstance(persona.objetivo, Persona):
                    objetivo_texto = f"Objetivo: {persona.objetivo.nombre}"
                # 🏠 Mostrar en interfaz
                elif hasattr(persona.objetivo, '__class__') and persona.objetivo.__class__.__name__ == 'Casa':
                    objetivo_texto = "Objetivo: Ir a Casa"
                else:
                    objetivo_texto = "Objetivo: Desconocido"
                superficie_obj = fuente_pequena.render(objetivo_texto, True, (200, 200, 200))
                self.pantalla.blit(superficie_obj, (320, y_offset))
            
            y_offset += 25
    
    def ejecutar(self):
        """Bucle principal de la simulación"""
        ejecutando = True
        
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        # Pausar/reanudar
                        pass
            
            self.actualizar()
            self.dibujar()
            self.reloj.tick(self.fps)
        
        pygame.quit()


if __name__ == "__main__":
    
    # Crear simulador
    sim = Simulador()
    
    Persona.cargar_nombres_en_memoria()

    # Agregar personas
    sim.agregar_persona("Juan", "feliz",sexo="masculino")
    sim.agregar_persona("María", "enfadado",sexo="femenino")
    sim.agregar_persona("Pedro", "tímido",sexo="masculino")
    sim.agregar_persona("Ana", "sociable",sexo="femenino")
    sim.agregar_persona("Lourdes", "feliz",sexo="femenino")
    sim.agregar_persona("Ramon", "enfadado",sexo="masculino")
    sim.agregar_persona("Camila", "sociable",sexo="femenino")
    
    # Ejecutar
    sim.ejecutar()
