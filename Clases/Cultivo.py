import random
from Comida import Comida

class Cultivo:
    """Clase que representa un cultivo plantado por una persona"""
    
    id_counter = 0
    
    def __init__(self, x: float, y: float, dueño):
        self.id = Cultivo.id_counter
        Cultivo.id_counter += 1
        
        self.x = x
        self.y = y
        self.dueño = dueño
        self.agua_almacenada = 0
        self.ciclos_crecimiento = 0
    
    def procesar(self) -> list[Comida]:
        """Procesa el agua y genera comida gradualmente. 1 de agua = 3 de comida."""
        comida_generada = []
        if self.agua_almacenada > 0:
            self.ciclos_crecimiento += 1
            # Tarda unos ciclos en crecer para simular tiempo
            if self.ciclos_crecimiento >= 100: 
                # Generar 3 unidades de comida alrededor del cultivo
                for _ in range(3):
                    offset_x = random.randint(-15, 15)
                    offset_y = random.randint(-15, 15)
                    comida_generada.append(Comida(self.x + offset_x, self.y + offset_y, cantidad=50))
                
                self.agua_almacenada -= 1
                self.ciclos_crecimiento = 0
                
        return comida_generada