import random
import os
from typing import Dict, Tuple, Optional

class Persona:
    """Clase que representa una persona en el simulador"""
    
    contador_id = 0
    personalidades = ["feliz", "enfadado", "tímido", "sociable"]
    
    @staticmethod
    def cargar_nombres_en_memoria():
        """Llama a esto UNA SOLA VEZ al principio de tu juego/simulación"""
        

    cargar_nombres_en_memoria()

    # Listas en memoria para no leer el disco constantemente
    
    
    
    def __init__(self, nombre: str, personalidad: str, x: float = 0, y: float = 0, 
                 edad: int = 12, sexo: str = None, padres: Tuple['Persona', 'Persona'] = None):
        self.id = Persona.contador_id
        Persona.contador_id += 1
        
        self.vida = 100
        self.nombre = nombre
        self.personalidad = personalidad  
        self.edad = edad  
        self.vivo = True
        self.sexo = sexo if sexo else random.choice(['masculino', 'femenino'])  
        
        # Posición en el mapa
        self.x = x
        self.y = y
        self.velocidad = 2
        
        # Necesidades (0-100)
        self.hambre = random.randint(30, 60)
        self.sed = random.randint(30, 60)
        self.soledad = random.randint(20, 50)
        
        # Estado
        self.energia = 100
        self.relaciones: Dict['Persona', int] = {}  
        self.objetivo = None  
        self.comida_almacenada = 0  
        
        # Sistema de reproducción
        self.pareja: Optional['Persona'] = None
        self.hijos: list['Persona'] = []
        self.padres = padres  
        self.dias_sin_pareja = 0
        self.puede_reproducirse = edad >= 18  

        self.nombres_masculinos = []
        self.nombres_femeninos = []

        try:
            with open("C:\\Users\\polloslokos\\Desktop\\Personas\\Documentos\\Nombres-sexo.txt", 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if '-' in linea:
                        nombre, sexo = linea.split('-')
                        if sexo.strip() == 'masculino':
                            self.nombres_masculinos.append(nombre.strip())
                        elif sexo.strip() == 'femenino':
                            self.nombres_femeninos.append(nombre.strip())
        except FileNotFoundError:
            print("Error al cargar archivo de nombres.")
        
        self.agua_inventario = 0
        self.cultivos = []
        self.casa = None
    
    def actualizar_necesidades(self):
        """Incrementa las necesidades gradualmente"""
        
        # Evalúa si la persona está físicamente sobre o muy cerca de su casa
        en_casa = self.casa is not None and self.distancia_a(self.casa.x, self.casa.y) < 15
        factor_desgaste = 0.5 if en_casa else 1.0  # Reduce a la mitad las pérdidas
        
        self.hambre = min(100, self.hambre + random.uniform(0.001, 0.005) * factor_desgaste)
        self.sed = min(100, self.sed + random.uniform(0.001, 0.005) * factor_desgaste)
        self.soledad = min(100, self.soledad + random.uniform(0.01, 0.05))
        self.energia = max(0, self.energia - random.uniform(0.001, 0.005) * factor_desgaste)
        self.edad += 0.007  

        if not self.puede_reproducirse and self.edad >= 18:
            self.puede_reproducirse = True
        
        # Actualizar estado de pareja
        if self.pareja and not self.pareja.vivo:
            self.pareja = None
            self.dias_sin_pareja = 0
        
        if self.pareja:
            self.dias_sin_pareja = 0
        else:
            self.dias_sin_pareja += 1
        
        # Muerte por vejez
        if self.edad > 80 and random.random() < 0.01:
            self.vivo = False
        #Pierde vida por hambre, sed o energía baja
        if self.hambre >= 95 or self.sed >= 95 or self.energia <= 5:
            self.vida -= 0.5
        #Si la vida es menor o igual a 0, la persona muere
        if self.vida <= 0:
            self.vivo = False

        self.actualizar_personalidad()


    def buscar_nombres(cls, sexo: str) -> str:
        """Ahora elige de la lista en memoria, ¡es mil veces más rápido!"""
        if sexo == 'masculino' and cls.nombres_masculinos:
            return random.choice(cls.nombres_masculinos)
        elif sexo == 'femenino' and cls.nombres_femeninos:
            return random.choice(cls.nombres_femeninos)
        return "NombreDesconocido"
            
    def actualizar_personalidad(self):
        """Evalúa el estado de las necesidades y redefine la personalidad"""
        if self.hambre > 80 or self.sed > 80:
            self.personalidad = "enfadado"
        elif self.soledad > 70:
            self.personalidad = "tímido"
        elif self.energia > 70 and self.energia < 90:
            self.personalidad = "sociable"
        else:
            self.personalidad = "feliz"
    
    def decidir_accion(self) -> str:
        """Decide qué hacer según personalidad, necesidades y estado"""
        if self.objetivo and not self.objetivo_valido():
            self.objetivo = None

        # 🏠 NUEVA LÓGICA: Construir casa si está estable y tiene recursos
        if not self.casa and self.comida_almacenada > 0 and self.hambre < 50 and self.sed < 50:
            if random.random() < 0.02:  # Probabilidad de decidir construir
                return 'crear_casa'
        
        # --- NUEVA LÓGICA DE AGRICULTURA ---
        # 1. Regar el cultivo si tiene agua encima
        if self.agua_inventario > 0 and self.cultivos:
            cultivos_secos = [c for c in self.cultivos if c.agua_almacenada < 3]
            if cultivos_secos:
                return 'regar_cultivo'
                
        # 2. Buscar agua para el cultivo si está seco (y no se está muriendo de sed/hambre)
        if self.cultivos and self.sed < 70 and self.hambre < 70:
            cultivos_secos = [c for c in self.cultivos if c.agua_almacenada == 0]
            if cultivos_secos and self.agua_inventario == 0:
                return 'buscar_agua_cultivo'

        # 3. Crear un cultivo si tiene comida almacenada y no tiene demasiados ya
        if self.comida_almacenada > 0 and len(self.cultivos) < 2 and self.hambre < 50:
            if random.random() < 0.02: # Probabilidad de decidir plantar
                return 'crear_cultivo'

        if self.comida_almacenada > 0 and self.hambre > 50:
            return 'comer_almacenado'
        
        if self.puede_reproducirse and not self.pareja and self.edad >= 18 and random.random() < 0.05:
            return 'buscar_pareja'
        
        
        if self.hambre > 85:
            if self.comida_almacenada == 0:
                return 'buscar_comida'
            else:
                return 'comer_almacenado'
        elif self.sed > 85:
            return 'buscar_agua'

        # 🏠 NUEVA LÓGICA: Si está cansado y tiene casa lejos, vuelve a ella
        if self.energia < 60 and self.casa and self.distancia_a(self.casa.x, self.casa.y) > 15:
            return 'ir_a_casa'

        elif self.soledad > 75:
            if self.personalidad == 'tímido' and random.random() < 0.5:
                self.objetivo = None  
                return 'socializar'
            return 'socializar'
        else:
            self.objetivo = None  
            return 'descansar'
        
    
    
    def debe_buscar_objetivo(self) -> bool:
        """Verifica si la persona debe estar buscando un objetivo"""
        accion = self.decidir_accion()
        return accion in ['buscar_comida', 'buscar_agua', 'socializar', 'buscar_agua_cultivo', 'regar_cultivo', 'ir_a_casa']
    
    def comer(self, cantidad: float = 30):
        """Reduce hambre al comer o almacenar comida"""
        if self.hambre >= 50:
            self.hambre = max(0, self.hambre - cantidad)
            self.energia = min(100, self.energia + 5)
        elif self.comida_almacenada < 1:
            self.comida_almacenada = min(1, self.comida_almacenada + 0.5)
            self.objetivo = None # Ya comió y guardó, meta completada
        else:
            self.objetivo = None
    def comer_almacenado(self):
        """Consume comida almacenada"""
        if self.comida_almacenada > 0:
            cantidad = min(30, self.comida_almacenada * 100)
            self.hambre = max(0, self.hambre - cantidad)
            self.comida_almacenada = 0
            self.energia = min(100, self.energia + 5)
            return True
        return False
    
    def beber(self, cantidad: float = 30):
        """Reduce sed al beber"""
        self.sed = max(0, self.sed - cantidad)
        self.energia = min(100, self.energia + 5) 
        self.objetivo = None
    
    def descansar(self):
        """Recupera energía (Mejorada notablemente si está en casa)"""
        en_casa = self.casa is not None and self.distancia_a(self.casa.x, self.casa.y) < 15
        recuperacion = 12 if en_casa else 5  # Recupera más de el doble de rápido
        limite_energia = 110 if en_casa else 100
        
        self.energia = min(limite_energia, self.energia + recuperacion)
        self.hambre = min(100, self.hambre + 0.1)
        self.sed = min(100, self.sed + 0.1)
    
    def hablar_con(self, otra_persona: 'Persona'):
        """Interactúa con otra persona"""
        if self.personalidad == 'enfadado' and random.random() > 0.2:
            self.relaciones[otra_persona] = self.relaciones.get(otra_persona, 0) - 10
            otra_persona.relaciones[self] = otra_persona.relaciones.get(self, 0) - 15
        else:
            self.relaciones[otra_persona] = self.relaciones.get(otra_persona, 0) + 5
            otra_persona.relaciones[self] = otra_persona.relaciones.get(self, 0) + 5
        
        self.soledad = max(0, self.soledad - 20)
        otra_persona.soledad = max(0, otra_persona.soledad - 20)
    
    def distancia_a(self, x: float, y: float) -> float:
        """Calcula distancia a un punto"""
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5    
    
    def objetivo_valido(self) -> bool:
        """Verifica si el objetivo actual sigue siendo válido"""
        if self.objetivo is None:
            return False
        if hasattr(self.objetivo, 'consumida') and self.objetivo.consumida:
            return False
        if hasattr(self.objetivo, 'agotada') and self.objetivo.agotada:
            return False
        return True    
    
    def formar_pareja_con(self, otra_persona: 'Persona') -> bool:
        """Intenta formar pareja con otra persona"""
        if not self.puede_reproducirse or not otra_persona.puede_reproducirse:
            return False
        if self.pareja or otra_persona.pareja:
            return False
        if self.sexo == otra_persona.sexo:
            return False  
        
        if self.personalidad == 'enfadado' and random.random() < 0.8:
            return False
        if otra_persona.personalidad == 'enfadado' and random.random() < 0.8:
            return False
        
        nivel_relacion = self.relaciones.get(otra_persona, 0)
        if nivel_relacion < -20:
            return False  
        
        self.pareja = otra_persona
        otra_persona.pareja = self
        
        self.relaciones[otra_persona] = min(100, max(20, nivel_relacion + 30))
        otra_persona.relaciones[self] = min(100, max(20, otra_persona.relaciones.get(self, 0) + 30))
        return True
    
    def disolver_pareja(self):
        """Disuelve la pareja si existe"""
        if self.pareja:
            antigua_pareja = self.pareja
            self.pareja = None
            antigua_pareja.pareja = None
            self.relaciones[antigua_pareja] = max(-50, self.relaciones.get(antigua_pareja, 0) - 20)
            antigua_pareja.relaciones[self] = max(-50, antigua_pareja.relaciones.get(self, 0) - 20)
    
    def puede_tener_hijos(self) -> bool:
        """Verifica si puede tener hijos"""
        if not self.pareja:
            return False
        if self.sexo == self.pareja.sexo:
            return False
        if not self.puede_reproducirse:
            return False
        if self.hambre > 80 or self.sed > 80:
            return False
        if self.energia < 50:
            return False  
        return True
    
    def reproducirse_con(self, pareja: 'Persona') -> 'Persona':
        """Crea un nuevo hijo con un nombre real acorde a su sexo"""
        if self.sexo == pareja.sexo:
            raise ValueError("Solo parejas de distinto sexo pueden reproducirse")
        
        if random.random() < 0.5:
            personalidad_hijo = self.personalidad if random.random() < 0.5 else pareja.personalidad
        else:
            personalidad_hijo = random.choice(self.personalidades)
        
        # 1. Decidimos el sexo biológico del bebé primero
        sexo_hijo = random.choice(['masculino', 'femenino'])
        
        #Usamos la funcion buscar_nombre para extraer el nombre del hijo según su sexo
        nombre_hijo = self.buscar_nombres(sexo_hijo)

        x_hijo = (self.x + pareja.x) / 2 + random.randint(-30, 30)
        y_hijo = (self.y + pareja.y) / 2 + random.randint(-30, 30)
        
        # 3. Construimos el objeto Persona pasándole el sexo correcto
        hijo = Persona(nombre_hijo, personalidad_hijo, x_hijo, y_hijo, edad=0, sexo=sexo_hijo, padres=(self, pareja))
        
        self.hijos.append(hijo)
        pareja.hijos.append(hijo)
        
        self.energia = max(0, self.energia - 30)
        pareja.energia = max(0, pareja.energia - 30)
        self.hambre = min(100, self.hambre + 20)
        pareja.hambre = min(100, pareja.hambre + 20)
        return hijo
    
    def obtener_info_pareja(self) -> str:
        if self.pareja:
            return f"Pareja: {self.pareja.nombre}"
        return "Sin pareja"
    
    def obtener_info_hijos(self) -> str:
        if not self.hijos:
            return "Sin hijos"
        hijos_vivos = [h for h in self.hijos if h.vivo]
        return f"{len(hijos_vivos)} hijo(s)"
    
    def __repr__(self):
        return f"Persona({self.nombre}, {self.personalidad}, H:{self.hambre:.1f}, S:{self.sed:.1f})"