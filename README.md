# 🎮 Simulador de Personas

Un simulador interactivo desarrollado en Python y Pygame donde personas virtuales con diferentes personalidades satisfacen necesidades básicas, interactúan entre sí, forman familias, gestionan cultivos agrícolas, construyen hogares y transmiten su legado a través de un sistema dinámico de herencia.

## 📋 Características

### Necesidades de las Personas
- **Hambre**: Incrementa de forma continua. Requiere consumir comida recolectada del mapa o del almacenamiento personal.
- **Sed**: Aumenta paulatinamente. Requiere beber agua directamente de las fuentes o recolectarla en el inventario para riego.
- **Soledad**: Aumenta si no hay interacción. Se mitiga socializando con otros individuos cercanos.
- **Energía**: Disminuye con la actividad y se recupera descansando (con un beneficio drástico si se realiza dentro del hogar).

### Sistema de Personalidades Dinámicas
La personalidad de cada individuo se redefine en tiempo real según el estado crítico de sus necesidades actuales:
- 🔴 **Enfadado**: Se activa si el hambre o la sed superan el 80%. Las personas en este estado tienden a hablar mal a otras, reduciendo el nivel de sus relaciones.
- 🔵 **Tímido**: Se activa si la soledad supera el 70%. Evitan la interacción social espontánea pero mantienen una actitud educada.
- 🟡 **Sociable**: Se activa si la energía está en un nivel óptimo (entre el 70% y el 90%) y las necesidades básicas están cubiertas. Son altamente propensas a entablar conversaciones.
- 🟢 **Feliz**: Estado por defecto cuando las necesidades generales se encuentran equilibradas. Buscan interacciones positivas.

### 🌟 Mecánicas Avanzadas Implementadas

- **Sistema de Reproducción Familiar**: Al alcanzar los 18 años, los individuos aptos buscan activamente parejas del sexo opuesto basadas en relaciones positivas. Las parejas pueden concebir hijos, determinando de forma biológica su sexo y asignando nombres legibles directamente desde un archivo en memoria (`Nombres-sexo.txt`).
- **Inventario y Almacenamiento**: Las personas ahora cuentan con variables autónomas para gestionar `comida_almacenada` y `agua_inventario` con capacidad de transporte de recursos.
- **Agricultura Automatizada (Cultivos)**: Los individuos pueden invertir comida almacenada para plantar hasta 2 cultivos. Los cultivos absorben el agua del inventario del personaje y, tras completar un ciclo de maduración de 100 y estar hidratados, generan de forma autónoma 3 unidades de comida a su alrededor.
- **Construcción y Beneficios de Casas**: Si una persona posee recursos y estabilidad, edificará una vivienda. Permanecer físicamente en el hogar reduce las pérdidas por desgaste de hambre, sed y energía a la mitad (factor de 0.5) y maximiza los efectos del descanso.
- **Sistema de Legado y Herencia**: Al ocurrir el fallecimiento de un habitante (por vejez, inanición o deshidratación), sus propiedades (cultivos y casa) son heredadas automáticamente por su pareja o por un hijo vivo seleccionado al azar, evitando el abandono ineficiente de la infraestructura.

## 🚀 Instalación

### Requisitos
- Python 3.8+
- Pygame
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

La ventana de simulación se abrirá mostrando gráficamente a las personas (círculos de colores), comida (naranja), fuentes de agua (azul), cultivos agrícolas en crecimiento y las casas edificadas.

## 🎨 Leyenda de Colores

- 🟢 **Verde**: Persona Feliz
- 🔴 **Rojo**: Persona Enfadada
- 🔵 **Azul**: Persona Tímida
- 🟡 **Amarillo**: Persona Sociable
- 🟠 **Naranja**: Comida
- 🔷 **Azul claro**: Fuentes de Agua

## 📁 Estructura del Proyecto

```
Personas/
├── main.py                          # Punto de entrada de la simulación
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo informativo
├── Documentos/
│   └── Nombres-sexo.txt             # Base de datos externa de nombres y sexos
└── Clases/
    ├── __init__.py                  # Inicializador del paquete de clases
    ├── Persona.py                   # Clase Persona (Necesidades, Reproducción, Inventario y Decisiones)
    ├── Comida.py                    # Clase Comida (Propiedades nutritivas y colisiones)
    ├── Agua.py                      # Clase Agua (Manejo de fuentes grupales y agotamiento)
    ├── Cultivo.py                   # Clase Cultivo (Mecánicas de crecimiento agrícola y producción)
    └── Casa.py                      # Clase Casa (Estructura de vivienda y mitigación de desgaste)
```

## 🔧 Personalización

### Ajustar velocidad de generación de recursos
En `Simulador.py`, puedes modificar los rangos aleatorios para alterar la tasa de aparición de recursos espontáneos en el mapa:
```python
self.generador_comida > random.randint(100, 300)   # Aparición de comida
self.generador_agua > random.randint(200, 500)     # Aparición de agua
```

## 📊 Clases Principales

### Persona
Gestiona las necesidades vitales (hambre, sed, soledad, energía, edad y vida). Cambia de personalidad dinámicamente y decide acciones complejas en base a su estado (buscar comida/agua, almacenar, socializar, buscar pareja, plantar, construir, ir a casa o descansar).

### Comida
Aparece aleatoriamente o es producida de forma eficiente mediante agricultura. Reduce el hambre al ser consumida directamente o permite acumular reservas alimenticias.

### Agua
Aparece en pequeños conjuntos geográficos (2-4 fuentes). Permite saciar la sed de los personajes inmediatamente o ser recolectada en porciones (3 unidades) para la hidratación de los huertos.

### Cultivo
Estructura agrícola vinculada a un dueño. Consume agua del inventario del personaje y genera 3 porciones de comida tras completar de forma exitosa su ciclo de maduración.

### Casa
Estructura habitacional construida individualmente por los personajes estables. Proporciona un área segura que reduce el desgaste de necesidades a la mitad y maximiza el descanso del dueño.

### Simulador
Clase principal que gestiona el bucle de simulación a través de Pygame. Controla los eventos globales, el paso del tiempo (ciclos y años virtuales), colisiones y las interacciones complejas de socialización, emparejamiento, natalidad y transferencia por herencia de bienes.

## 🎮 Controles
- **ESC** / Cerrar ventana: Salir de la simulación de forma segura.
- **ESPACIO**: Pausar o reanudar el transcurso de la simulación.

## 📈 Futuras Mejoras

- [x] Sistema de reproducción/herencia
- [x] Almacenes individuales de comida/agua (Inventario)
- [ ] Almacenes comunitarios o silos centralizados de comida/agua a gran escala.
- [ ] Introducción de jornadas laborales estructuradas y asignación de roles/profesiones.
- [ ] Interfaz gráfica detallada con estadísticas y gráficos demográficos en vivo.
- [ ] Controles por teclado para regular la velocidad de simulación en tiempo real.
- [ ] Exportar automáticamente métricas demográficas e históricas a un archivo CSV.

## 📝 Licencia

Este proyecto es de carácter estrictamente educativo.