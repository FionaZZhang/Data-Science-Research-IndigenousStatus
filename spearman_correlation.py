import pandas as pd
import os
from patsy import dmatrix
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import statsmodels.formula.api as smf

df=pd.read_csv('data/inequality_socioeco.csv',index_col=0,header=0)
df=df[df.notnull().all(axis=1)]
y_total=df.iloc[:,1:7]
x=df.iloc[:,7:].iloc[:,list(range(0,9,2))]
x.columns=['S-E disad score','S-E ad & disad score','Eco Resources Score','Edu & Occupation Score','Population']
y=y_total.iloc[:,[0]]
scaler = StandardScaler()
y=scaler.fit_transform(y)
scaler = StandardScaler()
x=pd.DataFrame(scaler.fit_transform(x),columns=x.columns)
poly = PolynomialFeatures(degree = 2)
x_poly = pd.DataFrame(poly.fit_transform(x),columns=poly.get_feature_names(x.columns))
model=sm.OLS(y,x_poly).fit()
# print(model.summary())
plt.plot(y_total.index,y,label='actual',color='blue')
plt.plot(y_total.index,model.predict(x_poly),label='pred',color='orange')
plt.legend()

x_poly.loc[:,model.pvalues<=0.1]

best_model=sm.OLS(y,x_poly.loc[:,model.pvalues<=0.1]).fit()
plt.plot(y_total.index,y,label='actual',color='blue')
plt.plot(y_total.index,best_model.predict(x_poly.loc[:,model.pvalues<=0.1]),label='pred',color='orange')
plt.legend()

x_poly.reset_index(drop=True, inplace=True)
y_total.reset_index(drop=True, inplace=True)
sp_cor=pd.concat([x_poly.iloc[:,1:],y_total],axis=1).corr('spearman').iloc[-6:,:-6]

plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(1, figsize=(20, 8))
fig.set_tight_layout(True)
sns.heatmap(sp_cor, cmap='RdBu', linewidths=0.05,annot=True)
plt.title('Spearman Correlation Values')
plt.savefig('data/spearman_heatmap.png')
