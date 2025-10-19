"""
Interfaz gráfica principal del visualizador A* - Con Lista Abierta y Cerrada
"""
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import time
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
        self.root.title("Visualizador A* - Con Lista Abierta/Cerrada")
        self.root.geometry("1600x900")
        
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
        
        # Velocidad
        self.velocidad_ms = tk.IntVar(value=300)
        
        # Algoritmo
        self.algoritmo = None
        self.paso_actual = 0
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz con 3 paneles: Canvas, Controles, Listas"""
        
        # ===== PANEL IZQUIERDO: Canvas (40%) =====
        frame_izq = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, borderwidth=2)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_izq, text="🎮 Área de Juego",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=5)
        
        self.frame_canvas = tk.Frame(frame_izq, bg='white')
        self.frame_canvas.pack(pady=10, expand=True)
        
        self.label_canvas_vacio = tk.Label(self.frame_canvas,
                                          text="👆 Crea una cuadrícula para comenzar",
                                          font=('Arial', 12), fg='gray', bg='white')
        self.label_canvas_vacio.pack(pady=50)
        
        # ===== PANEL CENTRAL: Controles (25%) =====
        frame_centro = tk.Frame(self.root, bg='#f5f5f5', width=400)
        frame_centro.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        frame_centro.pack_propagate(False)
        
        # Canvas con scrollbar para controles
        canvas_ctrl = tk.Canvas(frame_centro, bg='#f5f5f5', highlightthickness=0)
        scrollbar_ctrl = tk.Scrollbar(frame_centro, orient="vertical", command=canvas_ctrl.yview)
        self.frame_controles_scroll = tk.Frame(canvas_ctrl, bg='#f5f5f5')
        
        self.frame_controles_scroll.bind(
            "<Configure>",
            lambda e: canvas_ctrl.configure(scrollregion=canvas_ctrl.bbox("all"))
        )
        
        canvas_ctrl.create_window((0, 0), window=self.frame_controles_scroll, anchor="nw")
        canvas_ctrl.configure(yscrollcommand=scrollbar_ctrl.set)
        
        canvas_ctrl.pack(side="left", fill="both", expand=True)
        scrollbar_ctrl.pack(side="right", fill="y")
        
        tk.Label(self.frame_controles_scroll, text="⚙️ Panel de Control",
                font=('Arial', 14, 'bold'), bg='#f5f5f5').pack(pady=5)
        
        self.crear_frame_configuracion()
        self.crear_frame_costos()
        self.crear_frame_velocidad()
        self.crear_frame_modos()
        self.crear_frame_acciones()
        self.crear_frame_leyenda()
        self.crear_frame_info()
        
        # ===== PANEL DERECHO: Listas (35%) =====
        frame_der = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, borderwidth=2)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_der, text="📊 Análisis del Algoritmo A*",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=5)
        
        # Notebook con pestañas
        self.notebook = ttk.Notebook(frame_der)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Lista Abierta
        self.crear_pestaña_lista_abierta()
        
        # Pestaña 2: Lista Cerrada
        self.crear_pestaña_lista_cerrada()
        
        # Pestaña 3: Resumen
        self.crear_pestaña_resumen()
    
    def crear_pestaña_lista_abierta(self):
        """Crea la pestaña de Lista Abierta"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text="📂 Lista Abierta")
        
        tk.Label(frame, text="Nodos pendientes de explorar",
                font=('Arial', 10, 'italic'), bg='white', fg='#2196F3').pack(pady=3)
        
        tk.Label(frame, text="(Ordenados por F de menor a mayor)",
                font=('Arial', 9), bg='white', fg='gray').pack()
        
        # Frame con cabecera
        header_frame = tk.Frame(frame, bg='#e3f2fd', relief=tk.RAISED, borderwidth=1)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(header_frame, text="Nodo", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', width=10).grid(row=0, column=0, padx=2)
        tk.Label(header_frame, text="G", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='blue', width=8).grid(row=0, column=1, padx=2)
        tk.Label(header_frame, text="H", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='green', width=8).grid(row=0, column=2, padx=2)
        tk.Label(header_frame, text="F=G+H", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='red', width=10).grid(row=0, column=3, padx=2)
        
        self.text_abierta = scrolledtext.ScrolledText(frame, width=50, height=30,
                                                       font=('Courier', 9), wrap=tk.WORD)
        self.text_abierta.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.label_count_abierta = tk.Label(frame, text="Total: 0 nodos",
                                            font=('Arial', 9, 'bold'),
                                            bg='white', fg='#2196F3')
        self.label_count_abierta.pack(pady=3)
    
    def crear_pestaña_lista_cerrada(self):
        """Crea la pestaña de Lista Cerrada"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text="📁 Lista Cerrada")
        
        tk.Label(frame, text="Nodos ya explorados",
                font=('Arial', 10, 'italic'), bg='white', fg='#4CAF50').pack(pady=3)
        
        tk.Label(frame, text="(Orden de exploración)",
                font=('Arial', 9), bg='white', fg='gray').pack()
        
        # Frame con cabecera
        header_frame = tk.Frame(frame, bg='#e8f5e9', relief=tk.RAISED, borderwidth=1)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(header_frame, text="#", font=('Arial', 9, 'bold'),
                bg='#e8f5e9', width=5).grid(row=0, column=0, padx=2)
        tk.Label(header_frame, text="Nodo", font=('Arial', 9, 'bold'),
                bg='#e8f5e9', width=10).grid(row=0, column=1, padx=2)
        tk.Label(header_frame, text="G", font=('Arial', 9, 'bold'),
                bg='#e8f5e9', fg='blue', width=7).grid(row=0, column=2, padx=2)
        tk.Label(header_frame, text="H", font=('Arial', 9, 'bold'),
                bg='#e8f5e9', fg='green', width=7).grid(row=0, column=3, padx=2)
        tk.Label(header_frame, text="F", font=('Arial', 9, 'bold'),
                bg='#e8f5e9', fg='red', width=7).grid(row=0, column=4, padx=2)
        
        self.text_cerrada = scrolledtext.ScrolledText(frame, width=50, height=30,
                                                       font=('Courier', 9), wrap=tk.WORD)
        self.text_cerrada.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.label_count_cerrada = tk.Label(frame, text="Total: 0 nodos",
                                            font=('Arial', 9, 'bold'),
                                            bg='white', fg='#4CAF50')
        self.label_count_cerrada.pack(pady=3)
    
    def crear_pestaña_resumen(self):
        """Crea la pestaña de resumen"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text="📈 Resumen")
        
        tk.Label(frame, text="Estadísticas y Análisis Completo",
                font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        self.text_resumen = scrolledtext.ScrolledText(frame, width=50, height=35,
                                                       font=('Courier', 9), wrap=tk.WORD)
        self.text_resumen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def crear_frame_configuracion(self):
        """Crea el frame de configuración"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="🔧 Configuración", 
                font=('Arial', 11, 'bold'), bg='white').pack(pady=3)
        
        f = tk.Frame(frame, bg='white')
        f.pack(pady=3)
        
        tk.Label(f, text="Filas:", bg='white').grid(row=0, column=0, padx=3)
        self.entry_filas = tk.Entry(f, width=6)
        self.entry_filas.grid(row=0, column=1, padx=3)
        self.entry_filas.insert(0, "6")
        
        tk.Label(f, text="Cols:", bg='white').grid(row=0, column=2, padx=3)
        self.entry_columnas = tk.Entry(f, width=6)
        self.entry_columnas.grid(row=0, column=3, padx=3)
        self.entry_columnas.insert(0, "8")
        
        tk.Button(frame, text="✨ Crear Cuadrícula", 
                 command=self.crear_cuadricula,
                 bg='#4CAF50', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=25, height=2).pack(pady=5)
    
    def crear_frame_costos(self):
        """Crea el frame de costos"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='#e3f2fd')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="📏 Distancias", 
                font=('Arial', 11, 'bold'), bg='#e3f2fd').pack(pady=3)
        
        for texto, var in [("Horizontal:", self.costo_horizontal),
                           ("Vertical:", self.costo_vertical),
                           ("Diagonal:", self.costo_diagonal)]:
            f = tk.Frame(frame, bg='#e3f2fd')
            f.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(f, text=texto, bg='#e3f2fd', width=10, anchor='w').pack(side=tk.LEFT)
            tk.Entry(f, textvariable=var, width=8).pack(side=tk.LEFT)
        
        tk.Checkbutton(frame, text="✓ Diagonal", 
                      variable=self.permitir_diagonal,
                      bg='#e3f2fd', font=('Arial', 9, 'bold'),
                      command=self.actualizar_heuristica_recomendada).pack(pady=3)
        
        f = tk.Frame(frame, bg='#e3f2fd')
        f.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(f, text="Heurística:", bg='#e3f2fd', font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        
        heuristicas = ['manhattan', 'euclidiana', 'octile', 'chebyshev']
        combo = ttk.Combobox(f, textvariable=self.tipo_heuristica, 
                            values=heuristicas, state='readonly', width=12)
        combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame, text="❓ Info", 
                 command=self.mostrar_info_heuristicas,
                 bg='#fff9c4', font=('Arial', 8)).pack(pady=3)
        
        self.label_recomendacion = tk.Label(frame, text="", bg='#e3f2fd',
                                           font=('Arial', 8, 'italic'), fg='blue',
                                           wraplength=350)
        self.label_recomendacion.pack(pady=3)
        
        self.actualizar_heuristica_recomendada()
    
    def crear_frame_velocidad(self):
        """Crea el frame de velocidad"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='#fff9c4')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="⚡ Velocidad", 
                font=('Arial', 11, 'bold'), bg='#fff9c4').pack(pady=3)
        
        for texto, valor in [("Rápido", 100), ("Normal", 300), ("Lento", 800)]:
            tk.Radiobutton(frame, text=texto, variable=self.velocidad_ms,
                          value=valor, bg='#fff9c4', font=('Arial', 9)).pack(anchor='w', padx=15)
    
    def crear_frame_modos(self):
        """Crea el frame de modos"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="🎨 Modo", 
                font=('Arial', 11, 'bold'), bg='white').pack(pady=3)
        
        self.botones_modo = {}
        for texto, modo, color in [("🟢 Inicio", "inicio", COLORES['inicio']),
                                    ("🔴 Final", "fin", COLORES['fin']),
                                    ("⬛ Obstáculo", "obstaculo", COLORES['obstaculo']),
                                    ("🗑️ Borrar", "borrar", 'white')]:
            btn = tk.Button(frame, text=texto, width=22,
                          command=lambda m=modo: self.cambiar_modo(m),
                          bg=color, font=('Arial', 9, 'bold'), height=1)
            btn.pack(padx=5, pady=2)
            self.botones_modo[modo] = btn
        
        self.cambiar_modo("inicio")
    
    def crear_frame_acciones(self):
        """Crea el frame de acciones"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='white')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="🚀 Acciones", 
                font=('Arial', 11, 'bold'), bg='white').pack(pady=3)
        
        tk.Button(frame, text="▶ Ejecutar A*",
                 command=self.ejecutar_astar,
                 bg='#2196F3', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=25, height=2).pack(padx=5, pady=2)
        
        tk.Button(frame, text="⏩ Paso a Paso",
                 command=self.ejecutar_paso_a_paso,
                 bg='#FF9800', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=25, height=2).pack(padx=5, pady=2)
        
        tk.Button(frame, text="🔄 Limpiar",
                 command=self.limpiar_todo,
                 bg='#9E9E9E', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=25, height=2).pack(padx=5, pady=2)
    
    def crear_frame_leyenda(self):
        """Crea el frame de leyenda"""
        frame = tk.Frame(self.frame_controles_scroll, relief=tk.RIDGE, borderwidth=2, bg='#f0f0f0')
        frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(frame, text="📊 Leyenda",
                font=('Arial', 11, 'bold'),
                bg='#f0f0f0').pack(pady=3)
        
        for letra, desc, color in [("G", "Costo desde inicio", "blue"),
                                   ("H", "Heurística", "green"),
                                   ("F", "F = G + H", "red")]:
            f = tk.Frame(frame, bg='#f0f0f0')
            f.pack(anchor='w', padx=10, pady=2)
            
            tk.Label(f, text=f"{letra}:", 
                    font=('Arial', 9, 'bold'),
                    fg=color, bg='#f0f0f0',
                    width=2).pack(side=tk.LEFT)
            
            tk.Label(f, text=desc,
                    font=('Arial', 8),
                    bg='#f0f0f0').pack(side=tk.LEFT, padx=3)
    
    def crear_frame_info(self):
        """Crea el frame de información"""
        self.frame_info = tk.Frame(self.frame_controles_scroll, relief=tk.SUNKEN, 
                                   borderwidth=2, bg='#fff3e0')
        self.frame_info.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(self.frame_info, text="ℹ️ Info",
                font=('Arial', 10, 'bold'), bg='#fff3e0').pack(pady=3)
        
        self.label_info = tk.Label(self.frame_info,
                                   text="Crea una cuadrícula",
                                   font=('Arial', 9),
                                   fg='#e65100', bg='#fff3e0',
                                   wraplength=350, justify=tk.LEFT)
        self.label_info.pack(pady=5, padx=5)
    
    def actualizar_listas(self):
        """Actualiza la visualización de las listas Abierta y Cerrada"""
        if not self.algoritmo:
            return
        
        # ===== LISTA ABIERTA =====
        self.text_abierta.delete('1.0', tk.END)
        
        # Obtener nodos de la frontera ordenados por F
        nodos_abierta = sorted(self.algoritmo.frontera, key=lambda x: x[0])
        
        for i, (f, _, nodo) in enumerate(nodos_abierta[:50], 1):  # Mostrar máximo 50
            g = self.algoritmo.costo_g.get(nodo, 0)
            h = self.algoritmo.costo_h.get(nodo, 0)
            
            linea = f"{i:2}. {str(nodo):10} | G:{g:5.1f} H:{h:5.1f} F:{f:5.1f}\n"
            self.text_abierta.insert(tk.END, linea)
        
        if len(nodos_abierta) > 50:
            self.text_abierta.insert(tk.END, f"\n... y {len(nodos_abierta) - 50} nodos más\n")
        
        self.label_count_abierta.config(text=f"Total: {len(nodos_abierta)} nodos")
        
        # ===== LISTA CERRADA =====
        self.text_cerrada.delete('1.0', tk.END)
        
        nodos_cerrados = list(self.algoritmo.cerrado)
        
        for i, nodo in enumerate(nodos_cerrados, 1):
            g = self.algoritmo.costo_g.get(nodo, 0)
            h = self.algoritmo.costo_h.get(nodo, 0)
            f = self.algoritmo.costo_f.get(nodo, 0)
            
            linea = f"#{i:3} {str(nodo):10} | G:{g:5.1f} H:{h:5.1f} F:{f:5.1f}\n"
            self.text_cerrada.insert(tk.END, linea)
        
        self.label_count_cerrada.config(text=f"Total: {len(nodos_cerrados)} nodos")
        
        # ===== RESUMEN =====
        self.text_resumen.delete('1.0', tk.END)
        
        resumen = f"""
{'='*60}
ANÁLISIS DEL ALGORITMO A*
{'='*60}

