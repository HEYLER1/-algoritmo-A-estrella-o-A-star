"""
Funciones principales del algoritmo A*
"""

def calcular_peso_movimiento(desde, hacia):
    """
    Calcula el peso del movimiento entre dos celdas adyacentes.
    
    Args:
        desde: Tupla (fila, col) del nodo origen
        hacia: Tupla (fila, col) del nodo destino
    
    Returns:
        int: Peso del movimiento (por defecto 1)
    """
    # Movimiento básico tiene peso 1
    # Puedes modificar esto para agregar diferentes pesos
    return 1


def calcular_heuristica(nodo_actual, nodo_objetivo):
    """
    Calcula la heurística usando distancia Manhattan.
    H = |x1 - x2| + |y1 - y2|
    
    Args:
        nodo_actual: Tupla (fila, col) del nodo actual
        nodo_objetivo: Tupla (fila, col) del nodo objetivo
    
    Returns:
        int: Distancia Manhattan entre los nodos
    """
    return abs(nodo_actual[0] - nodo_objetivo[0]) + abs(nodo_actual[1] - nodo_objetivo[1])


def calcular_funcion_costo(costo_g, costo_h):
    """
    Calcula la función de costo total F.
    F = G + H
    
    Args:
        costo_g: Costo real desde el inicio
        costo_h: Heurística (estimación al objetivo)
    
    Returns:
        int: Costo total F
    """
    return costo_g + costo_h


def obtener_vecinos(nodo, filas, columnas, obstaculos):
    """
    Obtiene los vecinos válidos de un nodo.
    
    Args:
        nodo: Tupla (fila, col) del nodo actual
        filas: Número de filas de la cuadrícula
        columnas: Número de columnas de la cuadrícula
        obstaculos: Set de tuplas con posiciones de obstáculos
    
    Returns:
        list: Lista de vecinos válidos
    """
    from constantes import DIRECCIONES
    
    fila, col = nodo
    vecinos = []
    
    for df, dc in DIRECCIONES:
        nueva_fila, nueva_col = fila + df, col + dc
        
        # Verificar que esté dentro de los límites
        if (0 <= nueva_fila < filas and 
            0 <= nueva_col < columnas and
            (nueva_fila, nueva_col) not in obstaculos):
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