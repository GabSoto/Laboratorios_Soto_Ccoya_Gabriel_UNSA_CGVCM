"""
Detector de objetos con YOLOv8 (Ultralytics) + Streamlit
----------------------------------------------------------
Ejecutar con: streamlit run app.py
"""

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import io

# ----------------------------------------------------------------
# Configuración de la página
# ----------------------------------------------------------------
st.set_page_config(page_title="Detector de Objetos", page_icon="🔍", layout="centered")
st.title("🔍 Detector de Objetos con YOLOv8")
st.write(
    "Sube una imagen y el modelo reconocerá automáticamente los objetos "
    "presentes (personas, animales, vehículos, objetos cotidianos, etc.)."
)

# ----------------------------------------------------------------
# Cargar el modelo (se cachea para no recargarlo en cada interacción)
# ----------------------------------------------------------------
@st.cache_resource
def load_model():
    # "yolov8n.pt" = versión nano (rápida y liviana).
    # Otras opciones: yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt (más precisas pero más lentas)
    # El archivo de pesos se descarga automáticamente la primera vez.
    return YOLO("yolov8n.pt")

model = load_model()

# ----------------------------------------------------------------
# Slider de confianza mínima
# ----------------------------------------------------------------
confidence = st.slider(
    "Confianza mínima de detección",
    min_value=0.1, max_value=1.0, value=0.4, step=0.05
)

# ----------------------------------------------------------------
# Subida de imagen
# ----------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Selecciona una imagen (jpg, jpeg, png)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Leer imagen subida
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Imagen original")
        st.image(image, use_container_width=True)

    # --------------------------------------------------------
    # Ejecutar la detección
    # --------------------------------------------------------
    with st.spinner("Analizando imagen..."):
        results = model.predict(img_array, conf=confidence, verbose=False)
        result = results[0]

        # Imagen anotada con las cajas y etiquetas (BGR -> RGB)
        annotated_bgr = result.plot()
        annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
        annotated_image = Image.fromarray(annotated_rgb)

    with col2:
        st.subheader("Objetos detectados")
        st.image(annotated_image, use_container_width=True)

    # --------------------------------------------------------
    # Lista de objetos detectados
    # --------------------------------------------------------
    st.subheader("📋 Detalle de detecciones")
    if len(result.boxes) == 0:
        st.info("No se detectaron objetos con la confianza seleccionada.")
    else:
        detected = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf = float(box.conf[0])
            detected.append((cls_name, conf))

        for name, conf in sorted(detected, key=lambda x: -x[1]):
            st.write(f"- **{name}** ({conf*100:.1f}% de confianza)")

    # --------------------------------------------------------
    # Botón de descarga de la imagen resultante
    # --------------------------------------------------------
    buf = io.BytesIO()
    annotated_image.save(buf, format="PNG")
    st.download_button(
        label="⬇️ Descargar imagen con detecciones",
        data=buf.getvalue(),
        file_name="deteccion_objetos.png",
        mime="image/png",
    )
else:
    st.info("Esperando que subas una imagen...")
