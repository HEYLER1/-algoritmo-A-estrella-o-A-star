"""
Funciones principales del algoritmo A*
"""
import math


def calcular_peso_movimiento(desde, hacia, config_costos):
    """
    Calcula el peso del movimiento entre dos celdas adyacentes.
    
    Args:
        desde: Tupla (fila, col) del nodo origen
        hacia: Tupla (fila, col) del nodo destino
        config_costos: Diccionario con 'horizontal', 'vertical', 'diagonal'
    
    Returns:
        float: Peso del movimiento
    """
    diff_fila = abs(hacia[0] - desde[0])
    diff_col = abs(hacia[1] - desde[1])
    
    # Movimiento diagonal
    if diff_fila == 1 and diff_col == 1:
        return config_costos['diagonal']
    
    # Movimiento horizontal
    elif diff_fila == 0 and diff_col == 1:
        return config_costos['horizontal']
    
    # Movimiento vertical
    elif diff_fila == 1 and diff_col == 0:
        return config_costos['vertical']
    
    # Por defecto (no debería llegar aquí)
    return 1.0


def calcular_heuristica(nodo_actual, nodo_objetivo, config_costos, tipo_heuristica='manhattan'):
    """
    Calcula la heurística según el tipo seleccionado.
    
    Args:
        nodo_actual: Tupla (fila, col) del nodo actual
        nodo_objetivo: Tupla (fila, col) del nodo objetivo
        config_costos: Diccionario con 'horizontal', 'vertical', 'diagonal'
        tipo_heuristica: 'manhattan', 'euclidiana', 'octile', 'chebyshev'
    
    Returns:
        float: Valor de la heurística
    """
    dx = abs(nodo_actual[0] - nodo_objetivo[0])
    dy = abs(nodo_actual[1] - nodo_objetivo[1])
    
    if tipo_heuristica == 'manhattan':
        # Distancia Manhattan: suma de diferencias absolutas
        # Usa el promedio de costos horizontal y vertical
        costo_promedio = (config_costos['horizontal'] + config_costos['vertical']) / 2
        return (dx + dy) * costo_promedio
    
    elif tipo_heuristica == 'euclidiana':
        # Distancia Euclidiana: línea recta
        distancia = math.sqrt(dx**2 + dy**2)
        costo_promedio = (config_costos['horizontal'] + config_costos['vertical']) / 2
        return distancia * costo_promedio
    
    elif tipo_heuristica == 'octile':
        # Distancia Octile: considera movimientos diagonales
        # Óptima cuando se permiten 8 direcciones
        costo_diagonal = config_costos['diagonal']
        costo_recto = min(config_costos['horizontal'], config_costos['vertical'])
        
        if dx > dy:
            return costo_diagonal * dy + costo_recto * (dx - dy)
        else:
            return costo_diagonal * dx + costo_recto * (dy - dx)
    
    elif tipo_heuristica == 'chebyshev':
        # Distancia Chebyshev: máximo de las diferencias
        costo_diagonal = config_costos['diagonal']
        return max(dx, dy) * costo_diagonal
    
    else:
        # Por defecto: Manhattan
        costo_promedio = (config_costos['horizontal'] + config_costos['vertical']) / 2
        return (dx + dy) * costo_promedio


def calcular_funcion_costo(costo_g, costo_h):
    """
    Calcula la función de costo total F.
    F = G + H
    
    Args:
        costo_g: Costo real desde el inicio
        costo_h: Heurística (estimación al objetivo)
    
    Returns:
        float: Costo total F
    """
    return costo_g + costo_h


def obtener_vecinos(nodo, filas, columnas, obstaculos, permitir_diagonal=False):
    """
    Obtiene los vecinos válidos de un nodo.
    
    IMPORTANTE: El algoritmo A* explora TODOS los vecinos disponibles
    y usa la función de costo F para decidir cuál explorar primero.
    
    Args:
        nodo: Tupla (fila, col) del nodo actual
        filas: Número de filas de la cuadrícula
        columnas: Número de columnas de la cuadrícula
        obstaculos: Set de tuplas con posiciones de obstáculos
        permitir_diagonal: Si True, permite movimientos diagonales (8 direcciones)
                          Si False, solo horizontal/vertical (4 direcciones)
    
    Returns:
        list: Lista de vecinos válidos
    """
    fila, col = nodo
    vecinos = []
    
    # Direcciones: derecha, abajo, izquierda, arriba
    direcciones_basicas = [
        (0, 1),   # derecha
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (-1, 0)   # arriba
    ]
    
    # Direcciones diagonales
    direcciones_diagonales = [
        (1, 1),   # diagonal abajo-derecha
        (1, -1),  # diagonal abajo-izquierda
        (-1, 1),  # diagonal arriba-derecha
        (-1, -1)  # diagonal arriba-izquierda
    ]
    
    # Primero verificar movimientos básicos (siempre disponibles)
    for df, dc in direcciones_basicas:
        nueva_fila, nueva_col = fila + df, col + dc
        
        # Verificar límites y obstáculos
        if (0 <= nueva_fila < filas and 
            0 <= nueva_col < columnas and
            (nueva_fila, nueva_col) not in obstaculos):
            vecinos.append((nueva_fila, nueva_col))
    
    # Si se permiten diagonales, agregar movimientos diagonales
    if permitir_diagonal:
        for df, dc in direcciones_diagonales:
            nueva_fila, nueva_col = fila + df, col + dc
            
            # Verificar límites
            if not (0 <= nueva_fila < filas and 0 <= nueva_col < columnas):
                continue
            
            # Verificar que el destino no sea obstáculo
            if (nueva_fila, nueva_col) in obstaculos:
                continue
            
            # IMPORTANTE: Verificar que no haya obstáculos bloqueando el movimiento diagonal
            # Para moverse en diagonal, las dos celdas adyacentes deben estar libres
            celda_horizontal = (fila, nueva_col)  # Celda en la misma fila
            celda_vertical = (nueva_fila, col)     # Celda en la misma columna
            
            # Solo permitir diagonal si ambas celdas adyacentes están libres
            if (celda_horizontal not in obstaculos and 
                celda_vertical not in obstaculos):
                vecinos.append((nueva_fila, nueva_col))
    
    return vecinos


def reconstruir_camino(vino_de, inicio, fin):
    """
    Reconstruye el camino desde el inicio hasta el fin.
    
    Args:
        vino_de: Diccionario con el camino recorrido
        inicio: Tupla (fila, col) del inicio
        fin: Tupla (fila, col) del fin
    
    Returns:
        list: Lista de nodos que forman el camino
    """
    camino = []
    actual = fin
    
    while actual in vino_de:
        actual = vino_de[actual]
        if actual != inicio:
            camino.append(actual)
    
    camino.reverse()
    return camino