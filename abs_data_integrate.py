import pandas as pd
import warnings
import os
import openpyxl
import json
import numpy as np
warnings.filterwarnings('ignore')

# read data
bureau_file_dir=r'data/socio-eco index.xlsm'
link_file_dir='data/index_linkage.csv'
workbook=openpyxl.load_workbook(bureau_file_dir, read_only = True, data_only = True)
sheet_names=workbook.sheetnames
del workbook
bureau_df=pd.read_excel(bureau_file_dir, engine = 'openpyxl', sheet_name=sheet_names[1],header=4,index_col=0)
bureau_df=bureau_df.loc[:,~bureau_df.isnull().all()]
link_df=pd.read_csv(link_file_dir,header=0,index_col=1).iloc[:,1:]

# matching
col_names=[]
main_name=''
for col in range(bureau_df.shape[1]):
    if not 'Unnamed' in bureau_df.columns[col]:
        main_name=bureau_df.columns[col]
    if (str(bureau_df.iloc[0,col]) != 'nan'):
        name=main_name+'_'+str(bureau_df.iloc[0,col])
    else:
        name = main_name
    col_names.append(name)
bureau_df.columns=col_names
bureau_df=bureau_df.iloc[1:,1:]

integrate_df=pd.DataFrame(0,index=link_df.index,columns=bureau_df.columns)
for ind in integrate_df.index:
    for col in integrate_df.columns:
        code_list=json.loads(link_df.loc[ind,'abs_code'])
        total_num=0
        for code in code_list:
            try:
                population=bureau_df.loc[code,bureau_df.columns[-1]]
                total_num+=population
                integrate_df.loc[ind,col]+= bureau_df.loc[code,col]*population
            except:
                continue
    integrate_df.loc[ind,:]=np.round(integrate_df.loc[ind,:]/total_num,2)
    integrate_df.loc[ind,bureau_df.columns[-1]]=total_num

# export to csv
integrate_df.to_csv(r'data/integrate_abs_data_raw.csv',header=True,index=True)

