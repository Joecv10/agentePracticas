import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile
import all_indicadores_reports as run_all_indicadores
import titulacion_report
import openai
import os
import hashlib

# provide your key via env var or st.secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Generador de Informes del Decanato Académico de la ESPOCH")

# ---------- selector de tipo ----------
tipo_informe = st.radio("Tipo de informe",
                        ["Indicadores", "Titulación"], horizontal=True)   #

# ---------- uploader con key dinámico ----------
uploaded = st.file_uploader(
    "📄 Sube el archivo (.xlsx)",
    type=["xlsx"],
    # ← reset automático al cambiar de tipo
    key=f"uploader_{tipo_informe}"
)


# ---------- Identificador único del archivo subido ----------


def file_signature(file):
    # usa nombre + tamaño + md5 para evitar regenerar si es el mismo archivo
    m = hashlib.md5()
    m.update(file.getbuffer())
    # incluimos tipo_informe para disparar nuevo procesamiento si cambia
    return f"{file.name}-{file.size}-{m.hexdigest()}-{tipo_informe}"

# ---------- Procesamiento solo si es un archivo NUEVO ----------


if uploaded:
    sig = file_signature(uploaded)

    # Generar solo si aún no está en session_state, o si cambió el archivo
    if st.session_state.get("last_sig") != sig:
        st.session_state["last_sig"] = sig
        st.session_state["reports"] = None   # limpia antes

        # Mostrar spinner mientras se procesa
        progress_bar = st.progress(0, text="Iniciando…")

        # Función de actualización del progreso
        def on_progress(pct, msg):
            progress_bar.progress(pct, text=msg)

        with st.spinner("Procesando… esto puede tardar un momento"):
            # Guardar el archivo subido a un temp file
            tmp = NamedTemporaryFile(delete=False, suffix=".xlsx")
            tmp.write(uploaded.getbuffer())
            tmp.close()

            try:
                # ------------ dispatcher según tipo ------------
                if tipo_informe == "Indicadores":
                    paths = run_all_indicadores.generate_reports(
                        tmp.name, progress_update=on_progress)
                else:  # Titulación
                    path = titulacion_report.generate_report_titulacion(
                        tmp.name)
                    # lista para unificar
                    paths = [path]

                st.session_state["reports"] = paths
                progress_bar.progress(1.0, text="✔ Generación completa")
                st.success(f"Se generaron {len(paths)} informe(s).")

            except Exception as e:
                progress_bar.empty()
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
