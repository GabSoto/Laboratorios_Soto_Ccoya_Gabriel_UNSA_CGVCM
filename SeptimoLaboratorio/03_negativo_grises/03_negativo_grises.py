"""
=============================================================================
SCRIPT 3: CONVERSIÓN A NEGATIVO Y ESCALA DE GRISES
=============================================================================
DESCRIPCIÓN:
    Toma la imagen combinada del paso anterior y:
    a) Invierte cada píxel a su negativo (complemento a 255).
    b) Convierte el negativo a escala de grises y lo guarda.

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)                   : Carga la imagen combinada.
    - cv2.bitwise_not(img)               : Invierte bit a bit todos los
                                           valores de los píxeles.
                                           Equivalente a 255 - img para
                                           cada canal. Produce el negativo.
    - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY): Convierte imagen de color BGR
                                           a escala de grises (1 canal).
                                           Aplica ponderación perceptual:
                                           Y = 0.114B + 0.587G + 0.299R
    - cv2.imwrite(ruta, img)             : Guarda la imagen en disco.

PROCESO NEGATIVO:
    Para cada píxel y cada canal, el negativo se obtiene restando el valor
    original de 255:
        negativo(x, y, c) = 255 - original(x, y, c)
    cv2.bitwise_not() realiza exactamente esta operación de forma eficiente
    usando operaciones a nivel de bits.

PROCESO ESCALA DE GRISES:
    cv2.cvtColor con la bandera COLOR_BGR2GRAY colapsa los 3 canales en uno
    solo usando la fórmula de luminancia ponderada que imita la percepción
    humana del brillo (el ojo es más sensible al verde que al rojo o azul).
=============================================================================
"""
import cv2

# ── 1. Cargar la imagen combinada ─────────────────────────────────────────
combinada = cv2.imread("02_canales_combinados/combinada.png")
if combinada is None:
    raise FileNotFoundError("No se encontró 'combinada.png'. "
                            "Ejecuta primero el script 02.")

print("=== NEGATIVO Y ESCALA DE GRISES ===\n")
print(f"Imagen cargada: {combinada.shape[1]} x {combinada.shape[0]} px")

# ── 2. Invertir a negativo ────────────────────────────────────────────────
# cv2.bitwise_not calcula: pixel_nuevo = 255 - pixel_original
# para cada canal de cada píxel
negativo = cv2.bitwise_not(combinada)

cv2.imwrite("negativo.png", negativo)
print("\n  Imagen negativa guardada: negativo.png")
print("  Fórmula: nuevo_pixel = 255 - pixel_original")

# ── 3. Convertir el negativo a escala de grises ───────────────────────────
# COLOR_BGR2GRAY aplica: Y = 0.114*B + 0.587*G + 0.299*R
gris = cv2.cvtColor(negativo, cv2.COLOR_BGR2GRAY)

cv2.imwrite("negativo_gris.png", gris)
print("\n  Imagen en escala de grises guardada: negativo_gris.png")
print(f"  Shape resultado (1 canal): {gris.shape}")
print("  Fórmula: Y = 0.114·B + 0.587·G + 0.299·R")

# ── 4. Mostrar estadísticas ───────────────────────────────────────────────
import numpy as np
print(f"\n  Valor mínimo de píxel: {gris.min()}")
print(f"  Valor máximo de píxel: {gris.max()}")
print(f"  Valor promedio:        {gris.mean():.1f}")
print("\n✔  Negativo y escala de grises generados correctamente.")
