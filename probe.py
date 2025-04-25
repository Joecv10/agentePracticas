import re, pandas as pd, textwrap

df = pd.read_excel("files/encuesta.xlsx")   # keep your path

# Grab the ordered list of column names
cols = df.columns.tolist()

for i, col in enumerate(cols):
    if col.startswith("Indicador_"):
        # look ahead until the next Indicador_ or end of list
        j = i + 1
        while j < len(cols) and not cols[j].startswith("Indicador_"):
            j += 1
        block = cols[i:j]
        print(f"{col}  →  {len(block)} columnas")
        print(textwrap.indent('\n'.join(block[:4]), prefix="   "))
        print("   …\n")