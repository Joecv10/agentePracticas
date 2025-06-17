import json
import pandas as pd
import helpers

# -------- Prompt exclusivo para el Indicador 91 --------


def build_prompt_91(agg: dict) -> str:
    return f"""Genera un **INFORME EJECUTIVO** del *Indicador 91*.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Instrucciones de formato:
- El TÍTULO debe ser solo “Indicador 91”.
- Estructura obligatoria, en este orden:
    1. INTRODUCCIÓN (párrafo breve)
    2. ACTIVIDADES REALIZADAS (lista breve)
    3. OBJETIVOS DE LAS ACTIVIDADES (lista)
    4. ESTRATEGIAS IMPLEMENTADAS Y RESULTADOS (lista numerada; cada ítem: **Estrategia** en negrita + guion con *Resultado* alineado)
    5. ACTORES (lista detallada con descripción breve; incluye estudiantes, docentes, administrativos, graduados, externos, etc.)
    6. CONCLUSIONES (ítems)
    7. RECOMENDACIONES (ítems)

Reglas adicionales:
- En ACTORES incluye totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
- Sé preciso pero conciso; omite campos vacíos.
- Tono formal, español académico.
"""

# -------- Prompt exclusivo para el Indicador 92 --------


def build_prompt_92(agg):
    return f"""Genera un INFORME del INDICADOR 92, sintetizando la participación de
{agg['n_carreras']} carreras.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Estructura:
1. INTRODUCCIÓN
2. ACTIVIDADES
3. OBJETIVOS
4. ACTORES (totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos)
5. RESULTADOS
   ↳ ***Sub-sección: Seguimiento y evaluación del acompañamiento académico***
6. CONCLUSIONES
7. RECOMENDACIONES

Reglas:
- El título debe ser 'Indicador 92' y no repetir ese nombre en el cuerpo.
- RESULTADOS en párrafos; CONCLUSIONES y RECOMENDACIONES en ítems.
- En la sub-sección de seguimiento, destaca indicadores (ej. porcentaje de asistencia a tutorías, mejora en calificaciones, retención) y compara antes/después si hay datos.
- Omite campos vacíos; tono formal, español académico."""

# -------- Prompt exclusivo para el Indicador 94 --------


def build_prompt_94(agg):
    return f"""Genera un INFORME del *Indicador 94*.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Estructura obligatoria:
1. INTRODUCCIÓN
2. ACTIVIDADES DE SOCIALIZACIÓN
3. OBJETIVOS
4. COBERTURA DE LA SOCIALIZACIÓN
   - Incluye porcentajes y números de docentes, estudiantes y administrativos capacitados.
5. FORMATOS Y CANALES UTILIZADOS
   - Ej.: talleres presenciales, webinars, infografías, correo institucional.
6. EVALUACIÓN DE COMPRENSIÓN
   - Describe encuestas o pruebas aplicadas y sus resultados (porcentajes de aciertos, feedback).
7. IMPACTO INICIAL Y RESULTADOS
   - Cambios observados tras la socialización (reducción de dudas, mejoras en documentos de titulación, etc.).
8. ACTORES
   - Lista detallada con descripción breve; totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
9. CONCLUSIONES (ítems)
10. RECOMENDACIONES (ítems)

Reglas:
- Título exactamente “Indicador 94”.
- No repitas el nombre fuera del título.
- Usa un tono formal y español académico.
- Listas claras; evita listas excesivamente largas agrupando elementos.
- Omite secciones vacías con elegancia.
"""


