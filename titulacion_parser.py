from pathlib import Path
import pandas as pd
import re


def _find(df_cols, pattern: str):
    """Devuelve la primera columna cuyo nombre contiene el patrón (case-insensitive)."""
    pat = re.compile(pattern, re.I)
    for col in df_cols:
        if pat.search(col):
            return col
    raise KeyError(f"Columna con patrón '{pattern}' no encontrada")


def parse_titulacion_excel(path: str | Path):
    """
    Lee el Excel de titulación (formato 95) y devuelve:
      table1, table2, text_fields
    """
    df = pd.read_excel(path, sheet_name=0,
                       header=4)  # encabezados en la 5ª fila

    # ---- columnas base ------------------------------------------------------
    col_id = _find(df.columns, r'^Id$')
    col_carrera = _find(df.columns, r'CARRERA')
    col_sede = _find(df.columns, r'sede es su Carrera')

    # ---- columnas tabla 1 ----------------------------------------------------
    col_matric = _find(
        df.columns, r'matricularon.*TRABAJO DE TITULACIÓN.*periodo')
    col_aprob = _find(df.columns, r'aprobaron.*TRABAJO DE TITULACIÓN.*periodo')

    table1 = df[[col_id, col_carrera, col_sede, col_matric, col_aprob]].copy()
    table1.rename(columns={
        col_matric: 'Estudiantes matriculados',
        col_aprob:  'Estudiantes aprobados'
    }, inplace=True)
    table1['Porcentaje de aprobación [%]'] = (
        table1['Estudiantes aprobados'] * 100 /
        table1['Estudiantes matriculados']
    ).round(2)

    # ---- columnas tabla 2 ----------------------------------------------------
    col_complex = _find(df.columns, r'EXAMEN COMPLEXIVO')
    col_emprend = _find(df.columns, r'EMPRENDIMIENTO')
    col_tt = _find(df.columns, r'realizaron TRABAJO DE TITULACIÓN')

    table2 = df[[col_id, col_carrera, col_sede,
                 col_complex, col_emprend, col_tt]].copy()
    table2.rename(columns={
        col_complex: 'Examen complexivo',
        col_emprend: 'Emprendimiento',
        col_tt:      'Trabajo de titulación'
    }, inplace=True)

    # ---- extraer textos de acciones / mejoras --------------------------------
    col_planif = _find(df.columns, r'planificaci')   # planificación
    col_ejec = _find(df.columns, r'ejecuci')       # ejecución
    col_seguim = _find(df.columns, r'seguim')        # seguimiento
    col_mejora = _find(df.columns, r'mejora')        # acciones de mejora

    text_fields = {
        'planificacion': df[col_planif].dropna().tolist(),
        'ejecucion':     df[col_ejec].dropna().tolist(),
        'seguimiento':   df[col_seguim].dropna().tolist(),
        'mejoras':       df[col_mejora].dropna().tolist(),
    }

    return table1, table2, text_fields
