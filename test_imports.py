"""
Archivo de diagnóstico para verificar importaciones
"""
import sys
print("Python version:", sys.version)
print("Python path:", sys.executable)
print("\n" + "="*60)

try:
    print("✓ Importando tkinter...")
    import tkinter as tk
    print("  ✅ tkinter OK")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Importando constantes...")
    from constantes import CELDA_SIZE, COLORES
    print(f"  ✅ constantes OK (CELDA_SIZE={CELDA_SIZE})")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("✓ Importando funciones_astar...")
    from funciones_astar import calcular_heuristica
    print("  ✅ funciones_astar OK")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("✓ Importando celda_widget...")
    from celda_widget import CeldaWidget
    print("  ✅ celda_widget OK")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("✓ Importando algoritmo_astar...")
    from algoritmo_astar import AlgoritmoAStar
    print("  ✅ algoritmo_astar OK")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("✓ Importando interfaz_grafica...")
    from interfaz_grafica import InterfazAStar
    print("  ✅ interfaz_grafica OK")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Diagnóstico completado")
print("="*60)
input("\nPresiona Enter para salir...")