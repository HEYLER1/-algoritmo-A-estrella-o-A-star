"""
Constantes y configuraciones del proyecto A*
"""

# Tamaños
CELDA_SIZE = 80
MAX_FILAS = 20
MAX_COLUMNAS = 20

# Colores
COLORES = {
    'vacio': 'white',
    'inicio': '#4CAF50',  # Verde
    'fin': '#F44336',      # Rojo
    'obstaculo': '#212121', # Negro
    'visitado': '#BBDEFB',  # Azul claro
    'camino': '#FFEB3B',    # Amarillo
    'frontera': '#FF9800'   # Naranja
}

# Direcciones de movimiento (derecha, abajo, izquierda, arriba)
DIRECCIONES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Configuración por defecto
FILAS_DEFAULT = 8
COLUMNAS_DEFAULT = 10