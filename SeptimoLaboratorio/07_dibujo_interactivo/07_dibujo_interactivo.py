"""
=============================================================================
SCRIPT 7: PROGRAMA DE DIBUJO INTERACTIVO CON MOUSE Y TECLADO
=============================================================================
DESCRIPCIÓN:
    Permite al usuario dibujar figuras geométricas usando el mouse y el
    teclado, con opciones para deshacer el último trazo y guardar el dibujo.

CONTROLES:
    Mouse:
      - Clic izquierdo + arrastrar  → dibuja la figura activa
      - Soltar botón               → finaliza la figura

    Teclado:
      R   → cambiar figura a Rectángulo
      C   → cambiar figura a Círculo
      L   → cambiar figura a Línea
      F   → cambiar figura a Flecha
      Z   → Deshacer última figura
      S   → Guardar imagen como 'dibujo_guardado.png'
      Q   → Salir

FUNCIONES UTILIZADAS:
    - cv2.namedWindow(nombre)             : Crea ventana de visualización.
    - cv2.setMouseCallback(nombre, fn)    : Registra una función callback
                                           que se llama automáticamente
                                           con cada evento del mouse.
                                           Parámetros del callback:
                                             event: tipo de evento (click,
                                                    move, release, etc.)
                                             x, y : posición del cursor
                                             flags: modificadores (shift...)
                                             param: dato extra opcional
    - cv2.EVENT_LBUTTONDOWN               : Evento: botón izquierdo presionado
    - cv2.EVENT_MOUSEMOVE                 : Evento: movimiento del mouse
    - cv2.EVENT_LBUTTONUP                 : Evento: botón izquierdo suelto
    - cv2.rectangle(img, pt1, pt2, c, t)  : Dibuja rectángulo entre dos pts.
    - cv2.circle(img, c, r, color, t)     : Dibuja círculo.
    - cv2.line(img, pt1, pt2, color, t)   : Dibuja línea.
    - cv2.arrowedLine(img, pt1, pt2, c,t) : Dibuja flecha.
    - img.copy()                          : Copia del canvas para previsualizar
                                           sin alterar el dibujo permanente.
    - cv2.waitKey(ms)                     : Lee tecla presionada.
    - cv2.imwrite(ruta, img)              : Guarda el dibujo final.

PROCESO:
    1. Crear un canvas en blanco (lienzo para dibujar).
    2. Mantener una lista de "capas": cada elemento guarda una copia del
       canvas antes de agregar la figura actual. Esto permite deshacer.
    3. El callback de mouse actualiza las coordenadas de inicio/fin.
    4. Mientras se arrastra el mouse, se dibuja sobre una copia temporal
       para previsualizar sin alterar el canvas permanente.
    5. Al soltar el botón, la figura se graba definitivamente.
    6. Deshacer = restaurar la última copia de la lista de historial.
=============================================================================
NOTA: Requiere entorno gráfico (monitor/pantalla o display virtual).
=============================================================================
"""
import cv2
import numpy as np

# ── Parámetros globales del programa ──────────────────────────────────────
ANCHO, ALTO = 800, 600
COLOR_FONDO = (255, 255, 255)   # Blanco

# Estado del dibujo
canvas      = np.full((ALTO, ANCHO, 3), 255, dtype=np.uint8)  # lienzo blanco
historial   = []                # lista de copias para deshacer
figura_actual = "rectangulo"    # figura activa
dibujando   = False             # True mientras se arrastra el mouse
x_inicio = y_inicio = 0        # coordenadas del primer clic
x_actual  = y_actual  = 0      # coordenadas actuales del cursor

COLOR_FIGURA = (0, 0, 200)      # Rojo (BGR)
GROSOR       = 2

