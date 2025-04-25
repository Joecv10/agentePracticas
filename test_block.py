import pandas as pd, helpers

df = pd.read_excel("files/encuesta.xlsx") 

block91 = helpers.get_block(df, 91)

# show the tidy dict for the first career that answered 'Sí'
row0 = block91.iloc[0]
parsed = helpers.parse_row(row0)
print(parsed)