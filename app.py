import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile
import all_indicadores_reports as run_all_indicadores
import openai, os, hashlib

# provide your key via env var or st.secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Generador de Informes ESPOCH")

uploaded = st.file_uploader("📄 Sube el archivo de la encuesta (.xlsx)", type=["xlsx"])
# ---------- Identificador único del archivo subido ----------
def file_signature(file):
    # usa nombre + tamaño + md5 para evitar regenerar si es el mismo archivo
    m = hashlib.md5()
    m.update(file.getbuffer())
    return f"{file.name}-{file.size}-{m.hexdigest()}"

# ---------- Procesamiento solo si es un archivo NUEVO ----------

if uploaded:
    sig = file_signature(uploaded)

    # Generar solo si aún no está en session_state, o si cambió el archivo
    if st.session_state.get("last_sig") != sig:
        st.session_state["last_sig"] = sig
        st.session_state["reports"]  = None   # limpia antes

        with st.spinner("Procesando… esto puede tardar un momento"):
            # Guardar el archivo subido a un temp file
            tmp = NamedTemporaryFile(delete=False, suffix=".xlsx")
            tmp.write(uploaded.getbuffer())
            tmp.close()

            try:
                paths = run_all_indicadores.generate_reports(tmp.name)
                st.session_state["reports"] = paths
                st.success(f"Se generaron {len(paths)} informes.")
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
                st.stop()
    else:
        paths = st.session_state.get("reports", [])
    # Mostrar botones de descarga
    if paths:
        st.header("⬇️ Descargar informes")
        for p in paths:
            st.download_button(
                label=p.name,
                data=open(p, "rb").read(),
                file_name=p.name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )