from numpy.random import randn
from numpy.random import seed
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import csv
import pandas as pd

# read data
socio_name = "data/integrate_abs_data.csv"
equality_name = "data/inequality_socioeco.csv"
socio_data = pd.DataFrame(pd.read_csv(socio_name))
equality_data = pd.read_csv(equality_name)


# pearson correlation value
pearson_value = []

for i in range(1,9):
    x = socio_data.iloc[:,i]
    pearson_row = []
    for j in range(2,8):
        y = equality_data.iloc[:,j]
        corr, _ = pearsonr(x, y)
        pearson_row.append(round(corr,2))
        
    pearson_value.append(pearson_row)
    
pearson_data = pd.DataFrame(pearson_value)
pearson_data.index = socio_data.columns[1:9]
pearson_data.columns = equality_data.columns[2:8]

# create heatmap
fig = plt.figure(figsize=(6,6))
plt.title("Pearson Correlation Values")
cmap = sns.diverging_palette(240,240, as_cmap=True)
hm = sns.heatmap(pearson_data, cmap=cmap, annot = True, annot_kws={"size": 7}, xticklabels = True, yticklabels = True)

hm.set_xticklabels(hm.get_xticklabels(), rotation=90, size = 7) 
hm.set_yticklabels(hm.get_yticklabels(), rotation=65, size = 7)

plt.xlabel("(in)equality index")
plt.ylabel("socio-economic status index")
plt.tight_layout()
plt.savefig("data/pearson_heatmap.png")
plt.close()


    
