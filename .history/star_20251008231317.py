import tkinter as tk
from tkinter import messagebox, ttk
import heapq

class AStarGrid:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo A* - Pathfinding con Costos")
        
        # Variables
        self.filas = 0
        self.columnas = 0
        self.celda_size = 60  # Aumentado para mostrar valores
        self.grid = []
        self.canvas = None
        self.rectangulos = {}
        self.textos = {}  # Para mostrar valores en celdas
        
        # Estados
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.modo = "inicio"
        
        # Datos del algoritmo
        self.costo_g = {}  # Costo desde inicio
        self.costo_h = {}  # Heurística
        self.costo_f = {}  # Función de costo total
        self.mostrar_valores = tk.BooleanVar(value=True)
        
        # Colores
        self.colores = {
            'vacio': 'white',
            'inicio': 'green',
            'fin': 'red',
            'obstaculo': 'black',
            'visitado': 'lightblue',
            'camino': 'yellow',
            'frontera': 'orange'
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame superior para configuración
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=10)
        
        tk.Label(frame_config, text="Filas:").grid(row=0, column=0, padx=5)
        self.entry_filas = tk.Entry(frame_config, width=5)
        self.entry_filas.grid(row=0, column=1, padx=5)
        self.entry_filas.insert(0, "8")
        
        tk.Label(frame_config, text="Columnas:").grid(row=0, column=2, padx=5)
        self.entry_columnas = tk.Entry(frame_config, width=5)
        self.entry_columnas.grid(row=0, column=3, padx=5)
        self.entry_columnas.insert(0, "10")
        
        tk.Button(frame_config, text="Crear Cuadrícula", 
                 command=self.crear_cuadricula, bg='lightgreen').grid(row=0, column=4, padx=5)
        
        # Checkbox para mostrar valores
        tk.Checkbutton(frame_config, text="Mostrar Valores", 
                      variable=self.mostrar_valores,
                      command=self.actualizar_visualizacion).grid(row=0, column=5, padx=5)
        
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
        
        tk.Button(frame_acciones, text="⏩ Paso a Paso", 
                 command=self.ejecutar_paso_a_paso, bg='lightyellow', 
                 font=('Arial', 12, 'bold'), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_acciones, text="🔄 Limpiar Todo", 
                 command=self.limpiar_todo, bg='lightgray', 
                 width=15).pack(side=tk.LEFT, padx=5)
        
        # Frame para leyenda
        frame_leyenda = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=2)
        frame_leyenda.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_leyenda, text="Leyenda de Valores:", 
                font=('Arial', 11, 'bold')).pack()
        
        leyenda_texto = """
        g = Costo desde inicio (peso del movimiento acumulado)
        h = Heurística (distancia estimada al objetivo)
        f = g + h (función de costo total)
        """
        tk.Label(frame_leyenda, text=leyenda_texto, 
                justify=tk.LEFT, font=('Arial', 9)).pack()
        
        # Frame para el canvas
        self.frame_canvas = tk.Frame(self.root)
        self.frame_canvas.pack(pady=10)
        
        # Frame para información
        self.frame_info = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        self.frame_info.pack(pady=10, padx=10, fill=tk.X)
        
        self.label_info = tk.Label(self.frame_info, text="Esperando inicio...", 
                                   font=('Arial', 10), fg='blue')
        self.label_info.pack(pady=5)
    
    def crear_cuadricula(self):
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
            
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError
                
            if self.filas > 20 or self.columnas > 20:
                messagebox.showwarning("Advertencia", "Máximo 20x20 para mejor visualización")
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
        self.textos = {}
        self.costo_g = {}
        self.costo_h = {}
        self.costo_f = {}
        
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
                                                    fill='white', outline='gray', width=2)
                self.rectangulos[(i, j)] = rect
                
                # Crear texto para valores
                cx = x1 + self.celda_size / 2
                cy = y1 + self.celda_size / 2
                texto = self.canvas.create_text(cx, cy, text="", 
                                               font=('Arial', 8), fill='black')
                self.textos[(i, j)] = texto
                
                # Bind click
                self.canvas.tag_bind(rect, '<Button-1>', 
                                    lambda e, i=i, j=j: self.click_celda(i, j))
        
        self.label_info.config(text="Cuadrícula creada. Selecciona inicio y fin.")
    
    def cambiar_modo(self, modo):
        self.modo = modo
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
            self.actualizar_texto_celda(fila, col, "")
    
    def colorear_celda(self, fila, col, tipo):
        if (fila, col) in self.rectangulos:
            color = self.colores[tipo]
            self.canvas.itemconfig(self.rectangulos[(fila, col)], fill=color)
    
    def actualizar_texto_celda(self, fila, col, texto):
        if (fila, col) in self.textos:
            self.canvas.itemconfig(self.textos[(fila, col)], text=texto)
    
    def actualizar_visualizacion(self):
        if not self.mostrar_valores.get():
            # Ocultar todos los textos
            for pos in self.textos:
                if pos != self.inicio and pos != self.fin:
                    self.actualizar_texto_celda(*pos, "")
        else:
            # Mostrar valores calculados
            self.mostrar_costos_en_celdas()
    
    def mostrar_costos_en_celdas(self):
        for pos in self.costo_f:
            if pos != self.inicio and pos != self.fin and self.mostrar_valores.get():
                g = self.costo_g.get(pos, 0)
                h = self.costo_h.get(pos, 0)
                f = self.costo_f.get(pos, 0)
                texto = f"g:{g}\nh:{h}\nf:{f}"
                self.actualizar_texto_celda(*pos, texto)
    
    # ===== FUNCIONES DEL ALGORITMO A* =====
    
    def calcular_peso_movimiento(self, desde, hacia):
        """
        Calcula el peso del movimiento entre dos celdas adyacentes.
        Por defecto es 1 para movimientos horizontales/verticales.
        """
        return 1
    
    def calcular_heuristica(self, nodo_actual, nodo_objetivo):
        """
        Calcula la heurística (h) usando distancia Manhattan.
        h = |x1 - x2| + |y1 - y2|
        """
        return abs(nodo_actual[0] - nodo_objetivo[0]) + abs(nodo_actual[1] - nodo_objetivo[1])
    
    def calcular_funcion_costo(self, costo_g, costo_h):
        """
        Calcula la función de costo total.
        f = g + h
        donde:
        - g es el costo real desde el inicio
        - h es la heurística (estimación al objetivo)
        """
        return costo_g + costo_h
    
    def obtener_vecinos(self, nodo):
        """
        Obtiene los vecinos válidos de un nodo.
        """
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
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        self.label_info.config(text="Ejecutando A*...")
        
        # Inicializar estructuras
        frontera = []
        heapq.heappush(frontera, (0, self.inicio))
        
        vino_de = {}
        self.costo_g = {self.inicio: 0}
        self.costo_h = {self.inicio: self.calcular_heuristica(self.inicio, self.fin)}
        self.costo_f = {self.inicio: self.calcular_funcion_costo(
            self.costo_g[self.inicio], 
            self.costo_h[self.inicio]
        )}
        
        nodos_explorados = 0
        
        while frontera:
            _, actual = heapq.heappop(frontera)
            nodos_explorados += 1
            
            # Actualizar información
            self.label_info.config(text=f"Explorando nodo {actual} | Nodos explorados: {nodos_explorados}")
            self.root.update()
            
            if actual == self.fin:
                self.reconstruir_camino(vino_de)
                longitud_camino = self.costo_g[self.fin]
                self.label_info.config(
                    text=f"¡Camino encontrado! Longitud: {longitud_camino} | Nodos explorados: {nodos_explorados}"
                )
                messagebox.showinfo("¡Éxito!", 
                    f"Camino encontrado!\n\nLongitud: {longitud_camino}\nNodos explorados: {nodos_explorados}")
                return
            
            for vecino in self.obtener_vecinos(actual):
                # Calcular nuevo costo g
                peso_movimiento = self.calcular_peso_movimiento(actual, vecino)
                nuevo_costo_g = self.costo_g[actual] + peso_movimiento
                
                if vecino not in self.costo_g or nuevo_costo_g < self.costo_g[vecino]:
                    # Actualizar costos
                    self.costo_g[vecino] = nuevo_costo_g
                    self.costo_h[vecino] = self.calcular_heuristica(vecino, self.fin)
                    self.costo_f[vecino] = self.calcular_funcion_costo(
                        self.costo_g[vecino],
                        self.costo_h[vecino]
                    )
                    
                    # Agregar a frontera
                    heapq.heappush(frontera, (self.costo_f[vecino], vecino))
                    vino_de[vecino] = actual
                    
                    # Visualizar
                    if vecino != self.fin and vecino != self.inicio:
                        self.colorear_celda(*vecino, 'visitado')
                        if self.mostrar_valores.get():
                            g = self.costo_g[vecino]
                            h = self.costo_h[vecino]
                            f = self.costo_f[vecino]
                            self.actualizar_texto_celda(*vecino, f"g:{g}\nh:{h}\nf:{f}")
                    
                    self.root.update()
        
        self.label_info.config(text="No se encontró camino")
        messagebox.showerror("Error", "No se encontró un camino")
    
    def ejecutar_paso_a_paso(self):
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        
        # Inicializar estructuras
        frontera = []
        heapq.heappush(frontera, (0, self.inicio))
        
        vino_de = {}
        self.costo_g = {self.inicio: 0}
        self.costo_h = {self.inicio: self.calcular_heuristica(self.inicio, self.fin)}
        self.costo_f = {self.inicio: self.calcular_funcion_costo(
            self.costo_g[self.inicio], 
            self.costo_h[self.inicio]
        )}
        
        paso = 0
        
        def siguiente_paso():
            nonlocal paso
            if not frontera:
                self.label_info.config(text="No se encontró camino")
                messagebox.showerror("Error", "No se encontró un camino")
                return
            
            paso += 1
            _, actual = heapq.heappop(frontera)
            
            self.label_info.config(text=f"Paso {paso}: Explorando {actual} | f={self.costo_f[actual]}")
            
            if actual == self.fin:
                self.reconstruir_camino(vino_de)
                longitud_camino = self.costo_g[self.fin]
                self.label_info.config(text=f"¡Camino encontrado! Longitud: {longitud_camino} | Pasos: {paso}")
                messagebox.showinfo("¡Éxito!", f"Camino encontrado en {paso} pasos!\n\nLongitud: {longitud_camino}")
                return
            
            for vecino in self.obtener_vecinos(actual):
                peso_movimiento = self.calcular_peso_movimiento(actual, vecino)
                nuevo_costo_g = self.costo_g[actual] + peso_movimiento
                
                if vecino not in self.costo_g or nuevo_costo_g < self.costo_g[vecino]:
                    self.costo_g[vecino] = nuevo_costo_g
                    self.costo_h[vecino] = self.calcular_heuristica(vecino, self.fin)
                    self.costo_f[vecino] = self.calcular_funcion_costo(
                        self.costo_g[vecino],
                        self.costo_h[vecino]
                    )
                    
                    heapq.heappush(frontera, (self.costo_f[vecino], vecino))
                    vino_de[vecino] = actual
                    
                    if vecino != self.fin and vecino != self.inicio:
                        self.colorear_celda(*vecino, 'visitado')
                        if self.mostrar_valores.get():
                            g = self.costo_g[vecino]
                            h = self.costo_h[vecino]
                            f = self.costo_f[vecino]
                            self.actualizar_texto_celda(*vecino, f"g:{g}\nh:{h}\nf:{f}")
            
            # Botón para siguiente paso
            btn_siguiente = tk.Button(self.frame_info, text="▶ Siguiente Paso", 
                                     command=siguiente_paso, bg='lightgreen')
            btn_siguiente.pack(pady=5)
            
            # Auto-destruir botón anterior si existe
            for widget in self.frame_info.winfo_children():
                if widget != self.label_info and widget != btn_siguiente:
                    widget.destroy()
        
        # Iniciar primer paso
        siguiente_paso()
    
    def reconstruir_camino(self, vino_de):
        actual = self.fin
        while actual in vino_de:
            actual = vino_de[actual]
            if actual != self.inicio:
                self.colorear_celda(*actual, 'camino')
    
    def validar_inicio_fin(self):
        if not self.inicio:
            messagebox.showerror("Error", "Selecciona un punto de inicio")
            return False
        if not self.fin:
            messagebox.showerror("Error", "Selecciona un punto final")
            return False
        return True
    
    def limpiar_busqueda(self):
        self.costo_g = {}
        self.costo_h = {}
        self.costo_f = {}
        
        for i in range(self.filas):
            for j in range(self.columnas):
                if (i, j) not in self.obstaculos and (i, j) != self.inicio and (i, j) != self.fin:
                    self.colorear_celda(i, j, 'vacio')
                    self.actualizar_texto_celda(i, j, "")
    
    def limpiar_todo(self):
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.costo_g = {}
        self.costo_h = {}
        self.costo_f = {}
        
        if self.canvas:
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.colorear_celda(i, j, 'vacio')
                    self.actualizar_texto_celda(i, j, "")
        
        self.label_info.config(text="Todo limpio. Listo para empezar.")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AStarGrid(root)
    root.mainloop()