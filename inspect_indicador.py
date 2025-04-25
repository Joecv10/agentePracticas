import re
import pandas as pd

target = "Indicador_91"          # <‑‑ change here if you want 92, 94…

df = pd.read_excel("files/encuesta.xlsx") 

# 1) Grab the columns that belong to this indicador
cols_for_target = [c for c in df.columns if target in c]

# Safety check
if not cols_for_target:
    raise ValueError(f"No se encontraron columnas para {target}")

sub_df = df[cols_for_target]

# 2) Print some quick info
print(f"{target}: {len(cols_for_target)} columnas\n")
print(sub_df.head(2).to_markdown())  # first 2 rows, Markdown table is readable