import csv
from matplotlib import pyplot as plt
import pandas as pd
import openpyxl


# read data
socio_name = "data/integrate_abs_data.csv"
equality_name = "data/inequality_socioeco.csv"
equality_unorm = "data/inequality_index_unormalised.csv"
socio_data = pd.DataFrame(pd.read_csv(socio_name))
equality_data = pd.read_csv(equality_name)
equality_unorm_data = pd.read_csv(equality_unorm)

# Normalised plot------------------------------------------------------------

# create figure
fig = plt.figure(figsize=(9,9))

# generate a scatter plot including all inequality index for each socio-eco index, save as subplot to the figure
for i in range(1,9):
    x=socio_data.iloc[:,i]
    title = "(in)equality-index vs "+socio_data.columns[i]
    y_list=[]
    y_name=[]
    for j in range(2,8):
        y_list.append(equality_data.iloc[:,j])
        y_name.append(equality_data.columns[j])
    ax=fig.add_subplot(330+i)
    for j in range(0,6):
        ax.scatter(x,y_list[j],s=5)
    plt.xlabel(socio_data.columns[i], fontsize = 6.5)
    plt.tight_layout()
plt.title("(in)equality-index vs socio-eco index",y=3.42)
ax.legend(y_name, loc=(1.2,0.5), fontsize = 25, prop={'size': 7})
plt.savefig("data/scatter.png")

plt.close()

# Unormalised plot------------------------------------------------------------
# create figure
fig = plt.figure(figsize=(9,9))

# generate a scatter plot including all inequality index for each socio-eco index, save as subplot to the figure
for i in range(1,9):
    x=socio_data.iloc[:,i]
    title = "(in)equality-index vs "+socio_data.columns[i]
    y_list=[]
    y_name=[]
    for j in range(2,8):
        y_list.append(equality_unorm_data.iloc[:,j])
        y_name.append(equality_unorm_data.columns[j])
    ax=fig.add_subplot(330+i)
    for j in range(0,6):
        ax.scatter(x,y_list[j],s=5)
    plt.xlabel(socio_data.columns[i], fontsize = 6.5)
    plt.tight_layout()
plt.title("(in)equality-index vs socio-eco index",y=3.42)
ax.legend(y_name, loc=(1.2,0.5), fontsize = 25, prop={'size': 7})
plt.savefig("data/scatter(unormalised).png")

plt.close()
