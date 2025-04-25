from datetime import datetime, date
import os, json, openai, pandas as pd, helpers

openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------- directory & filename -------------
reports_dir = "reports"
os.makedirs(reports_dir, exist_ok=True)          # create if missing

stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
out_file = os.path.join(reports_dir, f"Informe_Indicador_91_{stamp}.docx")

df = pd.read_excel("files/encuesta.xlsx") 
block91 = helpers.get_block(df, 91)

# Parse every non‑empty row
rows = [helpers.parse_row(block91.iloc[i])
        for i in range(len(block91))
        if str(block91.iloc[i, 0]).strip().lower().startswith(("si", "sí"))]  # keep rows that responded "Sí"

agg = helpers.aggregate_rows(rows)

# Quick sanity check
print("Carreras incluidas:", agg["n_carreras"])
print("Total estudiantes:", agg["n_estudiantes_total"])
print("Primeras 3 actividades:", agg["actividades"][:3])

# ---------- LLM prompt ----------
prompt_system = "Eres un redactor académico. Usa el estilo formal del informe adjunto."
prompt_user = f"""Genera un INFORME del INDICADOR 91, sintetizando la participación de
{agg['n_carreras']} carreras de la Escuela Superior Politécnica de Chimborazo.

Datos agregados (JSON resumido):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Reglas:
-El titulo del informe debe ser Indicador 91, nada mas.
- No repitas “Indicador 91”.
- Incluye secciones INTRODUCCIÓN, ACTIVIDADES, OBJETIVOS, ACTORES, RESULTADOS, CONCLUSIONES, RECOMENDACIONES.
- No hagas listas interminables: si hay muchas actividades u objetivos, agrúpalos temáticamente.
- Menciona totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos, solo en la sección de ACTORES, y redactalos en parrafos no en items.
- Escribe en español, tono formal.
- Usa viñetas o párrafos breves, según corresponda.
- Si un campo está vacío, omítelo elegantemente.
-Las conclusiones redactales en forma de items no de párrafos.
-Los resultados redactalos en forma de párrafos no de items.
"""

resp = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user",   "content": prompt_user}
    ],
    temperature=0.4
)


report_text = resp.choices[0].message.content
print(resp.choices[0].message.content)    

# today = date.today().strftime("%Y-%m-%d")
# out_file = f"Informe_Indicador_91_{today}.docx"
helpers.save_report_to_docx(report_text, out_file)