📊 ESTADO ACTUAL:
  • Nodos en Lista Abierta: {len(nodos_abierta)}
  • Nodos en Lista Cerrada: {len(nodos_cerrados)}
  • Paso actual: {self.paso_actual}

📂 PRÓXIMO A EXPLORAR:
"""
        if nodos_abierta:
            _, _, proximo = nodos_abierta[0]
            f_proximo = self.algoritmo.costo_f.get(proximo, 0)
            resumen += f"  Nodo: {proximo}\n  F: {f_proximo:.2f} (menor F de la frontera)\n"
        else:
            resumen += "  (Lista abierta vacía)\n"
        
        resumen += f"""
📁 ÚLTIMOS EXPLORADOS:
"""
        for nodo in list(nodos_cerrados)[-5:]:
            f_nodo = self.algoritmo.costo_f.get(nodo, 0)
            resumen += f"  {nodo}: F={f_nodo:.2f}\n"
        
        resumen += f"""
{'='*60}
EXPLICACIÓN:

A* mantiene dos listas:

📂 LISTA ABIERTA: Nodos pendientes de explorar
   • Ordenada por F (F = G + H)
   • Siempre se explora el de MENOR F
   • Es una cola de prioridad (heap)

📁 LISTA CERRADA: Nodos ya explorados
   • No se vuelven a explorar
   • Contiene el orden de exploración

