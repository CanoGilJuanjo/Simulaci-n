class Casa:
    """Clase que representa una casa construida por una persona"""
    
    id_counter = 0
    
    def __init__(self, x: float, y: float, dueño):
        self.id = Casa.id_counter
        Casa.id_counter += 1
        
        self.x = x
        self.y = y
        self.dueño = dueño
        
    def __repr__(self):
        return f"Casa(id:{self.id}, dueño:{self.dueño.nombre if self.dueño else 'Nadie'})"