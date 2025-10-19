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

# Direcciones de movimiento
# (cambio_fila, cambio_columna, tipo)
DIRECCIONES_4 = [
    (0, 1, 'horizontal'),   # derecha
    (1, 0, 'vertical'),     # abajo
    (0, -1, 'horizontal'),  # izquierda
    (-1, 0, 'vertical')     # arriba
]

DIRECCIONES_8 = [
    (0, 1, 'horizontal'),    # derecha
    (1, 0, 'vertical'),      # abajo
    (0, -1, 'horizontal'),   # izquierda
    (-1, 0, 'vertical'),     # arriba
    (1, 1, 'diagonal'),      # diagonal abajo-derecha
    (1, -1, 'diagonal'),     # diagonal abajo-izquierda
    (-1, 1, 'diagonal'),     # diagonal arriba-derecha
    (-1, -1, 'diagonal')     # diagonal arriba-izquierda
]

# Configuración por defecto
FILAS_DEFAULT = 8
COLUMNAS_DEFAULT = 10

# Costos de movimiento por defecto
COSTO_HORIZONTAL_DEFAULT = 1.0
COSTO_VERTICAL_DEFAULT = 1.0
COSTO_DIAGONAL_DEFAULT = 1.4  # aproximadamente √2

# Permitir movimientos diagonales por defecto
PERMITIR_DIAGONAL_DEFAULT = False