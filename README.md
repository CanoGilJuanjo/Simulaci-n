# 🎮 Simulador de Personas

Un simulador interactivo donde personas virtuales con diferentes personalidades satisfacen necesidades básicas y interactúan entre sí.

## 📋 Características

### Necesidades de las Personas
- **Hambre**: Necesitan comer comida que aparece aleatoriamente en el mapa
- **Sed**: Necesitan beber agua de fuentes que aparecen en pequeños conjuntos
- **Soledad**: Necesitan socializar con otras personas
- **Energía**: Se reduce con la actividad y se recupera descansando

### Personalidades
Cada persona tiene una personalidad que determina su comportamiento:

| Personalidad | Hambre | Sed | Soledad | Educación |
|-------------|--------|-----|---------|-----------|
| 🟢 **Feliz** | 80% | 70% | 95% | 100% |
| 🔴 **Enfadado** | 60% | 50% | 20% | 20% |
| 🔵 **Tímido** | 85% | 90% | 30% | 100% |
| 🟡 **Sociable** | 70% | 60% | 98% | 90% |

### Comportamientos Especiales
- Las personas **enfadadas** tienden a hablar mal a otras, reduciendo sus relaciones
- Las personas **sociables** son más propensas a socializar
- Las personas **tímidas** evitan la interacción social pero son educadas
- Las personas **felices** buscan interactuar positivamente

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip o gestor de paquetes equivalente

### Pasos

1. **Clonar o descargar el proyecto**
```bash
cd Personas
```

2. **Crear entorno virtual** (opcional pero recomendado)
```bash
python -m venv venv
source venv/Scripts/activate  # En Windows
# o
source venv/bin/activate      # En Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
python main.py
```

La ventana de simulación se abrirá mostrando a las personas (círculos de colores), comida (naranja) y agua (azul).

## 🎨 Leyenda de Colores

- 🟢 **Verde**: Persona Feliz
- 🔴 **Rojo**: Persona Enfadado
- 🔵 **Azul**: Persona Tímida
- 🟡 **Amarillo**: Persona Sociable
- 🟠 **Naranja**: Comida
- 🔷 **Azul claro**: Agua

## 📁 Estructura del Proyecto

```
Personas/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
└── Clases/
    ├── __init__.py        # Paquete
    ├── Persona.py         # Clase Persona
    ├── Comida.py          # Clase Comida
    ├── Agua.py            # Clase Agua
    └── Simulador.py       # Clase Simulador
```

## 🔧 Personalización

### Agregar más personas
En `main.py`, añade más líneas:
```python
sim.agregar_persona("Nombre", "personalidad")
```

### Cambiar tamaño del mapa
En `main.py`, modifica los parámetros:
```python
sim = Simulador(ancho=1600, alto=900)
```

### Ajustar velocidad de generación
En `Simulador.py`, modifica estos rangos:
```python
self.generador_comida > random.randint(100, 300)   # Comida
self.generador_agua > random.randint(200, 500)     # Agua
```

## 📊 Clases Principales

### Persona
- Tiene necesidades (hambre, sed, soledad, energía)
- Decide acciones según personalidad
- Interactúa con otras personas
- Se mueve hacia objetivos

### Comida
- Aparece aleatoriamente en el mapa
- Es consumida por personas cuando están cerca
- Reduce el hambre

### Agua
- Aparece en pequeños conjuntos (2-4 fuentes)
- Es bebida por personas cuando están cerca
- Se agota lentamente

### Simulador
- Gestiona el bucle principal
- Actualiza estado de todos los elementos
- Renderiza la simulación con Pygame

## 🎮 Controles
- **ESC**: Salir de la simulación
- Puedes modificar `Simulador.py` para agregar más controles

## 📈 Futuras Mejoras

- [ ] Sistema de reproducción/herencia
- [ ] Almacenes de comida/agua
- [ ] Jornadas de trabajo
- [ ] Sistema económico
- [ ] Interfaz de estadísticas en vivo
- [ ] Pausa y control de velocidad
- [ ] Exportar datos a CSV

## 📝 Licencia

Este proyecto es educativo. Siéntete libre de modificarlo y mejorarlo.

## 🤝 Contribuciones

Las mejoras son bienvenidas. Puedes:
- Agregar nuevas personalidades
- Mejorar la física del movimiento
- Añadir nuevas necesidades
- Optimizar el rendimiento

---

¡Disfruta observando cómo viven tus personajes virtuales! 🎉
