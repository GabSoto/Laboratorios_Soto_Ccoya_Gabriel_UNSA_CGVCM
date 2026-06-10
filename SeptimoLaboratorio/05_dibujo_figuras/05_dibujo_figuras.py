"""
=============================================================================
SCRIPT 5: DIBUJO DE FIGURAS Y TEXTO EN IMÁGENES
=============================================================================
DESCRIPCIÓN:
    Abre una imagen que contiene una persona, dibuja un círculo sobre su
    cara y añade texto descriptivo indicando qué es la figura.

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)            : Carga la imagen de la persona.
    - cv2.circle(img, centro, radio, color, grosor)
                                  : Dibuja un círculo en la imagen.
                                    centro   = (x, y) en píxeles
                                    radio    = en píxeles
                                    color    = (B, G, R)
                                    grosor   = -1 relleno, >0 contorno
    - cv2.putText(img, texto, origen, fuente, escala, color, grosor,
                  lineType)       : Escribe texto en la imagen.
                                    origen   = esquina inferior-izquierda
                                    fuente   = constante cv2.FONT_...
                                    escala   = tamaño relativo de la fuente
                                    lineType = cv2.LINE_AA (anti-aliasing)
    - cv2.rectangle(img, pt1, pt2, color, grosor)
                                  : Dibuja un rectángulo. Usado para resaltar
                                    zona de interés secundaria.
    - cv2.imwrite(ruta, img)      : Guarda la imagen anotada en disco.
    - img.copy()                  : Crea una copia para no modificar el
                                    original mientras se realizan las anotaciones.

PROCESO:
    1. Cargar la imagen de la persona con imread.
    2. Hacer una copia con .copy() para trabajar sin alterar el original.
    3. Identificar manualmente (o con detector) la posición del rostro.
    4. Dibujar un círculo alrededor de la cara con cv2.circle.
    5. Añadir etiqueta de texto descriptivo con cv2.putText.
    6. Guardar la imagen anotada con imwrite.

NOTA SOBRE DETECCIÓN AUTOMÁTICA:
    Para detección automática se puede usar cv2.CascadeClassifier con el
    clasificador Haar 'haarcascade_frontalface_default.xml' incluido en
    OpenCV. En este ejemplo la posición se define manualmente para claridad.
=============================================================================
"""
import cv2

# ── 1. Cargar la imagen ────────────────────────────────────────────────────
imagen = cv2.imread("00_base_images/Leon.jpg")
if imagen is None:
    raise FileNotFoundError("No se encontró 'Leon.jpg'.")

print("=== DIBUJO DE FIGURAS Y TEXTO ===\n")
print(f"Imagen cargada: {imagen.shape[1]} x {imagen.shape[0]} px")

# ── 2. Trabajar sobre una copia ───────────────────────────────────────────
anotada = imagen.copy()

# ── 3. Posición del rostro (detectada manualmente o con clasificador) ─────
# En una imagen real se usaría cv2.CascadeClassifier.detectMultiScale()
# Aquí sabemos que la cara está centrada en x=180, y=200, radio≈85
centro_cara = (550, 400)
radio_cara  = 150

# ── 4. Dibujar círculo sobre la cara ─────────────────────────────────────
# Parámetros: imagen, centro (x,y), radio, color BGR, grosor
# Grosor positivo = contorno, -1 = relleno
cv2.circle(
    anotada,
    centro_cara,        # centro del círculo en (x, y)
    radio_cara,         # radio en píxeles
    (0, 255, 255),      # color: amarillo en BGR
    3                   # grosor del contorno en píxeles
)

# ── 5. Añadir texto descriptivo ──────────────────────────────────────────
# Fondo semitransparente para legibilidad del texto
etiqueta = "LEON"
# Posición del texto: ligeramente sobre el círculo
pos_texto = (centro_cara[0] - 45, centro_cara[1] - radio_cara - 12)

# Rectángulo de fondo
cv2.rectangle(
    anotada,
    (pos_texto[0] - 5, pos_texto[1] - 22),
    (pos_texto[0] + 100, pos_texto[1] + 5),
    (0, 0, 0),          # negro
    -1                  # relleno
)

# Texto principal
cv2.putText(
    anotada,
    etiqueta,
    pos_texto,
    cv2.FONT_HERSHEY_SIMPLEX,   # fuente estándar sin serifa
    0.8,                        # escala (tamaño)
    (0, 255, 255),              # color: amarillo
    2,                          # grosor del trazo
    cv2.LINE_AA                 # anti-aliasing para texto suave
)

# ── 6. Información adicional en la parte inferior ────────────────────────
cv2.putText(
    anotada,
    "Deteccion: cara detectada",
    (10, imagen.shape[0] - 15),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.55,
    (255, 255, 255),
    1,
    cv2.LINE_AA
)

# ── 7. Guardar resultado ─────────────────────────────────────────────────
cv2.imwrite("leon_anotado.jpg", anotada)
print(f"  Círculo dibujado en: centro={centro_cara}, radio={radio_cara}px")
print(f"  Texto agregado: '{etiqueta}'")
print("  Imagen guardada: persona_anotada.jpg")
print("\n✔  Anotaciones aplicadas correctamente.")