En cada paso:
1. Extrae nodo con MENOR F de Lista Abierta
2. Lo mueve a Lista Cerrada
3. Explora TODOS sus vecinos
4. Agrega vecinos a Lista Abierta
5. Repite hasta encontrar el objetivo

{'='*60}
        """
        
        self.text_resumen.insert(tk.END, resumen)
    
    def actualizar_heuristica_recomendada(self):
        """Actualiza recomendación de heurística"""
        if self.permitir_diagonal.get():
            rec = "💡 Recomendado: 'octile' para diagonal"
            self.tipo_heuristica.set('octile')
        else:
            rec = "💡 Recomendado: 'manhattan' sin diagonal"
            self.tipo_heuristica.set('manhattan')
        
        self.label_recomendacion.config(text=rec)
    
    def mostrar_info_heuristicas(self):
        """Muestra información de heurísticas"""
        info = """
HEURÍSTICAS:

Manhattan: |dx| + |dy|
  Mejor para: 4 direcciones

Euclidiana: √(dx² + dy²)
  Mejor para: Movimiento libre

Octile: Considera diagonales
  Mejor para: 8 direcciones

Chebyshev: max(|dx|, |dy|)
  Mejor para: Diagonal = recto
        """
        messagebox.showinfo("Heurísticas", info)
    
    def mostrar_restricciones_visuales(self):
        """Muestra restricciones diagonales"""
        try:
            from visualizador_restricciones import mostrar_restricciones_diagonales
            mostrar_restricciones_diagonales()
        except:
            messagebox.showinfo("Info", "Módulo de restricciones no disponible")
    
    def obtener_config_costos(self):
        """Obtiene configuración de costos"""
        return {
            'horizontal': self.costo_horizontal.get(),
            'vertical': self.costo_vertical.get(),
            'diagonal': self.costo_diagonal.get()
        }
    
    def crear_cuadricula(self):
        """Crea la cuadrícula"""
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
            
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError
            
            if self.filas > MAX_FILAS or self.columnas > MAX_COLUMNAS:
                messagebox.showwarning("Advertencia",
                    f"Máximo {MAX_FILAS}x{MAX_COLUMNAS}")
                return
        
        except ValueError:
            messagebox.showerror("Error", "Números inválidos")
            return
        
        if self.label_canvas_vacio:
            self.label_canvas_vacio.destroy()
            self.label_canvas_vacio = None
        
        if self.canvas:
            self.canvas.destroy()
        
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        self.celdas = {}
        
        ancho = self.columnas * CELDA_SIZE
        alto = self.filas * CELDA_SIZE
        
        self.canvas = tk.Canvas(self.frame_canvas, width=ancho, height=alto,
                               bg='white', highlightthickness=2,
                               highlightbackground='#2196F3')
        self.canvas.pack()
        
        for i in range(self.filas):
            for j in range(self.columnas):
                x = j * CELDA_SIZE
                y = i * CELDA_SIZE
                
                celda = CeldaWidget(self.canvas, x, y, CELDA_SIZE, i, j)
                celda.bind_click(self.click_celda)
                self.celdas[(i, j)] = celda
        
        self.label_info.config(text="✅ Cuadrícula creada")
    
    def cambiar_modo(self, modo):
        """Cambia el modo de dibujo"""
        self.modo = modo
        for m, btn in self.botones_modo.items():
            if m == modo:
                btn.config(relief=tk.SUNKEN, borderwidth=4)
            else:
                btn.config(relief=tk.RAISED, borderwidth=2)
    
    def click_celda(self, fila, col):
        """Maneja click en celda"""
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
        """Ejecuta A* con animación y actualización de listas"""
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        
        config_costos = self.obtener_config_costos()
        permitir_diag = self.permitir_diagonal.get()
        tipo_h = self.tipo_heuristica.get()
        velocidad = self.velocidad_ms.get()
        
        self.label_info.config(text=f"⏳ Ejecutando A* con {tipo_h}...")
        self.root.update()
        
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
        
        while True:
            self.paso_actual += 1
            actual, vecinos, encontrado = self.algoritmo.ejecutar_paso()
            
            if actual is None:
                self.label_info.config(text="❌ No hay camino")
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
            
            # ACTUALIZAR LISTAS
            self.actualizar_listas()
            
            # Actualizar info
            f_actual = round(self.algoritmo.costo_f.get(actual, 0), 2)
            self.label_info.config(
                text=f"Paso {self.paso_actual}\nExplorando: {actual}\nF={f_actual}\nVecinos: {len(vecinos)}"
            )
            
            self.root.update()
            time.sleep(velocidad / 1000.0)
            
            if encontrado:
                camino = reconstruir_camino(self.algoritmo.vino_de, 
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = round(self.algoritmo.costo_g[self.fin], 2)
                
                self.label_info.config(
                    text=f"✅ ¡Camino encontrado!\nCosto: {longitud}\nPasos: {self.paso_actual}"
                )
                
                # Actualizar listas finales
                self.actualizar_listas()
                
                estadisticas = f"""
