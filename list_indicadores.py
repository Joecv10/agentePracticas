import re
import pandas as pd

# 1) Load the first sheet
df = pd.read_excel("files/encuesta.xlsx")  # adjust file name if needed

# 2) Scan every column name for a pattern like 'Indicador_91'
indicadores = set()
for col in df.columns:
    match = re.search(r"Indicador_[0-9]+", col)
    if match:
        indicadores.add(match.group())

# 3) Show what we found
for ind in sorted(indicadores):
    print(ind)
print(f"\nTotal encontrados: {len(indicadores)}")