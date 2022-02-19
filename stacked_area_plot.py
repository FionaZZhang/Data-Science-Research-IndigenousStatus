import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv('data/inequality_socioeco.csv',index_col=0)
df=df[df.notnull().all(axis=1)]

phidu_df=df.iloc[:,1:7]

bureau_df=df.iloc[:,7:].iloc[:,list(range(0,9,2))]
for col in phidu_df.columns:
    if 'inequality' in col:
        phidu_df[col]=max(phidu_df[col])-phidu_df[col]
        phidu_df.rename(columns={col:'max-'+col},inplace=True)

def stack_area_plot(x,y):
    x=x.copy()
    x.sort_values(inplace=True)
    y=y.loc[x.index,:]
    y=(y - y.min()) / (y.max() - y.min())
    y_list=[y.iloc[:,i] for i in range(0,y.shape[1])]
    labels=y.columns
    palette = sns.color_palette("Spectral", y.shape[1]).as_hex()
    colors = ','.join(palette)
    fig,ax=plt.subplots(1,figsize=(20,10))
    ax.stackplot(x,y_list,labels=labels,colors=colors)
    ax.scatter(x,sum(y_list))
    ax.set_xlabel(pd.DataFrame(x).columns[0])
    plt.legend(loc="upper center", bbox_to_anchor=(1.1, 0.8), ncol=1)
    plt.show()

def stack_area_plot_loop(x_list,y):
    x_list=x_list.copy()
    fig, axes = plt.subplots(x_list.shape[1], figsize=(20, 20))
    fig.set_tight_layout(True)
    for id,col in enumerate(x_list.columns):
        x=x_list[col].copy()
        x.sort_values(inplace=True)
        y=y.loc[x.index,:]
        y=(y - y.min()) / (y.max() - y.min())
        y_list=[y.iloc[:,i] for i in range(0,y.shape[1])]
        labels=y.columns
        palette = sns.color_palette("Spectral", y.shape[1]).as_hex()
        colors = ','.join(palette)
        ax=axes[id]
        ax.stackplot(x,y_list,labels=labels,colors=colors)
        ax.scatter(x, sum(y_list))
        ax.set_xlabel(pd.DataFrame(x).columns[0])
        ax.legend(loc="upper center", bbox_to_anchor=(1.1, 0.8), ncol=1)
    plt.show()
stack_area_plot_loop(bureau_df,phidu_df)
plt.savefig('data/stacked_area_eq.png')
stack_area_plot_loop(phidu_df,bureau_df)
plt.savefig('data/stacked_area_sc.png')