¡Camino encontrado!

📊 Estadísticas:
- Costo total: {longitud}
- Pasos: {self.paso_actual}
- Nodos explorados: {len(self.algoritmo.cerrado)}
- Longitud camino: {len(camino) + 1} nodos

⚙️ Configuración:
- Heurística: {tipo_h}
- Costos: H={config_costos['horizontal']}, V={config_costos['vertical']}, D={config_costos['diagonal']}
- Diagonal: {'Sí' if permitir_diag else 'No'}

💡 Revisa las pestañas "Lista Abierta" y "Lista Cerrada"
   para ver cómo trabajó el algoritmo.
                """
                messagebox.showinfo("¡Éxito!", estadisticas)
                return
    
    def ejecutar_paso_a_paso(self):
        """Ejecuta A* paso a paso con actualización de listas"""
        if not self.validar_inicio_fin():
            return
        
        self.limpiar_busqueda()
        
        # Limpiar botones anteriores
        for widget in self.frame_info.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
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
        
        # Actualizar listas iniciales
        self.actualizar_listas()
        
        def siguiente_paso():
            self.paso_actual += 1
            actual, vecinos, encontrado = self.algoritmo.ejecutar_paso()
            
            if actual is None:
                self.label_info.config(text="❌ No hay camino")
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
            
            # ACTUALIZAR LISTAS
            self.actualizar_listas()
            
            if encontrado:
                camino = reconstruir_camino(self.algoritmo.vino_de,
                                           self.inicio, self.fin)
                
                for nodo in camino:
                    self.celdas[nodo].colorear('camino')
                
                longitud = round(self.algoritmo.costo_g[self.fin], 2)
                
                self.label_info.config(
                    text=f"✅ ¡Encontrado!\nCosto: {longitud}\nPasos: {self.paso_actual}"
                )
                
                messagebox.showinfo("¡Éxito!",
                    f"Camino encontrado en {self.paso_actual} pasos!\n\nCosto: {longitud}")
                btn_siguiente.destroy()
                return
            
            f_actual = round(self.algoritmo.costo_f.get(actual, 0), 2)
            
            info_text = f"""Paso {self.paso_actual}