# -------- Prompt exclusivo para el Indicador 95 --------
def build_prompt_95(agg):
    return f"""Genera un INFORME del *Indicador 95*.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Estructura obligatoria:
1. INTRODUCCIÓN
2. ACTIVIDADES RELACIONADAS
3. OBJETIVOS
4. PROCESO DE TITULACIÓN
   4.1 **Planificación**
       - Describe cronogramas, recursos asignados y preparación de lineamientos.
   4.2 **Ejecución**
       - Detalla acciones llevadas a cabo (tutorías, talleres, mesas de revisión, etc.).
   4.3 **Seguimiento**
       - Explica mecanismos de control de avance (reuniones de progreso, paneles de control, plataformas).
   4.4 **Evaluación**
       - Presenta métricas: tiempos promedio de culminación, tasas de aprobación, retroalimentación de evaluadores.
5. RESULTADOS
   - Síntesis de logros: reducción del tiempo de titulación, aumento de tasas de defensa exitosa, etc.
6. ACTORES
   - Lista detallada con descripción; totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
7. CONCLUSIONES (ítems)
8. RECOMENDACIONES (ítems)

Reglas:
- El título debe ser 'Indicador 95' y no repetir ese nombre en el cuerpo.
- RESULTADOS en párrafos; CONCLUSIONES y RECOMENDACIONES en ítems.
- Omite campos vacíos; tono formal, español académico.
"""

# -------- Prompt exclusivo para el Indicador 96 --------


def build_prompt_96(agg):
    return f"""Genera un INFORME del *Indicador 96*.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Estructura obligatoria:
1. INTRODUCCIÓN
2. ACTIVIDADES MOTIVACIONALES IMPLEMENTADAS
3. OBJETIVOS
4. IMPACTO EN LA TASA DE TITULACIÓN
   4.1 **Tasa de titulación de grado**
       - Incluye porcentaje actual y variación respecto al periodo anterior.
   4.2 **Tasa de titulación de posgrado**
       - Igual formato que grado.
   4.3 **Tendencia comparativa**
       - Breve análisis gráfico o textual antes / después de las actividades.
5. FACTORES MOTIVACIONALES IDENTIFICADOS
   - Enumera elementos que influyen positivamente (orientación, incentivos económicos, mentorías, etc.).
6. RESULTADOS
   - Describe logros cuantitativos y cualitativos derivados de las actividades.
7. ACTORES
   - Lista detallada con descripción; totales: {agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos.
8. CONCLUSIONES (ítems)
9. RECOMENDACIONES (ítems)

Reglas:
- El título debe ser 'Indicador 96' y no repetir ese nombre en el cuerpo.
- RESULTADOS en párrafos; CONCLUSIONES y RECOMENDACIONES en ítems.
- Incluye tasas de titulación en porcentaje (grado y posgrado) siempre que los datos estén disponibles en el JSON; si faltan, indica “Dato no disponible”.
- Tono formal, español académico. Omite secciones vacías con elegancia.
"""


# -------- Prompt genérico para el resto --------
def build_prompt_generic(num: int, agg: dict) -> str:
    return f"""Genera un INFORME del INDICADOR {num}, sintetizando la participación de
{agg['n_carreras']} carreras.

Datos agregados (JSON):
{json.dumps(agg, ensure_ascii=False, indent=2)}

Reglas:
- El título debe ser 'Indicador {num}'.
- Incluye secciones INTRODUCCIÓN, ACTIVIDADES, OBJETIVOS, ACTORES, RESULTADOS, CONCLUSIONES, RECOMENDACIONES.
- En ACTORES indica totales ({agg['n_estudiantes_total']} estudiantes, {agg['n_docentes_total']} docentes, {agg['n_administrativos_total']} administrativos) en párrafo.
- Resultados en párrafos; conclusiones en ítems; agrupa si son muchos.
- Omite campos vacíos; tono formal.
"""

# -------- Dispatcher --------


def build_prompt(num: int, agg: dict) -> str:
    if num == 91:
        return build_prompt_91(agg)
    # aquí puedes añadir más if num == 92, etc.
    if num == 92:
        return build_prompt_92(agg)

    if num == 94:
        return build_prompt_94(agg)

    if num == 95:
        return build_prompt_95(agg)

    if num == 96:
        return build_prompt_96(agg)

    return build_prompt_generic(num, agg)
