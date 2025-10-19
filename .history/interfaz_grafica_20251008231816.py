"""
Interfaz gráfica principal del visualizador A*
"""
import tkinter as tk
from tkinter import messagebox
from constantes import *
from celda_widget import CeldaWidget
from algoritmo_astar import AlgoritmoAStar


class InterfazAStar:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Algoritmo A*")
        
        # Variables
        self.filas = 0
        self.columnas = 0
        self.celdas = {}
        self.canvas = None
        
        # Estado
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.modo = "inicio"
        
        # Algoritmo
        self.algoritmo = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea toda la interfaz gráfica"""
        # Frame de configuración
        self.crear_frame_configuracion()
        
        # Frame de modos
        self.crear_frame_modos()
        
        # Frame de acciones
        self.crear_frame_acciones()
        
        # Frame de leyenda
        self.crear_frame_leyenda()
        
        # Frame para canvas
        self.frame_canvas = tk.Frame(self.root)
        self.frame_canvas.pack(pady=10)
        
        # Frame de información
        self.crear_frame_info()
    
    def crear_frame_configuracion(self):
        """Crea el frame de configuración"""
        frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="⚙️ Configuración", 
                font=('Arial', 11, 'bold')).grid(row=0, column=0, columnspan=5, pady=5)
        
        tk.Label(frame, text="Filas:").grid(row=1, column=0, padx=5)
        self.entry_filas = tk.Entry(frame, width=5)
        self.entry_filas.grid(row=1, column=1, padx=5)
        self.entry_filas.insert(0, str(FILAS_DEFAULT))
        
        tk.Label(frame, text="Columnas:").grid(row=1, column=2, padx=5)
        self.entry_columnas = tk.Entry(frame, width=5)
        self.entry_columnas.grid(row=1, column=3, padx=5)
        self.entry_columnas.insert(0, str(COLUMNAS_DEFAULT))
        
        tk.Button(frame, text="Crear Cuadrícula", 
                 command=self.crear_cuadricula,
                 bg='lightgreen',
                 font=('Arial', 10, 'bold')).grid(row=1, column=4, padx=5)
    
    def crear_frame_modos(self):
        """Crea el frame de selección de modos"""
        frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="🎨 Modo de Dibujo", 
                font=('Arial', 11, 'bold')).pack(pady=5)
        
        frame_botones = tk.Frame(frame)
        frame_botones.pack()
        
        self.botones_modo = {}
        modos = [
            ("🟢 Punto Inicio", "inicio", COLORES['inicio']),
            ("🔴 Punto Final", "fin", COLORES['fin']),
            ("⬛ Obstáculos", "obstaculo", COLORES['obstaculo']),
            ("🗑️ Borrar", "borrar", 'white')
        ]
        
        for texto, modo, color in modos:
            btn = tk.Button(frame_botones, text=texto, width=15,
                          command=lambda m=modo: self.cambiar_modo(m),
                          bg=color, font=('Arial', 9))
            btn.pack(side=tk.LEFT, padx=3, pady=5)
            self.botones_modo[modo] = btn
        
        self.cambiar_modo("inicio")
    
    def crear_frame_acciones(self):
        """Crea el frame de botones de acción"""
        frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="🚀 Acciones", 
                font=('Arial', 11, 'bold')).pack(pady=5)
        
        frame_botones = tk.Frame(frame)
        frame_botones.pack()
        
        tk.Button(frame_botones, text="▶ Ejecutar A*",
                 command=self.ejecutar_astar,
                 bg='#2196F3', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=18, height=2).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(frame_botones, text="⏩ Paso a Paso",
                 command=self.ejecutar_paso_a_paso,
                 bg='#FF9800', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=18, height=2).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(frame_botones, text="🔄 Limpiar Todo",
                 command=self.limpiar_todo,
                 bg='#9E9E9E', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=18, height=2).pack(side=tk.LEFT, padx=5, pady=5)
    
    def crear_frame_leyenda(self):
        """Crea el frame de leyenda"""
        frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=2, bg='#f0f0f0')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="📊 Leyenda de Valores",
                font=('Arial', 11, 'bold'),
                bg='#f0f0f0').pack(pady=5)
        
        info_frame = tk.Frame(frame, bg='#f0f0f0')
        info_frame.pack()
        
        leyenda = [
            ("G", "Peso del movimiento (costo desde inicio)", "blue"),
            ("H", "Heurística (Distancia Manhattan al objetivo)", "green"),
            ("F", "Función de costo (F = G + H)", "red")
        ]
        
        for letra, desc, color in leyenda:
            item_frame = tk.Frame(info_frame, bg='#f0f0f0')
            item_frame.pack(anchor='w', padx=10, pady=2)
            
            tk.Label(item_frame, text=f"{letra}:", 
                    font=('Arial', 10, 'bold'),
                    fg=color, bg='#f0f0f0',
                    width=2).pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=desc,
                    font=('Arial', 9),
                    bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
    
    def crear_frame_info(self):
        """Crea el frame de información"""
        self.frame_info = tk.Frame(self.root, relief=tk.SUNKEN, 
                                   borderwidth=2, bg='white')
        self.frame_info.pack(pady=10, padx=10, fill=tk.X)
        
        self.label_info = tk.Label(self.frame_info,
                                   text="Crea una cuadrícula para comenzar",
                                   font=('Arial', 10),
                                   fg='blue', bg='white')
        self.label_info.pack(pady=10)
    
    def crear_cuadricula(self):
        """Crea la cuadrícula de celdas"""
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
            
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError
            
            if self.filas > MAX_FILAS or self.columnas > MAX_COLUMNAS:
                messagebox.showwarning("Advertencia",
                    f"Máximo {MAX_FILAS}x{MAX_COLUMNAS} para mejor visualización")
                return
        
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")
            return
        
        # Limpiar canvas anterior
        if self.canvas:
            self.canvas.destroy()
        
        # Resetear estado
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.celdas = {}
        
        # Crear canvas
        ancho = self.columnas * CELDA_SIZE
        alto = self.filas * CELDA_SIZE
        
        self.canvas = tk.Canvas(self.frame_canvas, width=ancho, height=alto,
                               bg='white', highlightthickness=1,
                               highlightbackground='black')
        self.canvas.pack()
        
        # Crear celdas
        for i in range(self.filas):
            for j in range(self.columnas):
                x = j * CELDA_SIZE
                y = i * CELDA_SIZE
                
                celda = CeldaWidget(self.canvas, x, y, CELDA_SIZE, i, j)
                celda.bind_click(self.click_celda)
                self.celdas[(i, j)] = celda
        
        self.label_info.config(text="✅ Cuadrícula creada. Selecciona inicio (verde) y fin (rojo)")
    
    def cambiar_modo(self, modo):
        """Cambia el modo de dibujo"""
        self.modo = modo
        for m, btn in self.botones_modo.items():
            if m == modo:
                btn.config(relief=tk.SUNKEN, borderwidth=4)
            else:
                btn.config(relief=tk.RAISED, borderwidth=2)
    
    def click_celda(self, fila, col):
        """Maneja el click en una celda"""
        if self.modo == "inicio":
            if self.inicio:
                self.celdas[self.inicio].colorear('vacio')
                self.celdas[self.inicio].limpiar_valores()
            self.inicio = (fila, col)
            self.celdas[(fila, col)].colorear('inicio')
            if (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
        
        elif self.modo == "fin":
            if self.fin:
                self.celdas[self.fin].colorear('vacio')
                self.celdas[self.fin].limpiar_valores()
            self.fin = (fila, col)
            self.celdas[(fila, col)].colorear('fin')
            if (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
        
        elif self.modo == "obstaculo":
            if (fila, col) != self.inicio and (fila, col) != self.fin:
                if (fila, col) in self.obstaculos:
                    self.obstaculos.remove((fila, col))
                    self.celdas[(fila, col)].colorear('vacio')
                else:
                    self.obstaculos.add((fila, col))
                    self.celdas[(fila, col)].colorear('obstaculo')
        
        elif self.modo == "borrar":
            if (fila, col) == self.inicio:
                self.inicio = None
            elif (fila, col) == self.fin:
                self.fin = None
            elif (fila, col) in self.obstaculos:
                self.obstaculos.remove((fila, col))
            self.celdas[(fila, col)].colorear('vacio')
            self.celdas[(fila, col)].limpiar_valores()
    
    def ejecutar_astar(self):
        """Ejecuta el algoritmo A* completo"""
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        self.label_info.config(text="⏳ Ejecutando A*...")
        self.root.update()
        
        # Crear y ejecutar algoritmo
        self.algoritmo = AlgoritmoAStar(
            self.inicio, self.fin,
            self.filas, self.columnas,
            self.obstaculos
        )
        
        paso = 0
        while True:
            paso += 1
            actual, vecinos, encontrado = self.algoritmo.ejecutar_paso()
            
            if actual is None:
                self.label_info.config(text="❌ No se encontró camino")
                messagebox.showerror("Error", "No se encontró un camino")
                return
            
            # Visualizar nodo actual
            if actual != self.inicio and actual != self.fin:
                self.celdas[actual].colorear('visitado')
            
            # Visualizar vecinos
            for vecino in vecinos:
                if vecino != self.inicio and vecino != self.fin:
                    g = self.algoritmo.costo_g[vecino]
                    h = self.algoritmo.costo_h[vecino]
                    f = self.algoritmo.costo_f[vecino]
                    
                    self.celdas[vecino].colorear('visitado')
                    self.celdas[vecino].actualizar_valores(g, h, f)
            
            self.root.update()
            
            if encontrado:
                # Mostrar camino
                from funciones_astar import reconstruir_camino
                camino = reconstruir_camino(self.algoritmo.vino_de, 
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = self.algoritmo.costo_g[self.fin]
                self.label_info.config(
                    text=f"✅ ¡Camino encontrado! Longitud: {longitud} | Nodos explorados: {paso}"
                )
                messagebox.showinfo("¡Éxito!",
                    f"Camino encontrado!\n\nLongitud: {longitud}\nNodos explorados: {paso}")
                return
    
    def ejecutar_paso_a_paso(self):
        """Ejecuta el algoritmo paso a paso"""
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        
        # Crear algoritmo
        self.algoritmo = AlgoritmoAStar(
            self.inicio, self.fin,
            self.filas, self.columnas,
            self.obstaculos
        )
        
        self.paso_actual = 0
        
        def siguiente_paso():
            self.paso_actual += 1
            actual, vecinos, encontrado = self.algoritmo.ejecutar_paso()
            
            if actual is None:
                self.label_info.config(text="❌ No se encontró camino")
                messagebox.showerror("Error", "No se encontró un camino")
                return
            
            # Visualizar
            if actual != self.inicio and actual != self.fin:
                self.celdas[actual].colorear('visitado')
            
            for vecino in vecinos:
                if vecino != self.inicio and vecino != self.fin:
                    g = self.algoritmo.costo_g[vecino]
                    h = self.algoritmo.costo_h[vecino]
                    f = self.algoritmo.costo_f[vecino]
                    
                    self.celdas[vecino].colorear('visitado')
                    self.celdas[vecino].actualizar_valores(g, h, f)
            
            if encontrado:
                from funciones_astar import reconstruir_camino
                camino = reconstruir_camino(self.algoritmo.vino_de,
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = self.algoritmo.costo_g[self.fin]
                self.label_info.config(
                    text=f"✅ ¡Camino encontrado! Longitud: {longitud} | Pasos: {self.paso_actual}"
                )
                messagebox.showinfo("¡Éxito!",
                    f"Camino encontrado en {self.paso_actual} pasos!\n\nLongitud: {longitud}")
                btn_siguiente.destroy()
                return
            
            self.label_info.config(
                text=f"Paso {self.paso_actual}: Explorando {actual} | F={self.algoritmo.costo_f[actual]}"
            )
        
        # Crear botón siguiente
        btn_siguiente = tk.Button(self.frame_info, text="▶ Siguiente Paso",
                                 command=siguiente_paso,
                                 bg='lightgreen',
                                 font=('Arial', 10, 'bold'))
        btn_siguiente.pack(pady=5)
        
        siguiente_paso()
    
    def validar_inicio_fin(self):
        """Valida que exista inicio y fin"""
        if not self.inicio:
            messagebox.showerror("Error", "Selecciona un punto de inicio (verde)")
            return False
        if not self.fin:
            messagebox.showerror("Error", "Selecciona un punto final (rojo)")
            return False
        return True
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda anterior"""
        for pos, celda in self.celdas.items():
            if pos not in self.obstaculos and pos != self.inicio and pos != self.fin:
                celda.colorear('vacio')
                celda.limpiar_valores()
    
    def limpiar_todo(self):
        """Limpia todo el tablero"""
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        
        for celda in self.celdas.values():
            celda.colorear('vacio')
            celda.limpiar_valores()
        
        self.label_info.config(text="🧹 Todo limpio. Listo para empezar")