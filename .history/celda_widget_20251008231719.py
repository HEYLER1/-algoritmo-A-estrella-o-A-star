"""
Widget personalizado para mostrar información de cada celda
"""
import tkinter as tk
from constantes import COLORES


class CeldaWidget:
    def __init__(self, canvas, x, y, size, fila, col):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.fila = fila
        self.col = col
        
        # Crear elementos visuales
        self.rectangulo = canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=COLORES['vacio'],
            outline='gray',
            width=2
        )
        
        # Textos para G, H, F
        self.texto_g = canvas.create_text(
            x + 15, y + 15,
            text="",
            font=('Arial', 8, 'bold'),
            fill='blue',
            anchor='w'
        )
        
        self.texto_h = canvas.create_text(
            x + size - 15, y + 15,
            text="",
            font=('Arial', 8, 'bold'),
            fill='green',
            anchor='e'
        )
        
        self.texto_f = canvas.create_text(
            x + size/2, y + size - 15,
            text="",
            font=('Arial', 9, 'bold'),
            fill='red',
            anchor='center'
        )
        
        # Etiquetas
        canvas.create_text(
            x + 5, y + 5,
            text="G",
            font=('Arial', 7),
            fill='blue',
            anchor='nw'
        )
        
        canvas.create_text(
            x + size - 5, y + 5,
            text="H",
            font=('Arial', 7),
            fill='green',
            anchor='ne'
        )
        
        canvas.create_text(
            x + size/2, y + size - 25,
            text="F",
            font=('Arial', 7),
            fill='red',
            anchor='center'
        )
    
    def colorear(self, tipo):
        """Colorea la celda según su tipo"""
        color = COLORES.get(tipo, COLORES['vacio'])
        self.canvas.itemconfig(self.rectangulo, fill=color)
    
    def actualizar_valores(self, g=None, h=None, f=None):
        """Actualiza los valores G, H, F"""
        if g is not None:
            self.canvas.itemconfig(self.texto_g, text=str(g))
        
        if h is not None:
            self.canvas.itemconfig(self.texto_h, text=str(h))
        
        if f is not None:
            self.canvas.itemconfig(self.texto_f, text=str(f))
    
    def limpiar_valores(self):
        """Limpia los valores de la celda"""
        self.canvas.itemconfig(self.texto_g, text="")
        self.canvas.itemconfig(self.texto_h, text="")
        self.canvas.itemconfig(self.texto_f, text="")
    
    def bind_click(self, callback):
        """Asocia un callback al click"""
        self.canvas.tag_bind(self.rectangulo, '<Button-1>', 
                            lambda e: callback(self.fila, self.col))