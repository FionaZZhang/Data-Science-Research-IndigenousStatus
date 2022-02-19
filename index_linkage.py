import pandas as pd
import openpyxl
import numpy as np
import re

phidu_file = r"data/phidu_Indigenous_status_comparison_data_ia_aust.xlsm"
state = "2"

abs_file = r"data/socio-eco index.xlsm"
code_col = '2016 Statistical Area Level 1  (SA1) 7-Digit Code'
primary_col = '2016 Local Government Area (LGA) Name'
secondary_col = '2016 Statistical Area Level 2 (SA2) Name'
sheet = -2
state_col = '2016 State/Territory Name'
state_name = 'Victoria'

critical_sim = 0.6


def process(x):
    stop_words=['west','east','south','north']
    rule=re.compile('(('+'|'.join(stop_words)+').{0,1}-)'+'|'+'(-.{0,1}('+'|'.join(stop_words)+'))')
    result=re.findall(rule,x.lower())
    if len(result)!=0:
        return [[i for i in x.replace('-',' ').split(' ') if i!='']]
    else:
        return [[i for i in sub.replace('-',' ').split(' ') if i!=''] for sub in x.split(' - ')]

def process2(x):
    x=x.replace('-',' ')
    return [i for i in x.split(' ') if i !='']


# extract area name list from PHIDU dataset
phidu_df = pd.read_excel(phidu_file, engine='openpyxl', sheet_name= "Males").iloc[4:412, ]
phidu_df["if_victoria"] = phidu_df.iloc[:, 0].apply(lambda x: x[4] == state)
phidu_df = phidu_df.loc[phidu_df["if_victoria"] == True, :].iloc[:, [0, 1]]
phidu_df.columns = ["iare_code", "iare_name"]
phidu_df['name_process'] = phidu_df['iare_name'].apply(lambda x: process(x))
phidu_df['abs_code'] = 0
phidu_df['abs_name'] = ''
phidu_df['len'] = phidu_df['iare_name'].apply(lambda x:len(x))
phidu_df.sort_values(by=['len'] , axis = 0 , inplace = True, ascending = False)

# extract name and id list from ABS dataset
work_book = openpyxl.load_workbook(abs_file, read_only = True, data_only = True)
sheet_names = work_book.sheetnames
work_sheet = work_book[sheet_names[sheet]]
abs_df = pd.DataFrame(work_sheet.values)
abs_df.columns = abs_df.iloc[4, :]
abs_df = abs_df.loc[abs_df[state_col] == state_name, [code_col,primary_col,secondary_col]]
abs_df.dropna(inplace=True)
abs_df['used'] = 0

# initialize
phidu_df['abs_name']=''
abs_df['used'] = 0

# matching
for row in phidu_df.index:
    total_code_list=[]
    for phidu_name in phidu_df.loc[row, 'name_process']:
        col_id = 1
        code_list = []
        while col_id < 3 and not code_list:
            candidate_list=[i for i in list(abs_df.loc[abs_df['used'] ==0,abs_df.columns[col_id]].unique())]
            process_list= [process2(i.split('(')[0]) for i in candidate_list]
            similarity = [2*len(set(phidu_name)&set(abs_name)) /(len(set(phidu_name))+len(set(abs_name))) for abs_name in process_list]
            if max(similarity) >= critical_sim:
                index=abs_df[abs_df.columns[col_id]] == candidate_list[np.argmax(similarity)]
                phidu_df.loc[row, 'abs_name'] += ', ' + candidate_list[np.argmax(similarity)]
                abs_df.loc[index, 'used'] += 1
                code_list = list(abs_df.loc[index, code_col])
                total_code_list += code_list
            col_id += 1
    phidu_df.loc[row, 'abs_code'] = str(total_code_list)
phidu_df['abs_name']=phidu_df['abs_name'].apply(lambda x:x.strip(', '))

# impute some missige values
code_list=list(abs_df.loc[abs_df[secondary_col]=='North Melbourne',code_col])
phidu_df.loc[phidu_df['iare_name']=='Melbourne - North-East','abs_code']=str(code_list)
phidu_df.loc[phidu_df['iare_name']=='Melbourne - North-East','abs_name']=str(code_list)
code_list=list(abs_df.loc[abs_df[secondary_col]=='East Melbourne',code_col])
phidu_df.loc[phidu_df['iare_name']=='Melbourne - East','abs_code']=str(code_list)

phidu_df.to_csv("data/index_linkage.csv") 