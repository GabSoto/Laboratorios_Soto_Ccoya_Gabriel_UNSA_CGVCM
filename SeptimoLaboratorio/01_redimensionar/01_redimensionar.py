"""
=============================================================================
SCRIPT 1: REDIMENSIONAR IMÁGENES
=============================================================================
DESCRIPCIÓN:
    Abre tres imágenes y las redimensiona para que todas tengan las mismas
    dimensiones que la imagen más grande entre las tres.

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)        : Lee una imagen desde disco y la carga en
                                memoria como un arreglo NumPy (BGR).
    - img.shape               : Atributo de NumPy que devuelve (alto, ancho,
                                canales). Usado para obtener las dimensiones.
    - cv2.resize(img, (w,h))  : Redimensiona la imagen al tamaño (ancho, alto)
                                indicado. Interpola píxeles para ajustar.
    - cv2.imwrite(ruta, img)  : Guarda la imagen en disco en el formato
                                indicado por la extensión del nombre.

PROCESO:
    1. Se leen las 3 imágenes con imread.
    2. Se obtiene el alto y ancho de cada una con .shape.
    3. Se determina la imagen más grande comparando ancho*alto (área).
    4. Se redimensionan las otras dos imágenes al tamaño máximo con resize.
    5. Se guardan las imágenes resultantes con imwrite.
=============================================================================
"""
import cv2

# ── 1. Cargar las tres imágenes ────────────────────────────────────────────
img1 = cv2.imread("00_base_images/Auto.jpg")
img2 = cv2.imread("00_base_images/Leon.jpg")
img3 = cv2.imread("00_base_images/Hombre.jpg")

imagenes = [img1, img2, img3]
nombres  = ["Auto.jpg", "Leon.jpg", "Hombre.jpg"]

print("=== REDIMENSIONAR IMÁGENES ===\n")
for nombre, img in zip(nombres, imagenes):
    h, w = img.shape[:2]          # .shape devuelve (alto, ancho, canales)
    print(f"  {nombre}: {w} x {h} px")

# ── 2. Encontrar las dimensiones máximas ───────────────────────────────────
# Calculamos el área de cada imagen y nos quedamos con el tamaño del mayor
dimensiones = [(img.shape[1], img.shape[0]) for img in imagenes]  # (w, h)
max_w = max(d[0] for d in dimensiones)
max_h = max(d[1] for d in dimensiones)

print(f"\nTamaño objetivo (imagen más grande): {max_w} x {max_h} px")

# ── 3. Redimensionar todas al tamaño máximo ────────────────────────────────
# cv2.resize recibe (ancho, alto) — al revés que .shape
resized = []
for i, (img, nombre) in enumerate(zip(imagenes, nombres)):
    r = cv2.resize(img, (max_w, max_h))  # interpolación bilineal por defecto
    resized.append(r)
    salida = f"redim_{nombre}"
    cv2.imwrite(salida, r)
    print(f"  Guardada: {salida}  →  {r.shape[1]} x {r.shape[0]} px")

print("\n✔  Las tres imágenes ahora tienen el mismo tamaño.")