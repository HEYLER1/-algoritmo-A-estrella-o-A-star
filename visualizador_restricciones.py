"""
Módulo para visualizar las restricciones diagonales
"""
import tkinter as tk
from tkinter import messagebox


def mostrar_restricciones_diagonales():
    """
    Muestra una ventana explicando las restricciones diagonales con imágenes
    """
    ventana = tk.Toplevel()
    ventana.title("Restricciones de Movimiento Diagonal")
    ventana.geometry("800x600")
    
    # Frame principal con scroll
    canvas = tk.Canvas(ventana, bg='white')
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='white')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Título
    tk.Label(scrollable_frame, text="🚫 Restricciones de Movimiento Diagonal",
            font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
    
    # Explicación
    explicacion = """
Para moverse en diagonal, las dos celdas adyacentes DEBEN estar libres.
Esto simula el comportamiento realista donde no puedes "atravesar esquinas".
    """
    tk.Label(scrollable_frame, text=explicacion, 
            font=('Arial', 11), bg='white', justify=tk.LEFT).pack(pady=10)
    
    # ===== CASOS PERMITIDOS =====
    tk.Label(scrollable_frame, text="✅ MOVIMIENTOS PERMITIDOS",
            font=('Arial', 14, 'bold'), bg='#c8e6c9', fg='#2e7d32',
            width=80, anchor='w', padx=10).pack(fill=tk.X, pady=(20, 10))
    
    casos_permitidos = [
        {
            'nombre': '↗ Diagonal Arriba-Derecha',
            'explicacion': 'Puede moverse porque las celdas arriba y derecha están libres',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (0, 2),
            'adyacentes': [(1, 2), (0, 1)]
        },
        {
            'nombre': '↘ Diagonal Abajo-Derecha',
            'explicacion': 'Puede moverse porque las celdas abajo y derecha están libres',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (2, 2),
            'adyacentes': [(1, 2), (2, 1)]
        },
        {
            'nombre': '↙ Diagonal Abajo-Izquierda',
            'explicacion': 'Puede moverse porque las celdas abajo e izquierda están libres',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (2, 0),
            'adyacentes': [(1, 0), (2, 1)]
        },
        {
            'nombre': '↖ Diagonal Arriba-Izquierda',
            'explicacion': 'Puede moverse porque las celdas arriba e izquierda están libres',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (0, 0),
            'adyacentes': [(1, 0), (0, 1)]
        }
    ]
    
    for caso in casos_permitidos:
        crear_ejemplo_visual(scrollable_frame, caso, True)
    
    # ===== CASOS BLOQUEADOS =====
    tk.Label(scrollable_frame, text="❌ MOVIMIENTOS BLOQUEADOS",
            font=('Arial', 14, 'bold'), bg='#ffcdd2', fg='#c62828',
            width=80, anchor='w', padx=10).pack(fill=tk.X, pady=(20, 10))
    
    casos_bloqueados = [
        {
            'nombre': '↗ Bloqueado por obstáculo arriba',
            'explicacion': 'NO puede moverse porque hay obstáculo en la celda superior',
            'grid': [
                ['⬜', '⬛', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (0, 2),
            'bloqueador': (0, 1)
        },
        {
            'nombre': '↗ Bloqueado por obstáculo derecha',
            'explicacion': 'NO puede moverse porque hay obstáculo en la celda derecha',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬛'],
                ['⬜', '⬜', '⬜']
            ],
            'origen': (1, 1),
            'destino': (0, 2),
            'bloqueador': (1, 2)
        },
        {
            'nombre': '↘ Bloqueado por obstáculo abajo',
            'explicacion': 'NO puede moverse porque hay obstáculo en la celda inferior',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬛', '⬜']
            ],
            'origen': (1, 1),
            'destino': (2, 2),
            'bloqueador': (2, 1)
        },
        {
            'nombre': '↙ Bloqueado por ambos lados',
            'explicacion': 'NO puede moverse porque hay obstáculos en ambas celdas adyacentes',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬛', '🟦', '⬜'],
                ['⬜', '⬛', '⬜']
            ],
            'origen': (1, 1),
            'destino': (2, 0),
            'bloqueador': None  # Múltiples bloqueadores
        },
        {
            'nombre': '↘ Bloqueado por destino con obstáculo',
            'explicacion': 'NO puede moverse porque el destino mismo es un obstáculo',
            'grid': [
                ['⬜', '⬜', '⬜'],
                ['⬜', '🟦', '⬜'],
                ['⬜', '⬜', '⬛']
            ],
            'origen': (1, 1),
            'destino': (2, 2),
            'bloqueador': (2, 2)
        }
    ]
    
    for caso in casos_bloqueados:
        crear_ejemplo_visual(scrollable_frame, caso, False)
    
    # Regla general
    tk.Label(scrollable_frame, text="📐 REGLA GENERAL",
            font=('Arial', 14, 'bold'), bg='#fff9c4',
            width=80, anchor='w', padx=10).pack(fill=tk.X, pady=(20, 10))
    
    regla = """
Para moverse de la celda (fila, col) a la celda diagonal (fila±1, col±1):

1. La celda destino (fila±1, col±1) NO debe ser obstáculo
2. La celda horizontal (fila, col±1) NO debe ser obstáculo  
3. La celda vertical (fila±1, col) NO debe ser obstáculo

Si ALGUNA de estas condiciones falla, el movimiento diagonal está BLOQUEADO.
    """
    tk.Label(scrollable_frame, text=regla,
            font=('Arial', 10), bg='white', justify=tk.LEFT).pack(pady=10, padx=20)
    
    # Botón cerrar
    tk.Button(scrollable_frame, text="Cerrar", command=ventana.destroy,
             bg='#2196F3', fg='white', font=('Arial', 12, 'bold'),
             width=20, height=2).pack(pady=20)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def crear_ejemplo_visual(parent, caso, permitido):
    """
    Crea un ejemplo visual de un caso de movimiento diagonal
    """
    frame_caso = tk.Frame(parent, relief=tk.RIDGE, borderwidth=2, 
                         bg='#e8f5e9' if permitido else '#ffebee')
    frame_caso.pack(fill=tk.X, padx=20, pady=10)
    
    # Título del caso
    color_titulo = '#2e7d32' if permitido else '#c62828'
    tk.Label(frame_caso, text=caso['nombre'],
            font=('Arial', 12, 'bold'), fg=color_titulo,
            bg='#e8f5e9' if permitido else '#ffebee').pack(pady=5)
    
    # Grid visual
    frame_grid = tk.Frame(frame_caso, bg='white')
    frame_grid.pack(pady=5)
    
    for i, fila in enumerate(caso['grid']):
        frame_fila = tk.Frame(frame_grid, bg='white')
        frame_fila.pack()
        for j, celda in enumerate(fila):
            # Determinar el color de fondo
            if (i, j) == caso['origen']:
                bg_color = '#2196F3'  # Azul para origen
            elif (i, j) == caso['destino']:
                if permitido:
                    bg_color = '#4CAF50'  # Verde para destino permitido
                else:
                    bg_color = '#F44336'  # Rojo para destino bloqueado
            elif celda == '⬛':
                bg_color = '#424242'  # Negro para obstáculo
            else:
                bg_color = 'white'
            
            tk.Label(frame_fila, text=celda, font=('Arial', 20),
                    width=3, height=1, relief=tk.SOLID, borderwidth=1,
                    bg=bg_color).pack(side=tk.LEFT)
    
    # Explicación
    tk.Label(frame_caso, text=caso['explicacion'],
            font=('Arial', 10), bg='#e8f5e9' if permitido else '#ffebee',
            wraplength=600).pack(pady=5, padx=10)


def crear_boton_info_restricciones(parent):
    """
    Crea un botón para mostrar información sobre restricciones
    """
    tk.Button(parent, text="📚 Ver Restricciones Diagonales",
             command=mostrar_restricciones_diagonales,
             bg='#FFC107', font=('Arial', 10, 'bold')).pack(pady=5)