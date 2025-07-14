import streamlit as st
import requests
import os
from typing import List, Dict
import pandas as pd

# ---------- CONFIG ----------- #
BACKEND_URL = os.getenv("BACKEND_URL", "https://localhost:8000")

st.set_page_config(
    page_title="Te escuchamos! Proporciona tu feedback sobre el servicio aquí.",
    page_icon="📢",
    layout="wide",
    menu_items={'About': 'Author: https://www.linkedin.com/in/xabidelrey/'}
    )

# ---------- FUNCTIONS ----------- #
def _inject_full_modal_css() -> None:
    """Expande el diálogo casi al ancho completo de la ventana (≈95 vw)."""
    st.markdown(
        """
        <style>
        /* Selecciona el contenedor principal del diálogo */
        [data-testid="stDialog"] > div:first-child {
            width: 95vw !important;
            max-width: 95vw !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_history(limit: int=20) -> List[Dict]:
    """Devuelve el histórico desde el backend.
    Si hay error, devuelve una lista vacía y deja el mensaje en st.error()."""
    try:
        r = requests.get(f"{BACKEND_URL}/history", params={"n": limit}, timeout=10)
        if r.status_code == 200:
            return r.json()
        st.error(f"Error {r.status_code} al obtener histórico.")
    except requests.exceptions.RequestException as e:
        st.error(f"No se pudo conectar a /history: {e}")
    return []


@st.dialog("Historial de feedback")
def mostrar_historial() -> None:
    """Muestra el historial de feedbacks en un modal."""
    _inject_full_modal_css()

    registros = get_history(50)
    if not registros:
        st.info("Aún no hay registros.")
        return

    df = pd.DataFrame(registros)
    
    # Formateamos fecha y renombramos columnas para legibilidad
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.tz_localize(None)
    st.dataframe(
        df[["fecha", "texto", "respuesta"]],
        use_container_width=True,
        height=500,
    )


# ----------------- HEADER ----------------- #
header_col, btn_col = st.columns([8, 2])
with header_col:
    st.title("💬 Asistente de Feedback")
with btn_col:
    st.button("📜 Historial", on_click=mostrar_historial, key="btn_historial")



# ---------- INPUT ----------- #
texto = st.text_area(
    "Proporciona tu feedback aquí:",
    placeholder = "escribe aquí tus sugerencias, dudas, problemas o cualquier otro feedback que quieras proporcionar sobre el servicio.",
    height = 150,
)

if st.button("Enviar", type="primary", key="btn_enviar"):
    texto_limpio = texto.strip()
    if not texto_limpio:
        st.warning("El campo de texto está vacío.")
    else:
        with st.spinner("generando respuesta..."):
            try:
                r = requests.post(
                    f"{BACKEND_URL}/feedback",
                    json={"texto": texto.strip()},
                    timeout=30,
                )
                if r.status_code == 200:
                    respuesta = r.json().get("respuesta", "(sin respuesta)")
                    st.success("Respuesta del asistente:")
                    st.write(respuesta)
                else:
                    st.error(f"Error {r.status_code}: {r.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"No se pudo conectar al backend: {e}")