# run_all_indicadores.py
from datetime import datetime
import os, json, openai, pandas as pd, helpers
from openai_utils import chat_completion_with_retry 
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

# --------- configuración ----------
INDICADORES      = [91, 92, 93, 94, 95, 96]
EXCEL_FILE       = "files/encuesta.xlsx"   # ruta al archivo
REPORTS_DIR      = "reports"
MODEL            = "gpt-4o-mini"              # ajusta si quieres
TEMPERATURE      = 0.4
os.makedirs(REPORTS_DIR, exist_ok=True)
# -----------------------------------

df = pd.read_excel(EXCEL_FILE)

for num in INDICADORES:
    try:
        block = helpers.get_block(df, num)
    except ValueError:
        print(f"⚠️  Indicador {num} no encontrado, se omite.")
        continue

    # — filtramos carreras que respondieron "Sí" (ajusta si procede) —
    rows = [
        helpers.parse_row(block.iloc[i])
        for i in range(len(block))
        if str(block.iloc[i, 0]).strip().lower().startswith(("si", "sí"))
    ]
    if not rows:
        print(f"⚠️  Indicador {num}: sin filas válidas, se omite.")
        continue

    agg = helpers.aggregate_rows(rows)

    # ---------- prompt ----------
    prompt_system = "Eres un redactor académico. Usa el estilo formal del informe adjunto."
    prompt_user = f"""Genera un INFORME del INDICADOR {num}, sintetizando la participación de
{agg['n_carreras']} carreras de la Escuela Superior Politécnica de Chimborazo.

Datos agregados (JSON resumido):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Reglas:
- El título del informe debe ser 'Indicador {num}', nada más.
- No repitas “Indicador {num}” fuera del título.
- Incluye secciones INTRODUCCIÓN, ACTIVIDADES, OBJETIVOS, ACTORES, RESULTADOS, CONCLUSIONES, RECOMENDACIONES.
- En ACTORES redacta un párrafo con los totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
- Resultados en párrafos; conclusiones y recomendaciones en ítems sin numeración; agrupa actividades/objetivos si son muchos.
- Omite con elegancia campos vacíos. Escribe en español, tono formal.
"""

    # resp = openai.chat.completions.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": prompt_system},
    #         {"role": "user",   "content": prompt_user},
    #     ],
    #     temperature=TEMPERATURE,
    # )
    # report_text = resp.choices[0].message.content.strip()

    messages = [
    {"role": "system", "content": prompt_system},
    {"role": "user",   "content": prompt_user},
    ]

    report_text = chat_completion_with_retry(
    messages,
    model=MODEL,
    temperature=TEMPERATURE,
    max_retries=5,
    base_delay=2.0,
                    )

    # ---------- guardar DOCX ----------
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"Informe_Indicador_{num}_{stamp}.docx"
    path     = os.path.join(REPORTS_DIR, filename)
    helpers.save_report_to_docx(report_text, path)

    print(f"✅  Indicador {num}: informe listo → {path}")