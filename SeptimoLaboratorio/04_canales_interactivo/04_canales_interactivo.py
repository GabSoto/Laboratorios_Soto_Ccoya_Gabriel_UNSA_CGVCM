"""
=============================================================================
SCRIPT 4: APLICACIÓN INTERACTIVA DE VISUALIZACIÓN DE CANALES
=============================================================================
DESCRIPCIÓN:
    Muestra la imagen combinada en una ventana. El usuario puede presionar
    teclas para activar o desactivar la visualización de cada canal de color:
        R  →  alterna el canal Rojo
        G  →  alterna el canal Verde
        B  →  alterna el canal Azul
        Q  →  salir de la aplicación

FUNCIONES UTILIZADAS:
    - cv2.imread(ruta)            : Carga la imagen original.
    - cv2.split(img)              : Separa la imagen en sus 3 canales B,G,R.
    - cv2.merge([b, g, r])        : Reconstruye la imagen BGR desde canales.
    - numpy.zeros_like(canal)     : Crea un canal vacío (todo ceros) del
                                    mismo tamaño que un canal real.
    - cv2.namedWindow(nombre)     : Crea una ventana con nombre para mostrar.
    - cv2.imshow(nombre, img)     : Muestra la imagen en la ventana indicada.
    - cv2.waitKey(ms)             : Espera 'ms' milisegundos a que el usuario
                                    presione una tecla. Devuelve el código
                                    ASCII de la tecla. Con 1 ms forma el
                                    bucle de eventos en tiempo real.
    - cv2.destroyAllWindows()     : Cierra todas las ventanas de OpenCV.
    - cv2.putText(img, texto, ...) : Escribe texto en la imagen para mostrar
                                    el estado de los canales activos.

PROCESO:
    1. Cargar imagen y separar sus canales B, G, R.
    2. Mantener un estado booleano por canal: {R: True, G: True, B: True}.
    3. En cada iteración del bucle:
       a. Construir la imagen visible usando solo los canales activos
          (se reemplaza por cero el canal inactivo).
       b. Superponer texto informativo con cv2.putText.
       c. Mostrar con imshow.
       d. Leer tecla con waitKey y actualizar el estado según la tecla.
    4. Al presionar 'q' se sale del bucle y se cierran las ventanas.
=============================================================================
NOTA: Este script requiere un entorno gráfico (pantalla/monitor).
      Ejecutar en escritorio o con display virtual (Xvfb).
=============================================================================
"""
import cv2
import numpy as np

# ── 1. Cargar la imagen y separar canales ─────────────────────────────────
imagen = cv2.imread("02_canales_combinados/combinada.png")
if imagen is None:
    raise FileNotFoundError("No se encontró 'combinada.png'.")

# cv2.split devuelve los canales en orden BGR
b, g, r = cv2.split(imagen)
cero = np.zeros_like(b)         # canal vacío (negro)

# ── 2. Estado inicial: todos los canales visibles ─────────────────────────
estado = {"R": True, "G": True, "B": True}

print("=== VISUALIZACIÓN INTERACTIVA DE CANALES ===")
print("  Teclas: R → Rojo | G → Verde | B → Azul | Q → Salir")

cv2.namedWindow("Canales de Color", cv2.WINDOW_NORMAL)

# ── 3. Bucle principal de eventos ─────────────────────────────────────────
while True:
    # Construir imagen usando solo canales activos
    canal_r = r    if estado["R"] else cero
    canal_g = g    if estado["G"] else cero
    canal_b = b    if estado["B"] else cero

    # cv2.merge reconstruye BGR desde canales individuales
    visible = cv2.merge([canal_b, canal_g, canal_r])

    # ── 4. Superponer texto de estado ──────────────────────────────────────
    texto_r = f"[R] Rojo: {'ON ' if estado['R'] else 'OFF'}"
    texto_g = f"[G] Verde: {'ON ' if estado['G'] else 'OFF'}"
    texto_b = f"[B] Azul: {'ON ' if estado['B'] else 'OFF'}"

    def color_estado(activo):
        return (50, 255, 50) if activo else (50, 50, 255)

    # putText(imagen, texto, posicion, fuente, escala, color, grosor)
    cv2.putText(visible, texto_r, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_estado(estado["R"]), 2)
    cv2.putText(visible, texto_g, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_estado(estado["G"]), 2)
    cv2.putText(visible, texto_b, (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_estado(estado["B"]), 2)
    cv2.putText(visible, "[Q] Salir", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

    cv2.imshow("Canales de Color", visible)

    # ── 5. Leer tecla (espera 1 ms para no bloquear) ───────────────────────
    # waitKey retorna -1 si no se presionó nada, o el código ASCII de la tecla
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('r') or tecla == ord('R'):
        estado["R"] = not estado["R"]
        print(f"  Canal Rojo:  {'ON' if estado['R'] else 'OFF'}")
    elif tecla == ord('g') or tecla == ord('G'):
        estado["G"] = not estado["G"]
        print(f"  Canal Verde: {'ON' if estado['G'] else 'OFF'}")
    elif tecla == ord('b') or tecla == ord('B'):
        estado["B"] = not estado["B"]
        print(f"  Canal Azul:  {'ON' if estado['B'] else 'OFF'}")
    elif tecla == ord('q') or tecla == ord('Q'):
        print("  Saliendo...")
        break

cv2.destroyAllWindows()
print("\n✔  Aplicación cerrada.")