# ── Función callback del mouse ────────────────────────────────────────────
def callback_mouse(event, x, y, flags, param):
    """
    Función llamada automáticamente por OpenCV ante cualquier evento del mouse.
    Actualiza las variables globales de estado del dibujo.
    """
    global dibujando, x_inicio, y_inicio, x_actual, y_actual, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        # Guardar copia en historial ANTES de dibujar (para poder deshacer)
        historial.append(canvas.copy())
        dibujando = True
        x_inicio, y_inicio = x, y
        x_actual,  y_actual  = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if dibujando:
            x_actual, y_actual = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        if dibujando:
            x_actual, y_actual = x, y
            # Grabar la figura definitivamente en el canvas
            dibujar_figura(canvas, figura_actual,
                           (x_inicio, y_inicio), (x_actual, y_actual))
            dibujando = False


def dibujar_figura(img, figura, pt1, pt2):
    """Dibuja la figura seleccionada entre dos puntos."""
    if figura == "rectangulo":
        cv2.rectangle(img, pt1, pt2, COLOR_FIGURA, GROSOR)

    elif figura == "circulo":
        # Radio = distancia euclídea entre los dos puntos / 2
        cx = (pt1[0] + pt2[0]) // 2
        cy = (pt1[1] + pt2[1]) // 2
        radio = int(((pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2)**0.5 // 2)
        cv2.circle(img, (cx, cy), max(1, radio), COLOR_FIGURA, GROSOR)

    elif figura == "linea":
        cv2.line(img, pt1, pt2, COLOR_FIGURA, GROSOR)

    elif figura == "flecha":
        cv2.arrowedLine(img, pt1, pt2, COLOR_FIGURA, GROSOR, tipLength=0.2)


def mostrar_info(img, figura):
    """Superpone instrucciones en la esquina superior del lienzo."""
    instrucciones = [
        f"Figura: {figura.upper()}  |  R=Rect  C=Circ  L=Linea  F=Flecha",
        "Z=Deshacer   S=Guardar   Q=Salir"
    ]
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (ANCHO, 50), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    for i, texto in enumerate(instrucciones):
        cv2.putText(img, texto, (10, 18 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 200), 1,
                    cv2.LINE_AA)


# ── Ventana y callback ────────────────────────────────────────────────────
cv2.namedWindow("Dibujo Interactivo")
cv2.setMouseCallback("Dibujo Interactivo", callback_mouse)

print("=== PROGRAMA DE DIBUJO INTERACTIVO ===")
print("  R: Rectángulo  |  C: Círculo  |  L: Línea  |  F: Flecha")
print("  Z: Deshacer    |  S: Guardar  |  Q: Salir")

# ── Bucle principal ───────────────────────────────────────────────────────
while True:
    # Crear copia temporal para previsualizar figura en construcción
    vista = canvas.copy()

    if dibujando:
        dibujar_figura(vista, figura_actual,
                       (x_inicio, y_inicio), (x_actual, y_actual))

    mostrar_info(vista, figura_actual)
    cv2.imshow("Dibujo Interactivo", vista)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('r') or tecla == ord('R'):
        figura_actual = "rectangulo"
        print("  → Figura: Rectángulo")
    elif tecla == ord('c') or tecla == ord('C'):
        figura_actual = "circulo"
        print("  → Figura: Círculo")
    elif tecla == ord('l') or tecla == ord('L'):
        figura_actual = "linea"
        print("  → Figura: Línea")
    elif tecla == ord('f') or tecla == ord('F'):
        figura_actual = "flecha"
        print("  → Figura: Flecha")
    elif tecla == ord('z') or tecla == ord('Z'):
        # Deshacer: restaurar última copia del historial
        if historial:
            canvas = historial.pop()
            print("  → Deshacer: última figura eliminada")
        else:
            print("  → Sin acciones para deshacer")
    elif tecla == ord('s') or tecla == ord('S'):
        cv2.imwrite("dibujo_guardado.png", canvas)
        print("  → Dibujo guardado como 'dibujo_guardado.png'")
    elif tecla == ord('q') or tecla == ord('Q'):
        print("  Saliendo...")
        break

cv2.destroyAllWindows()
print("\n✔  Programa de dibujo cerrado.")
