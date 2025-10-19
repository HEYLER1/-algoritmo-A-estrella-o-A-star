import tkinter as tk
from tkinter import messagebox
import heapq

class AStarGrid:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo A* - Pathfinding")
        
        # Variables
        self.filas = 0
        self.columnas = 0
        self.celda_size = 50
        self.grid = []
        self.canvas = None
        self.rectangulos = {}
        
        # Estados
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.modo = "inicio"  # inicio, fin, obstaculo, borrar
        
        # Colores
        self.colores = {
            'vacio': 'white',
            'inicio': 'green',
            'fin': 'red',
            'obstaculo': 'black',
            'visitado': 'lightblue',
            'camino': 'yellow'
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame superior para configuración
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=10)
        
        tk.Label(frame_config, text="Filas:").grid(row=0, column=0, padx=5)
        self.entry_filas = tk.Entry(frame_config, width=5)
        self.entry_filas.grid(row=0, column=1, padx=5)
        self.entry_filas.insert(0, "10")
        
        tk.Label(frame_config, text="Columnas:").grid(row=0, column=2, padx=5)
        self.entry_columnas = tk.Entry(frame_config, width=5)
        self.entry_columnas.grid(row=0, column=3, padx=5)
        self.entry_columnas.insert(0, "10")
        
        tk.Button(frame_config, text="Crear Cuadrícula", 
                 command=self.crear_cuadricula, bg='lightgreen').grid(row=0, column=4, padx=5)
        
        # Frame para botones de modo
        frame_modos = tk.Frame(self.root)
        frame_modos.pack(pady=10)
        
        tk.Label(frame_modos, text="Modo:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.botones_modo = {}
        modos = [
            ("Punto Inicio", "inicio", 'lightgreen'),
            ("Punto Final", "fin", 'lightcoral'),
            ("Obstáculos", "obstaculo", 'gray'),
            ("Borrar", "borrar", 'white')
        ]
        
        for texto, modo, color in modos:
            btn = tk.Button(frame_modos, text=texto, width=12,
                          command=lambda m=modo: self.cambiar_modo(m),
                          bg=color)
            btn.pack(side=tk.LEFT, padx=2)
            self.botones_modo[modo] = btn
        
        # Frame para botones de acción
        frame_acciones = tk.Frame(self.root)
        frame_acciones.pack(pady=10)
        
        tk.Button(frame_acciones, text="▶ Ejecutar A*", 
                 command=self.ejecutar_astar, bg='lightblue', 
                 font=('Arial', 12, 'bold'), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_acciones, text="🔄 Limpiar Todo", 
                 command=self.limpiar_todo, bg='lightyellow', 
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_acciones, text="🗑️ Limpiar Búsqueda", 
                 command=self.limpiar_busqueda, bg='lightgray', 
                 width=15).pack(side=tk.LEFT, padx=5)
        
        # Frame para el canvas
        self.frame_canvas = tk.Frame(self.root)
        self.frame_canvas.pack(pady=10)
        
        # Instrucciones
        frame_info = tk.Frame(self.root)
        frame_info.pack(pady=10)
        tk.Label(frame_info, text="Instrucciones: 1) Crea la cuadrícula  2) Selecciona modo  3) Click en celdas  4) Ejecuta A*", 
                fg='blue').pack()
    
    def crear_cuadricula(self):
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
            
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError
                
            if self.filas > 30 or self.columnas > 30:
                messagebox.showwarning("Advertencia", "Máximo 30x30 para mejor rendimiento")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")
            return
        
        # Limpiar canvas anterior
        if self.canvas:
            self.canvas.destroy()
        
        # Resetear variables
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.rectangulos = {}
        
        # Crear nuevo canvas
        ancho = self.columnas * self.celda_size
        alto = self.filas * self.celda_size
        
        self.canvas = tk.Canvas(self.frame_canvas, width=ancho, height=alto, bg='white')
        self.canvas.pack()
        
        # Dibujar cuadrícula
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * self.celda_size
                y1 = i * self.celda_size
                x2 = x1 + self.celda_size
                y2 = y1 + self.celda_size
                
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                    fill='white', outline='gray')
                self.rectangulos[(i, j)] = rect
                
                # Bind click
                self.canvas.tag_bind(rect, '<Button-1>', 
                                    lambda e, i=i, j=j: self.click_celda(i, j))
    
    def cambiar_modo(self, modo):
        self.modo = modo
        # Resaltar botón activo
        for m, btn in self.botones_modo.items():
            if m == modo:
                btn.config(relief=tk.SUNKEN, borderwidth=3)
            else:
                btn.config(relief=tk.RAISED, borderwidth=2)
    
    def click_celda(self, fila, col):
        if self.modo == "inicio":
            if self.inicio:
                self.colorear_celda(*self.inicio, 'vacio')
            self.inicio = (fila, col)
            self.colorear_celda(fila, col, 'inicio')
            if (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
            
        elif self.modo == "fin":
            if self.fin:
                self.colorear_celda(*self.fin, 'vacio')
            self.fin = (fila, col)
            self.colorear_celda(fila, col, 'fin')
            if (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
            
        elif self.modo == "obstaculo":
            if (fila, col) != self.inicio and (fila, col) != self.fin:
                if (fila, col) in self.obstaculos:
                    self.obstaculos.remove((fila, col))
                    self.colorear_celda(fila, col, 'vacio')
                else:
                    self.obstaculos.add((fila, col))
                    self.colorear_celda(fila, col, 'obstaculo')
        
        elif self.modo == "borrar":
            if (fila, col) == self.inicio:
                self.inicio = None
            elif (fila, col) == self.fin:
                self.fin = None
            elif (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
            self.colorear_celda(fila, col, 'vacio')
    
    def colorear_celda(self, fila, col, tipo):
        if (fila, col) in self.rectangulos:
            color = self.colores[tipo]
            self.canvas.itemconfig(self.rectangulos[(fila, col)], fill=color)
    
    def heuristica(self, a, b):
        # Distancia Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def obtener_vecinos(self, nodo):
        fila, col = nodo
        vecinos = []
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            if (0 <= nueva_fila < self.filas and 
                0 <= nueva_col < self.columnas and
                (nueva_fila, nueva_col) not in self.obstaculos):
                vecinos.append((nueva_fila, nueva_col))
        
        return vecinos
    
    def ejecutar_astar(self):
        if not self.inicio:
            messagebox.showerror("Error", "Selecciona un punto de inicio")
            return
        if not self.fin:
            messagebox.showerror("Error", "Selecciona un punto final")
            return
        
        # Limpiar búsqueda anterior
        self.limpiar_busqueda()
        
        # Algoritmo A*
        frontera = []
        heapq.heappush(frontera, (0, self.inicio))
        
        vino_de = {}
        costo_g = {self.inicio: 0}
        
        while frontera:
            _, actual = heapq.heappop(frontera)
            
            if actual == self.fin:
                # Reconstruir camino
                self.reconstruir_camino(vino_de)
                messagebox.showinfo("¡Éxito!", "¡Camino encontrado!")
                return
            
            for vecino in self.obtener_vecinos(actual):
                nuevo_costo = costo_g[actual] + 1
                
                if vecino not in costo_g or nuevo_costo < costo_g[vecino]:
                    costo_g[vecino] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(vecino, self.fin)
                    heapq.heappush(frontera, (prioridad, vecino))
                    vino_de[vecino] = actual
                    
                    # Colorear celda visitada
                    if vecino != self.fin and vecino != self.inicio:
                        self.colorear_celda(*vecino, 'visitado')
                        self.root.update()
        
        messagebox.showerror("Error", "No se encontró un camino")
    
    def reconstruir_camino(self, vino_de):
        actual = self.fin
        while actual in vino_de:
            actual = vino_de[actual]
            if actual != self.inicio:
                self.colorear_celda(*actual, 'camino')
    
    def limpiar_busqueda(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if (i, j) not in self.obstaculos and (i, j) != self.inicio and (i, j) != self.fin:
                    self.colorear_celda(i, j, 'vacio')
    
    def limpiar_todo(self):
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        if self.canvas:
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.colorear_celda(i, j, 'vacio')

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AStarGrid(root)
    root.mainloop()