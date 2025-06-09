import os, json, openai, pandas as pd, helpers

def build_prompt(num: int, agg: dict) -> str:
    """Returns the user prompt string — unchanged from earlier logic."""
    return f"""Genera un INFORME del INDICADOR {num}, sintetizando la participación de
{agg['n_carreras']} carreras de la Escuela Superior Politécnica de Chimborazo.

Datos agregados (JSON resumido):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Reglas:
- El título del informe debe ser 'Indicador {num}', nada más.
- No repitas “Indicador {num}” fuera del título.
- Incluye secciones INTRODUCCIÓN, ACTIVIDADES, OBJETIVOS, ACTORES, RESULTADOS, CONCLUSIONES, RECOMENDACIONES.
- En ACTORES redacta un párrafo con los totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
- Resultados en párrafos; conclusiones en ítems; agrupa actividades/objetivos si son muchos.
- Omite con elegancia campos vacíos. Escribe en español, tono formal.
"""
# -------------------------------------------------