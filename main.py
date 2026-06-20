"""
Simulador de Personas - Punto de entrada principal
"""

import sys
from pathlib import Path

# Agregar la carpeta Clases al path
clases_path = Path(__file__).parent / "Clases"
sys.path.insert(0, str(clases_path))

from Clases.Persona import Persona
from Simulador import Simulador

def main():
    """Función principal"""
    print("🎮 Iniciando Simulador de Personas...")
    print("=" * 50)

       

    # 2. Creamos y ejecutamos el simulador
    sim = Simulador()
    
    # Agregar personas con diferentes personalidades
    print("\n👥 Personajes creados:")
    sim.agregar_persona("Juan", "feliz",sexo="masculino")
    print("  ✓ Juan (Feliz)")
    sim.agregar_persona("María", "enfadado",sexo="femenino")
    print("  ✓ María (Enfadado)")
    sim.agregar_persona("Pedro", "tímido",sexo="masculino")
    print("  ✓ Pedro (Tímido)")
    sim.agregar_persona("Ana", "sociable",sexo="femenino")
    print("  ✓ Ana (Sociable)")
    sim.agregar_persona("Lourdes", "feliz",sexo="femenino")
    print("  ✓ Lourdes (Feliz)")
    sim.agregar_persona("Ramon", "enfadado",sexo="masculino")
    print("  ✓ Ramon (Enfadado)")
    sim.agregar_persona("Camila", "sociable",sexo="femenino")
    print("  ✓ Camila (Sociable)")
    sim.agregar_persona("Rosa", "sociable",sexo="femenino")
    print("  ✓ Rosa (Sociable)")
    sim.agregar_persona("Mirella", "sociable",sexo="femenino")
    print("  ✓ Mirella (Sociable)")
    sim.agregar_persona("Jorge", "sociable",sexo="masculino")
    print("  ✓ Jorge (Sociable)")
    sim.agregar_persona("Carolina", "sociable",sexo="femenino")
    print("  ✓ Carolina (Sociable)")
    sim.agregar_persona("Raul", "sociable",sexo="masculino")
    print("  ✓ Raul (Sociable)")
    sim.agregar_persona("Pedro", "sociable",sexo="masculino")
    print("  ✓ Pedro (Sociable)")
    sim.agregar_persona("Lucas", "sociable",sexo="masculino")
    print("  ✓ Lucas (Sociable)")
    
    print("\n" + "=" * 50)
    print("Leyenda de colores:")
    print("  🟢 Verde: Feliz")
    print("  🔴 Rojo: Enfadado")
    print("  🔵 Azul: Tímido")
    print("  🟡 Amarillo: Sociable")
    print("  🟠 Naranja: Comida")
    print("  🔷 Azul claro: Agua")
    print("\nPulsa ESC para salir")
    print("=" * 50 + "\n")
    
    # Ejecutar simulador
    sim.ejecutar()
    
    print("\n¡Simulación finalizada!")

if __name__ == "__main__":
    main()