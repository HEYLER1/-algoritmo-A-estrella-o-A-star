"""
Implementación completa del algoritmo A*

FUNCIONAMIENTO CORRECTO:
1. Extrae el nodo con menor F de la frontera
2. Explora TODOS sus vecinos válidos
3. Para cada vecino:
   - Calcula G (costo acumulado)
   - Calcula H (heurística)
   - Calcula F = G + H
   - Lo agrega/actualiza en la frontera
4. Repite hasta encontrar el objetivo
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
        """
        Inicializa el algoritmo A*
        
        Args:
            inicio: Tupla (fila, col) del nodo inicial
            fin: Tupla (fila, col) del nodo objetivo
            filas: Número de filas de la cuadrícula
            columnas: Número de columnas de la cuadrícula
            obstaculos: Set de tuplas con posiciones bloqueadas
            config_costos: Dict con costos {'horizontal', 'vertical', 'diagonal'}
            permitir_diagonal: Si True, permite movimientos en 8 direcciones
            tipo_heuristica: Tipo de heurística a usar
        """
        self.inicio = inicio
        self.fin = fin
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = obstaculos
        self.config_costos = config_costos
        self.permitir_diagonal = permitir_diagonal
        self.tipo_heuristica = tipo_heuristica
        
        # Estructuras de datos principales
        self.frontera = []           # Cola de prioridad (heap) - ordena por F
        self.vino_de = {}           # Para reconstruir el camino
        self.costo_g = {}           # Costo acumulado desde inicio (G)
        self.costo_h = {}           # Heurística (H)
        self.costo_f = {}           # Función de costo total (F = G + H)
        self.cerrado = set()        # Nodos ya completamente explorados
        
        # Contador para desempate en el heap
        self.contador = 0
        
        # Estadísticas
        self.nodos_explorados = 0
        self.vecinos_totales_evaluados = 0
        
        # Inicializar
        self.inicializar()
    
    def inicializar(self):
        """Inicializa el nodo de inicio en todas las estructuras"""
        # Calcular costos del nodo inicial
        self.costo_g[self.inicio] = 0
        self.costo_h[self.inicio] = calcular_heuristica(
            self.inicio, self.fin, self.config_costos, self.tipo_heuristica
        )
        self.costo_f[self.inicio] = calcular_funcion_costo(
            self.costo_g[self.inicio],
            self.costo_h[self.inicio]
        )
        
        # Agregar a la frontera
        # Formato: (F, contador, nodo)
        heapq.heappush(self.frontera, (
            self.costo_f[self.inicio], 
            self.contador, 
            self.inicio
        ))
        self.contador += 1
    
    def ejecutar_paso(self):
        """
        Ejecuta UN PASO del algoritmo A*
        
        PROCESO DETALLADO:
        1. Extrae el nodo con menor F de la frontera
        2. Si ya fue explorado, lo salta
        3. Lo marca como explorado (cerrado)
        4. Si es el objetivo, termina
        5. Obtiene TODOS sus vecinos válidos
        6. Para CADA vecino:
           a) Si ya fue explorado, lo salta
           b) Calcula el nuevo costo G
           c) Si es un vecino nuevo O encontró un camino mejor:
              - Actualiza G, H, F
              - Lo agrega a la frontera
              - Guarda de dónde vino
        
        Returns:
            tuple: (nodo_actual, lista_vecinos_explorados, encontrado)
                  - nodo_actual: El nodo que se exploró en este paso
                  - lista_vecinos_explorados: Vecinos que se agregaron/actualizaron
                  - encontrado: True si llegamos al objetivo
        """
        
        # Verificar que haya nodos en la frontera
        if not self.frontera:
            return None, [], False
        
        # 1. EXTRAER el nodo con menor F de la frontera
        f_actual, _, actual = heapq.heappop(self.frontera)
        
        # 2. Si ya lo exploramos completamente, saltarlo
        if actual in self.cerrado:
            # Esto puede pasar si agregamos el mismo nodo múltiples veces
            # con diferentes valores de F
            return self.ejecutar_paso()  # Recursión para obtener el siguiente
        
        # 3. MARCAR como explorado
        self.cerrado.add(actual)
        self.nodos_explorados += 1
        
        # 4. ¿Llegamos al objetivo?
        if actual == self.fin:
            return actual, [], True
        
        # 5. OBTENER TODOS LOS VECINOS VÁLIDOS
        vecinos = obtener_vecinos(
            actual, 
            self.filas, 
            self.columnas, 
            self.obstaculos, 
            self.permitir_diagonal
        )
        
        # Lista para retornar los vecinos que se exploraron en este paso
        vecinos_explorados = []
        
        # 6. EXPLORAR CADA VECINO
        for vecino in vecinos:
            # 6a. Si ya exploramos este vecino completamente, saltarlo
            if vecino in self.cerrado:
                continue
            
            # 6b. CALCULAR el nuevo costo G para este vecino
            # G = costo acumulado del nodo actual + peso del movimiento
            peso_movimiento = calcular_peso_movimiento(
                actual, vecino, self.config_costos
            )
            nuevo_costo_g = self.costo_g[actual] + peso_movimiento
            
            # 6c. ¿Es un vecino nuevo O encontramos un camino mejor?
            es_nuevo = vecino not in self.costo_g
            es_mejor_camino = not es_nuevo and nuevo_costo_g < self.costo_g[vecino]
            
            if es_nuevo or es_mejor_camino:
                # ACTUALIZAR costos
                self.costo_g[vecino] = nuevo_costo_g
                
                # CALCULAR heurística H
                self.costo_h[vecino] = calcular_heuristica(
                    vecino, self.fin, self.config_costos, self.tipo_heuristica
                )
                
                # CALCULAR función de costo F = G + H
                self.costo_f[vecino] = calcular_funcion_costo(
                    self.costo_g[vecino],
                    self.costo_h[vecino]
                )
                
                # AGREGAR a la frontera con prioridad F
                # El heap automáticamente mantiene el orden por F menor
                heapq.heappush(
                    self.frontera,
                    (self.costo_f[vecino], self.contador, vecino)
                )
                self.contador += 1
                
                # GUARDAR de dónde venimos (para reconstruir el camino)
                self.vino_de[vecino] = actual
                
                # AGREGAR a la lista de vecinos explorados (para visualización)
                vecinos_explorados.append(vecino)
                
                # Incrementar estadística
                self.vecinos_totales_evaluados += 1
        
        # Retornar información del paso
        return actual, vecinos_explorados, False
    
    def ejecutar_completo(self):
        """
        Ejecuta el algoritmo completo hasta encontrar el camino
        
        Returns:
            tuple: (exito, camino, nodos_explorados, costos)
        """
        while self.frontera:
            actual, vecinos, encontrado = self.ejecutar_paso()
            
            if actual is None:
                # No hay camino posible
                return False, [], self.nodos_explorados, {}
            
            if encontrado:
                # ¡Éxito! Reconstruir el camino
                camino = reconstruir_camino(self.vino_de, self.inicio, self.fin)
                costos = {
                    'g': self.costo_g,
                    'h': self.costo_h,
                    'f': self.costo_f
                }
                return True, camino, self.nodos_explorados, costos
        
        # La frontera se vació sin encontrar el objetivo
        return False, [], self.nodos_explorados, {}
    
    def obtener_info_frontera(self, limite=10):
        """
        Obtiene información sobre los primeros nodos en la frontera
        
        Args:
            limite: Número máximo de nodos a retornar
        
        Returns:
            list: Lista de tuplas (nodo, F, G, H) ordenadas por F
        """
        info = []
        for f, _, nodo in sorted(self.frontera)[:limite]:
            g = self.costo_g.get(nodo, 0)
            h = self.costo_h.get(nodo, 0)
            info.append((nodo, f, g, h))
        return info
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del estado actual del algoritmo
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            'nodos_explorados': self.nodos_explorados,
            'nodos_en_frontera': len(self.frontera),
            'nodos_cerrados': len(self.cerrado),
            'vecinos_evaluados': self.vecinos_totales_evaluados,
            'costo_g_objetivo': self.costo_g.get(self.fin, None)
        }
    
    def verificar_consistencia(self):
        """
        Verifica la consistencia de las estructuras de datos
        Útil para debugging
        
        Returns:
            tuple: (es_consistente, mensajes_error)
        """
        errores = []
        
        # Verificar que todos los nodos en costo_g tengan costo_h y costo_f
        for nodo in self.costo_g:
            if nodo not in self.costo_h:
                errores.append(f"Nodo {nodo} tiene G pero no H")
            if nodo not in self.costo_f:
                errores.append(f"Nodo {nodo} tiene G pero no F")
        
        # Verificar que F = G + H
        for nodo in self.costo_f:
            if nodo in self.costo_g and nodo in self.costo_h:
                f_calculado = self.costo_g[nodo] + self.costo_h[nodo]
                f_guardado = self.costo_f[nodo]
                if abs(f_calculado - f_guardado) > 0.001:  # Tolerancia para flotantes
                    errores.append(
                        f"Nodo {nodo}: F inconsistente. "
                        f"Guardado={f_guardado}, Calculado={f_calculado}"
                    )
        
        # Verificar que los nodos cerrados no estén en la frontera
        nodos_frontera = {nodo for _, _, nodo in self.frontera}
        nodos_en_ambos = self.cerrado.intersection(nodos_frontera)
        if nodos_en_ambos:
            errores.append(f"Nodos en cerrado Y frontera: {nodos_en_ambos}")
        
        return len(errores) == 0, errores


# ============== FUNCIÓN DE PRUEBA ==============
def test_algoritmo():
    """
    Función de prueba para verificar que el algoritmo explora correctamente
    """
    print("="*70)
    print("PRUEBA DEL ALGORITMO A*")
    print("="*70)
    
    # Configuración simple
    inicio = (0, 0)
    fin = (3, 3)
    filas = 4
    columnas = 4
    obstaculos = {(1, 1), (1, 2), (2, 1)}  # Algunos obstáculos
    config_costos = {'horizontal': 1.0, 'vertical': 1.0, 'diagonal': 1.4}
    
    print(f"\nConfiguración:")
    print(f"  Inicio: {inicio}")
    print(f"  Fin: {fin}")
    print(f"  Tamaño: {filas}x{columnas}")
    print(f"  Obstáculos: {obstaculos}")
    print(f"  Diagonal: Sí")
    
    # Crear algoritmo
    algoritmo = AlgoritmoAStar(
        inicio, fin, filas, columnas, obstaculos,
        config_costos, permitir_diagonal=True, tipo_heuristica='octile'
    )
    
    print("\n" + "-"*70)
    print("EJECUCIÓN PASO A PASO")
    print("-"*70)
    
    paso = 0
    while True:
        paso += 1
        actual, vecinos, encontrado = algoritmo.ejecutar_paso()
        
        if actual is None:
            print(f"\n❌ Paso {paso}: No se encontró camino")
            break
        
        print(f"\n📍 Paso {paso}:")
        print(f"   Nodo actual: {actual}")
        print(f"   F = {algoritmo.costo_f.get(actual, 0):.2f}")
        print(f"   Vecinos explorados: {len(vecinos)}")
        
        if vecinos:
            print(f"   Lista de vecinos:")
            for v in vecinos:
                g = algoritmo.costo_g[v]
                h = algoritmo.costo_h[v]
                f = algoritmo.costo_f[v]
                print(f"      • {v}: G={g:.2f}, H={h:.2f}, F={f:.2f}")
        else:
            print(f"   (No se agregaron nuevos vecinos)")
        
        print(f"   Frontera: {len(algoritmo.frontera)} nodos")
        print(f"   Cerrados: {len(algoritmo.cerrado)} nodos")
        
        if encontrado:
            print(f"\n✅ ¡CAMINO ENCONTRADO en el paso {paso}!")
            camino = reconstruir_camino(algoritmo.vino_de, inicio, fin)
            print(f"   Longitud del camino: {len(camino) + 1} nodos")
            print(f"   Costo total: {algoritmo.costo_g[fin]:.2f}")
            print(f"   Nodos explorados: {algoritmo.nodos_explorados}")
            print(f"   Vecinos evaluados: {algoritmo.vecinos_totales_evaluados}")
            break
        
        # Límite de seguridad
        if paso > 50:
            print("\n⚠️ Límite de pasos alcanzado")
            break
    
    # Verificar consistencia
    print("\n" + "-"*70)
    print("VERIFICACIÓN DE CONSISTENCIA")
    print("-"*70)
    consistente, errores = algoritmo.verificar_consistencia()
    if consistente:
        print("✅ Todas las estructuras son consistentes")
    else:
        print("❌ Se encontraron inconsistencias:")
        for error in errores:
            print(f"   • {error}")
    
    print("\n" + "="*70)
    print("FIN DE LA PRUEBA")
    print("="*70)


if __name__ == "__main__":
    test_algoritmo()