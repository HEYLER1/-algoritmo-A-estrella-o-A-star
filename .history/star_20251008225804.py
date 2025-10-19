import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configuración de la matriz
filas = int(input("¿Cuántas filas quieres? "))
columnas = int(input("¿Cuántas columnas quieres? "))

# Crear la figura
fig, ax = plt.subplots(figsize=(columnas, filas))

# Configurar los límites del gráfico
ax.set_xlim(0, columnas)
ax.set_ylim(0, filas)
ax.set_aspect('equal')

# Dibujar la cuadrícula
for i in range(filas + 1):
    ax.plot([0, columnas], [i, i], 'k-', linewidth=0.5)

for j in range(columnas + 1):
    ax.plot([j, j], [0, filas], 'k-', linewidth=0.5)

# Invertir el eje Y para que (0,0) esté arriba a la izquierda
ax.invert_yaxis()

# Eliminar los ticks de los ejes
ax.set_xticks(np.arange(0.5, columnas, 1))
ax.set_yticks(np.arange(0.5, filas, 1))

# Agregar etiquetas a las celdas (opcional)
letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(filas):
    for j in range(columnas):
        idx = i * columnas + j
        if idx < len(letras):
            ax.text(j + 0.5, i + 0.5, letras[idx], 
                   ha='center', va='center', fontsize=12)

# Función para colorear celdas (ejemplo)
def colorear_celda(fila, columna, color='cyan'):
    rect = patches.Rectangle((columna, fila), 1, 1, 
                             linewidth=0.5, 
                             edgecolor='black', 
                             facecolor=color)
    ax.add_patch(rect)

# Ejemplo: colorear algunas celdas (como en tu imagen)
# Puedes modificar esto según necesites
colorear_celda(1, 3, 'cyan')  # H
colorear_celda(2, 3, 'cyan')  # M
colorear_celda(3, 3, 'cyan')  # Q
colorear_celda(4, 3, 'cyan')  # V

plt.title(f'Cuadrícula A* ({filas}x{columnas})', fontsize=14)
plt.tight_layout()
plt.show()