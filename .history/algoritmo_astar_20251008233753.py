"""
Implementación completa del algoritmo A*

FUNCIONAMIENTO:
1. Se inicia con el nodo inicial en la frontera
2. Se exploran TODOS los vecinos del nodo actual
3. Para cada vecino:
   - Se calcula G (costo acumulado desde inicio)
   - Se calcula H (heurística al objetivo)
   - Se calcula F = G + H
   - Se agrega a la frontera con prioridad F
4. La frontera (heap) automáticamente ordena por F menor
5. Se extrae siempre el nodo con menor F
6. Se repite hasta encontrar el objetivo

IMPORTANTE: El algoritmo NO decide moverse solo horizontal/vertical.
Explora TODOS los vecinos disponibles y la estructura heap decide
cuál explorar según el menor F.
"""
import heapq
from funciones_astar import (
    calcular_peso_movimiento,
    calcular_heuristica,
    calcular_funcion_costo,
    obtener_vecinos,
    reconstruir_camino
)


class AlgoritmoAStar:
    def __init__(self, inicio, fin, filas, columnas, obstaculos, 
                 config_costos, permitir_diagonal=False, tipo_heuristica='manhattan'):
        self.inicio = inicio
        self.fin = fin
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = obstaculos
        self.config_costos = config_costos
        self.permitir_diagonal = permitir_diagonal
        self.tipo_heuristica = tipo_heuristica
        
        # Estructuras de datos
        self.frontera = []  # Cola de prioridad (heap) - ordena automáticamente por F
        self.vino_de = {}   # Para reconstruir el camino
        self.costo_g = {}   # Costo acumulado desde inicio
        self.costo_h = {}   # Heurística (estimación al objetivo)
        self.costo_f = {}   # Función de costo total (F = G + H)
        self.cerrado = set()  # Nodos ya explorados completamente
        
        # Contador para desempate cuando F es igual
        self.contador = 0
        
        # Inicializar
        self.inicializar()
    
    def inicializar(self):
        """Inicializa las estructuras del algoritmo"""
        # Inicializar nodo de inicio
        self.costo_g[self.inicio] = 0
        self.costo_h[self.inicio] = calcular_heuristica(
            self.inicio, self.fin, self.config_costos, self.tipo_heuristica
        )
        self.costo_f[self.inicio] = calcular_funcion_costo(
            self.costo_g[self.inicio],
            self.costo_h[self.inicio]
        )
        
        # Agregar a la frontera con prioridad F
        # Formato: (F, contador, nodo)
        # El contador evita errores cuando F es igual
        heapq.heappush(self.frontera, (self.costo_f[self.inicio], self.contador, self.inicio))
        self.contador += 1
    
    def ejecutar_paso(self):
        """
        Ejecuta un paso del algoritmo A*
        
        PROCESO:
        1. Extrae el nodo con menor F de la frontera
        2. Si es el objetivo, termina
        3. Si no, explora TODOS sus vecinos:
           - Calcula G, H, F para cada vecino
           - Si el vecino es nuevo o encontramos un camino mejor:
             * Actualiza sus costos
             * Lo agrega a la frontera
        4. La frontera mantiene automáticamente el orden por F
        
        Returns:
            tuple: (nodo_actual, vecinos_explorados, encontrado)
        """
        if not self.frontera:
            return None, [], False
        
        # Extraer el nodo con menor F de la frontera
        _, _, actual = heapq.heappop(self.frontera)
        
        # Si ya lo exploramos, saltar
        if actual in self.cerrado:
            return actual, [], False
        
        # Marcar como explorado
        self.cerrado.add(actual)
        
        # ¿Llegamos al objetivo?
        if actual == self.fin:
            return actual, [], True
        
        vecinos_explorados = []
        
        # EXPLORAR TODOS LOS VECINOS DISPONIBLES
        vecinos = obtener_vecinos(
            actual, self.filas, self.columnas, 
            self.obstaculos, self.permitir_diagonal
        )
        
        for vecino in vecinos:
            # Si ya exploramos este vecino completamente, saltarlo
            if vecino in self.cerrado:
                continue
            
            # Calcular el costo G para llegar a este vecino desde actual
            peso = calcular_peso_movimiento(actual, vecino, self.config_costos)
            nuevo_costo_g = self.costo_g[actual] + peso
            
            # Si es un vecino nuevo O encontramos un camino mejor
            if vecino not in self.costo_g or nuevo_costo_g < self.costo_g[vecino]:
                # Actualizar costos
                self.costo_g[vecino] = nuevo_costo_g
                
                # Calcular heurística H
                self.costo_h[vecino] = calcular_heuristica(
                    vecino, self.fin, self.config_costos, self.tipo_heuristica
                )
                
                # Calcular función de costo F = G + H
                self.costo_f[vecino] = calcular_funcion_costo(
                    self.costo_g[vecino],
                    self.costo_h[vecino]
                )
                
                # Agregar a la frontera con prioridad F
                # El heap ordenará automáticamente por F menor
                heapq.heappush(
                    self.frontera, 
                    (self.costo_f[vecino], self.contador, vecino)
                )
                self.contador += 1
                
                # Guardar de dónde venimos (para reconstruir camino)
                self.vino_de[vecino] = actual
                
                # Agregar a la lista de vecinos explorados (para visualización)
                vecinos_explorados.append(vecino)
        
        return actual, vecinos_explorados, False
    
    def ejecutar_completo(self):
        """
        Ejecuta el algoritmo completo
        
        Returns:
            tuple: (exito, camino, nodos_explorados, costos)
        """
        nodos_explorados = 0
        
        while self.frontera:
            actual, vecinos, encontrado = self.ejecutar_paso()
            
            if actual is None:
                return False, [], nodos_explorados, {}
            
            nodos_explorados += 1
            
            if encontrado:
                camino = reconstruir_camino(self.vino_de, self.inicio, self.fin)
                costos = {
                    'g': self.costo_g,
                    'h': self.costo_h,
                    'f': self.costo_f
                }
                return True, camino, nodos_explorados, costos
        
        return False, [], nodos_explorados, {}
    
    def obtener_info_frontera(self):
        """
        Obtiene información sobre el estado actual de la frontera
        
        Returns:
            list: Lista de tuplas (nodo, F) ordenadas por F
        """
        info = [(nodo, f) for f, _, nodo in self.frontera]
        info.sort(key=lambda x: x[1])  # Ordenar por F
        return info