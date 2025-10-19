"""
Archivo principal para ejecutar el visualizador A*
"""
import tkinter as tk
from interfaz_grafica import InterfazAStar


def main():
    """Función principal"""
    root = tk.Tk()
    root.resizable(False, False)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    # Crear aplicación
    app = InterfazAStar(root)
    
    # Ejecutar
    root.mainloop()


if __name__ == "__main__":
    main()