import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np


socio_name = "data/integrate_abs_data_raw.csv"
socio_data = pd.DataFrame(pd.read_csv(socio_name))
new_data = socio_data
data = socio_data.iloc[:,1:]

imputer = SimpleImputer(missing_values = np.nan, strategy ='mean')
imputer = imputer.fit(data)
data = imputer.transform(data)
imputer = SimpleImputer(missing_values = 0, strategy ='mean')
imputer = imputer.fit(data)
data = imputer.transform(data)
data = pd.DataFrame(data,columns = new_data.columns[1:])

new_data.iloc[:,1:]=data
new_data.to_csv("data/integrate_abs_data.csv", index = False)


