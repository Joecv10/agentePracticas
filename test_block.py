import pandas as pd
import helpers
from titulacion_parser import parse_titulacion_excel

# df = pd.read_excel("files/encuesta.xlsx")

# block91 = helpers.get_block(df, 91)

# # show the tidy dict for the first career that answered 'Sí'
# row0 = block91.iloc[0]
# parsed = helpers.parse_row(row0)
# print(parsed)

t1, t2, texts = parse_titulacion_excel("files/95_formato.xlsx")
print(t1.head())
print(t2.head())
print(texts['planificacion'][:3])
