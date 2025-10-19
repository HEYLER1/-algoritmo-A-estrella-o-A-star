"""
Implementación completa del algoritmo A*
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
    def __init__(self, inicio, fin, filas, columnas, obstaculos):
        self.inicio = inicio
        self.fin = fin
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = obstaculos
        
        # Estructuras de datos
        self.frontera = []
        self.vino_de = {}
        self.costo_g = {}
        self.costo_h = {}
        self.costo_f = {}
        
        # Inicializar
        self.inicializar()
    
    def inicializar(self):
        """Inicializa las estructuras del algoritmo"""
        self.costo_g[self.inicio] = 0
        self.costo_h[self.inicio] = calcular_heuristica(self.inicio, self.fin)
        self.costo_f[self.inicio] = calcular_funcion_costo(
            self.costo_g[self.inicio],
            self.costo_h[self.inicio]
        )
        heapq.heappush(self.frontera, (self.costo_f[self.inicio], self.inicio))
    
    def ejecutar_paso(self):
        """
        Ejecuta un paso del algoritmo A*
        
        Returns:
            tuple: (nodo_actual, vecinos_explorados, encontrado)
        """
        if not self.frontera:
            return None, [], False
        
        _, actual = heapq.heappop(self.frontera)
        
        if actual == self.fin:
            return actual, [], True
        
        vecinos_explorados = []
        
        for vecino in obtener_vecinos(actual, self.filas, self.columnas, self.obstaculos):
            peso = calcular_peso_movimiento(actual, vecino)
            nuevo_costo_g = self.costo_g[actual] + peso
            
            if vecino not in self.costo_g or nuevo_costo_g < self.costo_g[vecino]:
                # Actualizar costos
                self.costo_g[vecino] = nuevo_costo_g
                self.costo_h[vecino] = calcular_heuristica(vecino, self.fin)
                self.costo_f[vecino] = calcular_funcion_costo(
                    self.costo_g[vecino],
                    self.costo_h[vecino]
                )
                
                # Agregar a frontera
                heapq.heappush(self.frontera, (self.costo_f[vecino], vecino))
                self.vino_de[vecino] = actual
                
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