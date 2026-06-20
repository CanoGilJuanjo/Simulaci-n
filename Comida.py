import random

class Comida:
    """Clase que representa comida en el mapa"""
    
    id_counter = 0
    
    def __init__(self, x: float, y: float, cantidad: float = 50):
        self.id = Comida.id_counter
        Comida.id_counter += 1
        
        self.x = x
        self.y = y
        self.cantidad = cantidad  # Valor nutritivo
        self.consumida = False
    
    @staticmethod
    def generar_aleatorio(ancho: int, alto: int, cantidad: float = 50) -> 'Comida':
        """Genera comida en posición aleatoria del mapa"""
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        return Comida(x, y, cantidad)
    
    def es_consumida_por(self, persona) -> bool:
        """Verifica si una persona está lo bastante cerca para comer"""
        distancia = ((self.x - persona.x) ** 2 + (self.y - persona.y) ** 2) ** 0.5
        if distancia < 15:  # Radio de interacción
            persona.comer(self.cantidad)
            self.consumida = True
            return True
        return False
    
    def __repr__(self):
        return f"Comida(id:{self.id}, pos:({self.x:.1f},{self.y:.1f}), cantidad:{self.cantidad})"
