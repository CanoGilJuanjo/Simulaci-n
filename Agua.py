import random

class Agua:
    """Clase que representa fuentes de agua en el mapa"""
    
    id_counter = 0
    
    def __init__(self, x: float, y: float, cantidad: float = 50):
        self.id = Agua.id_counter
        Agua.id_counter += 1
        
        self.x = x
        self.y = y
        self.cantidad = cantidad  # Cantidad de agua disponible
        self.agotada = False
    
    @staticmethod
    def generar_conjunto(ancho: int, alto: int, cantidad_fuentes: int = None) -> list['Agua']:
        """
        Genera un pequeño conjunto de fuentes de agua cerca una de otra
        Cantidad de fuentes: 2-4 normalmente
        """
        if cantidad_fuentes is None:
            cantidad_fuentes = random.randint(2, 4)
        
        # Centro del conjunto
        centro_x = random.randint(50, ancho - 50)
        centro_y = random.randint(50, alto - 50)
        
        conjunto = []
        for _ in range(cantidad_fuentes):
            # Generar fuentes cerca del centro (radio de 30)
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            
            x = centro_x + offset_x
            y = centro_y + offset_y
            
            # Asegurar que esté dentro del mapa
            x = max(0, min(x, ancho))
            y = max(0, min(y, alto))
            
            conjunto.append(Agua(x, y, cantidad=50))
        
        return conjunto
    
    def es_bebida_por(self, persona) -> bool:
        """Verifica si una persona está lo bastante cerca para beber"""
        distancia = ((self.x - persona.x) ** 2 + (self.y - persona.y) ** 2) ** 0.5
        if distancia < 15:  # Radio de interacción
            persona.beber(self.cantidad * 0.1)  # Bebe una pequeña porción
            self.cantidad = max(0, self.cantidad - 5)
            
            if self.cantidad <= 0:
                self.agotada = True
            return True
        return False
    
    def __repr__(self):
        return f"Agua(id:{self.id}, pos:({self.x:.1f},{self.y:.1f}), cantidad:{self.cantidad})"