Explorando: {actual}
F = {f_actual}
Vecinos: {len(vecinos)}

Ver listas →"""
            
            self.label_info.config(text=info_text)
        
        # Crear botón siguiente
        btn_siguiente = tk.Button(self.frame_info, text="▶ Siguiente Paso",
                                 command=siguiente_paso,
                                 bg='#4CAF50', fg='white',
                                 font=('Arial', 10, 'bold'),
                                 width=22, height=2)
        btn_siguiente.pack(pady=5)
        
        self.label_info.config(text="🎮 Modo Paso a Paso\nClick 'Siguiente Paso'")
    
    def validar_inicio_fin(self):
        """Valida inicio y fin"""
        if not self.inicio:
            messagebox.showerror("Error", "Selecciona punto de inicio")
            return False
        if not self.fin:
            messagebox.showerror("Error", "Selecciona punto final")
            return False
        
        try:
            h = self.costo_horizontal.get()
            v = self.costo_vertical.get()
            d = self.costo_diagonal.get()
            
            if h <= 0 or v <= 0 or d <= 0:
                messagebox.showerror("Error", "Costos > 0")
                return False
        except:
            messagebox.showerror("Error", "Costos inválidos")
            return False
        
        return True
    
    def limpiar_busqueda(self):
        """Limpia búsqueda anterior"""
        for pos, celda in self.celdas.items():
            if pos not in self.obstaculos and pos != self.inicio and pos != self.fin:
                celda.colorear('vacio')
                celda.limpiar_valores()
        
        for widget in self.frame_info.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        # Limpiar listas
        self.text_abierta.delete('1.0', tk.END)
        self.text_cerrada.delete('1.0', tk.END)
        self.text_resumen.delete('1.0', tk.END)
        self.label_count_abierta.config(text="Total: 0 nodos")
        self.label_count_cerrada.config(text="Total: 0 nodos")
    
    def limpiar_todo(self):
        """Limpia todo"""
        self.inicio = None
        self.fin = None
        self.obstaculos = set()
        
        for celda in self.celdas.values():
            celda.colorear('vacio')
            celda.limpiar_valores()
        
        for widget in self.frame_info.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self.label_info.config(text="🧹 Todo limpio")
        
        # Limpiar listas
        self.text_abierta.delete('1.0', tk.END)
        self.text_cerrada.delete('1.0', tk.END)
        self.text_resumen.delete('1.0', tk.END)
        self.label_count_abierta.config(text="Total: 0 nodos")
        self.label_count_cerrada.config(text="Total: 0 nodos")