"""
Interfaz gráfica principal del visualizador A*
"""
import tkinter as tk
from tkinter import messagebox, ttk
from constantes import (CELDA_SIZE, MAX_FILAS, MAX_COLUMNAS, FILAS_DEFAULT, 
                       COLUMNAS_DEFAULT, COLORES, COSTO_HORIZONTAL_DEFAULT,
                       COSTO_VERTICAL_DEFAULT, COSTO_DIAGONAL_DEFAULT,
                       PERMITIR_DIAGONAL_DEFAULT)
from celda_widget import CeldaWidget
from algoritmo_astar import AlgoritmoAStar
from funciones_astar import reconstruir_camino


class InterfazAStar:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Algoritmo A* - Configuración Avanzada")
        
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
        
        # Configuración de costos
        self.costo_horizontal = tk.DoubleVar(value=COSTO_HORIZONTAL_DEFAULT)
        self.costo_vertical = tk.DoubleVar(value=COSTO_VERTICAL_DEFAULT)
        self.costo_diagonal = tk.DoubleVar(value=COSTO_DIAGONAL_DEFAULT)
        self.permitir_diagonal = tk.BooleanVar(value=PERMITIR_DIAGONAL_DEFAULT)
        self.tipo_heuristica = tk.StringVar(value='manhattan')
        
        # Algoritmo
        self.algoritmo = None
        self.paso_actual = 0
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea toda la interfaz gráfica con layout horizontal"""
        
        # ===== FRAME PRINCIPAL CON DOS COLUMNAS =====
        # Columna izquierda: Canvas (cuadrícula)
        # Columna derecha: Controles
        
        # Frame izquierdo para el canvas
        self.frame_izquierdo = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(self.frame_izquierdo, text="🎮 Área de Juego",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Frame para el canvas
        self.frame_canvas = tk.Frame(self.frame_izquierdo, bg='white')
        self.frame_canvas.pack(pady=10, expand=True)
        
        # Mensaje inicial
        self.label_canvas_vacio = tk.Label(self.frame_canvas,
                                          text="👆 Configura y crea una cuadrícula\npara comenzar",
                                          font=('Arial', 12), fg='gray', bg='white')
        self.label_canvas_vacio.pack(pady=50)
        
        # Frame derecho para controles (con scroll)
        self.frame_derecho = tk.Frame(self.root, bg='#f5f5f5', width=450)
        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        self.frame_derecho.pack_propagate(False)  # Mantener ancho fijo
        
        # Canvas con scrollbar para los controles
        canvas_controles = tk.Canvas(self.frame_derecho, bg='#f5f5f5', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_derecho, orient="vertical", command=canvas_controles.yview)
        self.frame_controles_scroll = tk.Frame(canvas_controles, bg='#f5f5f5')
        
        self.frame_controles_scroll.bind(
            "<Configure>",
            lambda e: canvas_controles.configure(scrollregion=canvas_controles.bbox("all"))
        )
        
        canvas_controles.create_window((0, 0), window=self.frame_controles_scroll, anchor="nw")
        canvas_controles.configure(yscrollcommand=scrollbar.set)
        
        canvas_controles.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título de controles
        tk.Label(self.frame_controles_scroll, text="⚙️ Panel de Control",
                font=('Arial', 16, 'bold'), bg='#f5f5f5').pack(pady=10)
        
        # Crear todos los frames de control
        self.crear_frame_configuracion()
        self.crear_frame_costos()
        self.crear_frame_modos()
        self.crear_frame_acciones()
        self.crear_frame_leyenda()
        self.crear_frame_info()
    
    def crear_frame_configuracion(self):
        """Crea el frame de configuración"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="🔧 Configuración de Cuadrícula", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=5)
        
        # Sub-frame para inputs
        frame_inputs = tk.Frame(frame, bg='white')
        frame_inputs.pack(pady=5)
        
        tk.Label(frame_inputs, text="Filas:", bg='white', font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_filas = tk.Entry(frame_inputs, width=8, font=('Arial', 10))
        self.entry_filas.grid(row=0, column=1, padx=5, pady=5)
        self.entry_filas.insert(0, str(FILAS_DEFAULT))
        
        tk.Label(frame_inputs, text="Columnas:", bg='white', font=('Arial', 10)).grid(row=0, column=2, padx=5, pady=5)
        self.entry_columnas = tk.Entry(frame_inputs, width=8, font=('Arial', 10))
        self.entry_columnas.grid(row=0, column=3, padx=5, pady=5)
        self.entry_columnas.insert(0, str(COLUMNAS_DEFAULT))
        
        tk.Button(frame, text="✨ Crear Cuadrícula", 
                 command=self.crear_cuadricula,
                 bg='#4CAF50', fg='white',
                 font=('Arial', 11, 'bold'),
                 width=30, height=2).pack(pady=10)
    
    def crear_frame_costos(self):
        """Crea el frame de configuración de costos"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='#e3f2fd')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="📏 Distancias y Costos", 
                font=('Arial', 12, 'bold'), bg='#e3f2fd').pack(pady=5)
        
        # Costo Horizontal
        frame_h = tk.Frame(frame, bg='#e3f2fd')
        frame_h.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(frame_h, text="Horizontal (←→):", bg='#e3f2fd',
                font=('Arial', 10, 'bold'), width=18, anchor='w').pack(side=tk.LEFT)
        tk.Entry(frame_h, textvariable=self.costo_horizontal, width=10,
                font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Costo Vertical
        frame_v = tk.Frame(frame, bg='#e3f2fd')
        frame_v.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(frame_v, text="Vertical (↑↓):", bg='#e3f2fd',
                font=('Arial', 10, 'bold'), width=18, anchor='w').pack(side=tk.LEFT)
        tk.Entry(frame_v, textvariable=self.costo_vertical, width=10,
                font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Costo Diagonal
        frame_d = tk.Frame(frame, bg='#e3f2fd')
        frame_d.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(frame_d, text="Diagonal (↗↘):", bg='#e3f2fd',
                font=('Arial', 10, 'bold'), width=18, anchor='w').pack(side=tk.LEFT)
        tk.Entry(frame_d, textvariable=self.costo_diagonal, width=10,
                font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Checkbox diagonal
        tk.Checkbutton(frame, text="✓ Permitir movimientos diagonales", 
                      variable=self.permitir_diagonal,
                      bg='#e3f2fd', font=('Arial', 10, 'bold'),
                      command=self.actualizar_heuristica_recomendada).pack(pady=8)
        
        # Tipo de heurística
        frame_heur = tk.Frame(frame, bg='#e3f2fd')
        frame_heur.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(frame_heur, text="Heurística:", bg='#e3f2fd',
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        heuristicas = ['manhattan', 'euclidiana', 'octile', 'chebyshev']
        combo_heuristica = ttk.Combobox(frame_heur, textvariable=self.tipo_heuristica, 
                                       values=heuristicas, state='readonly', width=15)
        combo_heuristica.pack(side=tk.LEFT, padx=5)
        
        # Botones de ayuda
        frame_botones_ayuda = tk.Frame(frame, bg='#e3f2fd')
        frame_botones_ayuda.pack(pady=5)
        
        tk.Button(frame_botones_ayuda, text="❓ Info Heurísticas", 
                 command=self.mostrar_info_heuristicas,
                 bg='#fff9c4', font=('Arial', 9)).pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_botones_ayuda, text="📚 Restricciones", 
                 command=self.mostrar_restricciones_visuales,
                 bg='#FFC107', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=3)
        
        # Etiqueta de recomendación
        self.label_recomendacion = tk.Label(frame, text="", bg='#e3f2fd',
                                           font=('Arial', 9, 'italic'), fg='blue',
                                           wraplength=380)
        self.label_recomendacion.pack(pady=5)
        
        self.actualizar_heuristica_recomendada()
    
    def crear_frame_modos(self):
        """Crea el frame de selección de modos"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="🎨 Modo de Dibujo", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=5)
        
        self.botones_modo = {}
        modos = [
            ("🟢 Inicio", "inicio", COLORES['inicio']),
            ("🔴 Final", "fin", COLORES['fin']),
            ("⬛ Obstáculo", "obstaculo", COLORES['obstaculo']),
            ("🗑️ Borrar", "borrar", 'white')
        ]
        
        for texto, modo, color in modos:
            btn = tk.Button(frame, text=texto, width=25,
                          command=lambda m=modo: self.cambiar_modo(m),
                          bg=color, font=('Arial', 10, 'bold'), height=2)
            btn.pack(padx=10, pady=3)
            self.botones_modo[modo] = btn
        
        self.cambiar_modo("inicio")
    
    def crear_frame_acciones(self):
        """Crea el frame de botones de acción"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="🚀 Acciones", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=5)
        
        tk.Button(frame, text="▶ Ejecutar A*",
                 command=self.ejecutar_astar,
                 bg='#2196F3', fg='white',
                 font=('Arial', 11, 'bold'),
                 width=30, height=2).pack(padx=10, pady=3)
        
        tk.Button(frame, text="⏩ Paso a Paso",
                 command=self.ejecutar_paso_a_paso,
                 bg='#FF9800', fg='white',
                 font=('Arial', 11, 'bold'),
                 width=30, height=2).pack(padx=10, pady=3)
        
        tk.Button(frame, text="🔄 Limpiar Todo",
                 command=self.limpiar_todo,
                 bg='#9E9E9E', fg='white',
                 font=('Arial', 11, 'bold'),
                 width=30, height=2).pack(padx=10, pady=3)
    
    def crear_frame_leyenda(self):
        """Crea el frame de leyenda"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='#f0f0f0')
        frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame, text="📊 Leyenda",
                font=('Arial', 12, 'bold'),
                bg='#f0f0f0').pack(pady=5)
        
        leyenda = [
            ("G", "Costo desde inicio", "blue"),
            ("H", "Heurística al objetivo", "green"),
            ("F", "Costo total (F = G + H)", "red")
        ]
        
        for letra, desc, color in leyenda:
            item_frame = tk.Frame(frame, bg='#f0f0f0')
            item_frame.pack(anchor='w', padx=15, pady=3)
            
            tk.Label(item_frame, text=f"{letra}:", 
                    font=('Arial', 10, 'bold'),
                    fg=color, bg='#f0f0f0',
                    width=3).pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=desc,
                    font=('Arial', 9),
                    bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
    
    def crear_frame_info(self):
        """Crea el frame de información"""
        self.frame_info = tk.Frame(self.frame_controles_scroll, relief=tk.SUNKEN, 
                                   borderwidth=2, bg='#fff3e0')
        self.frame_info.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(self.frame_info, text="ℹ️ Información",
                font=('Arial', 11, 'bold'), bg='#fff3e0').pack(pady=5)
        
        self.label_info = tk.Label(self.frame_info,
                                   text="Configura las distancias y\ncrea una cuadrícula para comenzar",
                                   font=('Arial', 10),
                                   fg='#e65100', bg='#fff3e0',
                                   wraplength=380, justify=tk.LEFT)
        self.label_info.pack(pady=10, padx=10)
    
    def actualizar_heuristica_recomendada(self):
        """Actualiza la recomendación de heurística según el modo"""
        if self.permitir_diagonal.get():
            recomendacion = "💡 Recomendado: Heurística 'octile' para movimientos con diagonal"
            self.tipo_heuristica.set('octile')
        else:
            recomendacion = "💡 Recomendado: Heurística 'manhattan' para movimientos sin diagonal"
            self.tipo_heuristica.set('manhattan')
        
        self.label_recomendacion.config(text=recomendacion)
    
    def mostrar_info_heuristicas(self):
        """Muestra información sobre los tipos de heurísticas"""
        info = """
TIPOS DE HEURÍSTICAS:

🔹 Manhattan: Suma de diferencias absolutas (|dx| + |dy|)
   Mejor para: Movimientos solo horizontal/vertical (4 direcciones)
   
🔹 Euclidiana: Distancia en línea recta (√(dx² + dy²))
   Mejor para: Cuando se permite movimiento libre
   
🔹 Octile: Considera movimientos diagonales
   Mejor para: Movimientos en 8 direcciones (con diagonal)
   Fórmula: D·min(dx,dy) + D'·|dx-dy|
   
🔹 Chebyshev: Máximo de diferencias (max(|dx|, |dy|))
   Mejor para: Cuando diagonal tiene mismo costo que recto

NOTA: Una heurística admisible nunca sobreestima el costo real.
        """
        messagebox.showinfo("Información de Heurísticas", info)
    
    def mostrar_restricciones_visuales(self):
        """Muestra la ventana de restricciones diagonales"""
        from visualizador_restricciones import mostrar_restricciones_diagonales
        mostrar_restricciones_diagonales()
    
    def obtener_config_costos(self):
        """Obtiene la configuración actual de costos"""
        return {
            'horizontal': self.costo_horizontal.get(),
            'vertical': self.costo_vertical.get(),
            'diagonal': self.costo_diagonal.get()
        }
    
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
        
        # Ocultar mensaje inicial
        if self.label_canvas_vacio:
            self.label_canvas_vacio.destroy()
            self.label_canvas_vacio = None
        
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
                               bg='white', highlightthickness=2,
                               highlightbackground='#2196F3')
        self.canvas.pack()
        
        # Crear celdas
        for i in range(self.filas):
            for j in range(self.columnas):
                x = j * CELDA_SIZE
                y = i * CELDA_SIZE
                
                celda = CeldaWidget(self.canvas, x, y, CELDA_SIZE, i, j)
                celda.bind_click(self.click_celda)
                self.celdas[(i, j)] = celda
        
        self.label_info.config(text="✅ Cuadrícula creada!\nSelecciona inicio (verde) y fin (rojo)")
    
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
        
        # Obtener configuración
        config_costos = self.obtener_config_costos()
        permitir_diag = self.permitir_diagonal.get()
        tipo_h = self.tipo_heuristica.get()
        
        self.label_info.config(text=f"⏳ Ejecutando A* con {tipo_h}...")
        self.root.update()
        
        # Crear y ejecutar algoritmo
        self.algoritmo = AlgoritmoAStar(
            self.inicio, self.fin,
            self.filas, self.columnas,
            self.obstaculos,
            config_costos,
            permitir_diag,
            tipo_h
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
                    g = round(self.algoritmo.costo_g[vecino], 2)
                    h = round(self.algoritmo.costo_h[vecino], 2)
                    f = round(self.algoritmo.costo_f[vecino], 2)
                    
                    self.celdas[vecino].colorear('visitado')
                    self.celdas[vecino].actualizar_valores(g, h, f)
            
            self.root.update()
            
            if encontrado:
                # Mostrar camino
                camino = reconstruir_camino(self.algoritmo.vino_de, 
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = round(self.algoritmo.costo_g[self.fin], 2)
                self.label_info.config(
                    text=f"✅ Camino encontrado!\nCosto: {longitud} | Nodos: {paso}"
                )
                
                # Mostrar estadísticas detalladas
                estadisticas = f"""
¡Camino encontrado!

📊 Estadísticas:
- Costo total: {longitud}
- Nodos explorados: {paso}
- Longitud: {len(camino) + 1} nodos

⚙️ Configuración:
- Heurística: {tipo_h}
- Costo H: {config_costos['horizontal']}
- Costo V: {config_costos['vertical']}
- Costo D: {config_costos['diagonal']}
- Diagonal: {'Sí' if permitir_diag else 'No'}
                """
                messagebox.showinfo("¡Éxito!", estadisticas)
                return
    
    def ejecutar_paso_a_paso(self):
        """Ejecuta el algoritmo paso a paso"""
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        
        # Limpiar botones anteriores
        for widget in self.frame_info.winfo_children():
            if not isinstance(widget, tk.Label) or widget != self.label_info:
                widget.destroy()
        
        # Obtener configuración
        config_costos = self.obtener_config_costos()
        permitir_diag = self.permitir_diagonal.get()
        tipo_h = self.tipo_heuristica.get()
        
        # Crear algoritmo
        self.algoritmo = AlgoritmoAStar(
            self.inicio, self.fin,
            self.filas, self.columnas,
            self.obstaculos,
            config_costos,
            permitir_diag,
            tipo_h
        )
        
        self.paso_actual = 0
        
        def siguiente_paso():
            self.paso_actual += 1
            actual, vecinos, encontrado = self.algoritmo.ejecutar_paso()
            
            if actual is None:
                self.label_info.config(text="❌ No se encontró camino")
                messagebox.showerror("Error", "No se encontró un camino")
                btn_siguiente.destroy()
                return
            
            # Visualizar
            if actual != self.inicio and actual != self.fin:
                self.celdas[actual].colorear('visitado')
            
            for vecino in vecinos:
                if vecino != self.inicio and vecino != self.fin:
                    g = round(self.algoritmo.costo_g[vecino], 2)
                    h = round(self.algoritmo.costo_h[vecino], 2)
                    f = round(self.algoritmo.costo_f[vecino], 2)
                    
                    self.celdas[vecino].colorear('visitado')
                    self.celdas[vecino].actualizar_valores(g, h, f)
            
            if encontrado:
                camino = reconstruir_camino(self.algoritmo.vino_de,
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = round(self.algoritmo.costo_g[self.fin], 2)
                self.label_info.config(
                    text=f"✅ Camino encontrado!\nCosto: {longitud} | Pasos: {self.paso_actual}"
                )
                
                estadisticas = f"""
¡Encontrado en {self.paso_actual} pasos!

Costo total: {longitud}
Longitud: {len(camino) + 1} nodos
Heurística: {tipo_h}
                """
                messagebox.showinfo("¡Éxito!", estadisticas)
                btn_siguiente.destroy()
                return
            
            f_actual = round(self.algoritmo.costo_f.get(actual, 0), 2)
            self.label_info.config(
                text=f"Paso {self.paso_actual}:\nExplorando {actual}\nF = {f_actual}"
            )
        
        # Crear botón siguiente
        btn_siguiente = tk.Button(self.frame_info, text="▶ Siguiente Paso",
                                 command=siguiente_paso,
                                 bg='#4CAF50', fg='white',
                                 font=('Arial', 10, 'bold'),
                                 width=25, height=2)
        btn_siguiente.pack(pady=10)
        
        siguiente_paso()
    
    def validar_inicio_fin(self):
        """Valida que exista inicio y fin"""
        if not self.inicio:
            messagebox.showerror("Error", "Selecciona un punto de inicio (verde)")
            return False
        if not self.fin:
            messagebox.showerror("Error", "Selecciona un punto final (rojo)")
            return False
        
        # Validar costos
        try:
            h = self.costo_horizontal.get()
            v = self.costo_vertical.get()
            d = self.costo_diagonal.get()
            
            if h <= 0 or v <= 0 or d <= 0:
                messagebox.showerror("Error", "Los costos deben ser mayores a 0")
                return False
        except:
            messagebox.showerror("Error", "Los costos deben ser números válidos")
            return False
        
        return True
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda anterior"""
        for pos, celda in self.celdas.items():
            if pos not in self.obstaculos and pos != self.inicio and pos != self.fin:
                celda.colorear('vacio')
                celda.limpiar_valores()
        
        # Limpiar botones del frame_info excepto etiquetas
        for widget in self.frame_info.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
    
    def limpiar_todo(self):
        """Limpia todo el tablero"""
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        
        for celda in self.celdas.values():
            celda.colorear('vacio')
            celda.limpiar_valores()
        
        # Limpiar botones del frame_info
        for widget in self.frame_info.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self.label_info.config(text="🧹 Todo limpio.\nListo para empezar")