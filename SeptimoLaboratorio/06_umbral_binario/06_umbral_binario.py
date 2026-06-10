"""
=============================================================================
SCRIPT 6: APLICACIÓN DE UMBRAL BINARIO (THRESHOLD)
=============================================================================
DESCRIPCIÓN:
    Convierte una imagen a escala de grises y aplica un umbral binario para
    producir una imagen en blanco y negro (binarizada). Los píxeles con
    intensidad superior al umbral se vuelven blancos (255) y los demás,
    negros (0).

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)                    : Carga la imagen.
    - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY): Convierte a escala de grises.
                                            Necesario porque threshold opera
                                            sobre imágenes de 1 canal.
    - cv2.threshold(src, thresh, maxval, type)
                                          : Aplica el umbral. Parámetros:
                                            src    = imagen en gris
                                            thresh = valor del umbral (0-255)
                                            maxval = valor para píxeles que
                                                     superan el umbral
                                            type   = tipo de umbralización
                                          Devuelve: (retval, imagen_binaria)
                                          retval = umbral usado (útil para
                                                   OTSU)
    - cv2.THRESH_BINARY                   : Píxel > umbral → maxval, sino 0
    - cv2.THRESH_BINARY_INV               : Inverso del anterior
    - cv2.THRESH_OTSU                     : Calcula umbral óptimo automático
                                            usando el método de Otsu
    - cv2.imwrite(ruta, img)              : Guarda la imagen binarizada.

PROCESO:
    1. Cargar imagen y convertir a grises.
    2. Aplicar cv2.threshold con umbral manual (127) → THRESH_BINARY.
    3. Aplicar cv2.threshold con umbral automático Otsu → mejor separación.
    4. Guardar ambos resultados para comparar.

EXPLICACIÓN DEL UMBRAL BINARIO:
    Si intensidad(x,y) > umbral  →  píxel = 255 (blanco)
    Si intensidad(x,y) ≤ umbral  →  píxel = 0   (negro)
    El método de Otsu minimiza la varianza dentro de cada clase para
    encontrar el umbral óptimo automáticamente.
=============================================================================
"""
import cv2
import numpy as np

# ── 1. Cargar imagen y convertir a grises ─────────────────────────────────
imagen = cv2.imread("02_canales_combinados/combinada.png")
if imagen is None:
    raise FileNotFoundError("No se encontró 'combinada.png'.")

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
print("=== UMBRAL BINARIO (THRESHOLD) ===\n")
print(f"Imagen cargada: {imagen.shape[1]} x {imagen.shape[0]} px")
print(f"Rango de intensidades: min={gris.min()}, max={gris.max()}, "
      f"promedio={gris.mean():.1f}\n")

# ── 2. Umbral manual (valor fijo = 127) ───────────────────────────────────
# threshold devuelve (valor_umbral_usado, imagen_binarizada)
umbral_manual = 127
_, binaria_manual = cv2.threshold(
    gris,
    umbral_manual,      # umbral: píxeles > 127 → blanco
    255,                # valor máximo (blanco)
    cv2.THRESH_BINARY   # tipo: binario simple
)

cv2.imwrite("umbral_manual.png", binaria_manual)
print(f"  Umbral manual ({umbral_manual}): guardado como 'umbral_manual.png'")
blancos = np.count_nonzero(binaria_manual)
total   = binaria_manual.size
print(f"  Píxeles blancos: {blancos} ({100*blancos/total:.1f}%)")
print(f"  Píxeles negros:  {total - blancos} ({100*(total-blancos)/total:.1f}%)")

# ── 3. Umbral automático (método de Otsu) ─────────────────────────────────
# THRESH_OTSU calcula el umbral óptimo automáticamente
# Se combina con THRESH_BINARY usando el operador |
umbral_otsu, binaria_otsu = cv2.threshold(
    gris,
    0,                                      # ignorado cuando se usa Otsu
    255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU    # Otsu determina el umbral
)

cv2.imwrite("umbral_otsu.png", binaria_otsu)
print(f"\n  Umbral Otsu (automático): {umbral_otsu:.0f}")
print(f"  Guardado como: 'umbral_otsu.png'")
blancos2 = np.count_nonzero(binaria_otsu)
print(f"  Píxeles blancos: {blancos2} ({100*blancos2/total:.1f}%)")

# ── 4. Umbral invertido ───────────────────────────────────────────────────
_, binaria_inv = cv2.threshold(
    gris, umbral_manual, 255, cv2.THRESH_BINARY_INV
)
cv2.imwrite("umbral_invertido.png", binaria_inv)
print(f"\n  Umbral invertido (fondo blanco): 'umbral_invertido.png'")

print("\n✔  Tres variantes de umbral generadas correctamente.")
