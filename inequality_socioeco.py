import pandas as pd  

# Merge inequality_index and the socio-eco file
socio_eco = pd.read_csv("data/integrate_abs_data.csv")
inequality_index = pd.read_csv("data/inequality_index.csv")
inequality_socioeco = inequality_index.merge(socio_eco, on="iare_code", how="outer")
inequality_socioeco.to_csv("data/inequality_socioeco.csv", index=False)
