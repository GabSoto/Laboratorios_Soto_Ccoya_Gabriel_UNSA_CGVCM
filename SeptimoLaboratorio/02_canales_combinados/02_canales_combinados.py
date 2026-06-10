"""
=============================================================================
SCRIPT 2: CREAR IMAGEN CON CANALES DE COLOR COMBINADOS
=============================================================================
DESCRIPCIÓN:
    Genera una nueva imagen tomando el canal ROJO de la imagen 1,
    el canal VERDE de la imagen 2 y el canal AZUL de la imagen 3.
    Antes de combinar, todas las imágenes se redimensionan al tamaño
    de la más grande para que los arreglos sean compatibles.

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)            : Carga imagen como arreglo BGR (NumPy).
    - cv2.resize(img, (w, h))     : Ajusta dimensiones para compatibilidad.
    - cv2.split(img)              : Separa la imagen en sus 3 canales
                                    individuales (B, G, R). Devuelve tres
                                    arreglos 2-D de un canal cada uno.
    - cv2.merge([b, g, r])        : Une tres canales individuales en una
                                    imagen BGR de tres canales.
    - cv2.imwrite(ruta, img)      : Guarda la imagen resultante en disco.
    - numpy.zeros_like(canal)     : Crea un arreglo de ceros con la misma
                                    forma que el canal dado (usado para
                                    "apagar" canales no deseados).

PROCESO:
    1. Cargar y redimensionar las 3 imágenes al mismo tamaño.
    2. Separar los canales de cada imagen con cv2.split.
       OpenCV trabaja en orden BGR, entonces:
         split devuelve  (b, g, r)  →  índices 0, 1, 2
    3. Construir la nueva imagen tomando:
         Canal R  ←  canal[2] de imagen1
         Canal G  ←  canal[1] de imagen2
         Canal B  ←  canal[0] de imagen3
    4. Unir los tres canales con cv2.merge y guardar el resultado.
=============================================================================
"""
import cv2
import numpy as np

# ── 1. Cargar las imágenes ─────────────────────────────────────────────────
img1 = cv2.imread("01_redimensionar/redim_Auto.jpg")
img2 = cv2.imread("01_redimensionar/redim_Leon.jpg")
img3 = cv2.imread("01_redimensionar/redim_Hombre.jpg")

max_w = 2000
max_h = 1333

print("=== COMBINACIÓN DE CANALES DE COLOR ===\n")
print(f"Tamaño de trabajo: {max_w} x {max_h} px")

# ── 2. Separar canales (OpenCV usa orden BGR) ──────────────────────────────
# cv2.split devuelve una tupla (B, G, R)
b1, g1, r1 = cv2.split(img1)   # canales de imagen 1
b2, g2, r2 = cv2.split(img2)   # canales de imagen 2
b3, g3, r3 = cv2.split(img3)   # canales de imagen 3

print("Canales separados de cada imagen:")
print(f"  Imagen1  →  R promedio: {r1.mean():.1f}")
print(f"  Imagen2  →  G promedio: {g2.mean():.1f}")
print(f"  Imagen3  →  B promedio: {b3.mean():.1f}")

# ── 4. Construir la imagen combinada ──────────────────────────────────────
# Necesitamos pasar (B, G, R) a cv2.merge
# Usamos ceros para los canales que NO tomamos de cada imagen
cero = np.zeros((max_h, max_w), dtype=np.uint8)

# Solo canal rojo de img1 (los otros dos en cero)
# Solo canal verde de img2
# Solo canal azul  de img3
combinada = cv2.merge([b3, g2, r1])   # merge espera lista [B, G, R]

cv2.imwrite("combinada.png", combinada)
print("\n  Nueva imagen guardada: combinada.png")
print(f"  Shape resultante: {combinada.shape}")
print("\n✔  Canal R de imagen1 + Canal G de imagen2 + Canal B de imagen3")
