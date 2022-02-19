import openpyxl
import pandas as pd

workbook = openpyxl.load_workbook("data/phidu_Indigenous_status_comparison_data_ia_aust.xlsm", read_only = True, data_only = True)
name_linkage = pd.read_csv("data/index_linkage.csv")

focus = workbook["Families"]
df = pd.DataFrame(focus.values)
# Victoria filter
Vic_list = []
Vic_iare = list(name_linkage.iloc[:, 1])
for iare in list(df.iloc[:, 0]):
    if iare in Vic_iare:
        Vic_list.append(True)
    else:
        Vic_list.append(False)


# Low income families
focus = workbook["Families"]
df = pd.DataFrame(focus.values)
columns = [0, 1, 11, 14]
Vic_df = df[Vic_list]
income = Vic_df.iloc[:, columns]
column_name = ["iare_code", "Indigenous Area name", "Indigenous low-income family rate", "Non-indigenous low-income family rate"]
income.columns = column_name
income.index = range(39)

# Unemployment
focus = workbook["Labour_force"]
df = pd.DataFrame(focus.values)
columns = [4, 7]
Vic_df = df[Vic_list]
unemployment = Vic_df.iloc[:, columns]
column_name = ["Indigenous unemployment rate", "Non-indigenous unemployment rate"]
unemployment.columns = column_name
unemployment.index = range(39)
resources = pd.concat([income, unemployment], axis=1)

# Primary_school dropout rate
focus = workbook["Education"]
df = pd.DataFrame(focus.values)
columns = [10, 14]
Vic_df = df[Vic_list]
primary_school_dropout = Vic_df.iloc[:, columns]
column_name = ["Indigenous Primary-school dropout ASR_per_100", "Non-indigenous Primary-school dropout ASR_per_100"]
primary_school_dropout.columns = column_name
primary_school_dropout.index = range(39)
resources = pd.concat([resources, primary_school_dropout], axis=1)

# Middle_school participation
focus = workbook["Education"]
df = pd.DataFrame(focus.values)
columns = [20, 23]
Vic_df = df[Vic_list]
middle_school_participation = Vic_df.iloc[:, columns]
column_name = ["Indigenous middle_school_participation rate", "Non-indigenous middle_school_participation rate"]
middle_school_participation.columns = column_name
middle_school_participation.index = range(39)
resources = pd.concat([resources, middle_school_participation], axis=1)

# Internet access
focus = workbook["Internet"]
df = pd.DataFrame(focus.values)
columns = [11, 14]
Vic_df = df[Vic_list]
internet_access = Vic_df.iloc[:, columns]
column_name = ["Indigenous internet access rate", "Non-indigenous internet access rate"]
internet_access.columns = column_name
internet_access.index = range(39)
resources = pd.concat([resources, internet_access], axis=1)

# Social engagement
focus = workbook["Learning_or_Earning"]
df = pd.DataFrame(focus.values)
columns = [4, 7]
Vic_df = df[Vic_list]
social_participation = Vic_df.iloc[:, columns]
column_name = ["Indigenous social engagement rate", "Non-indigenous social engagement rate"]
social_participation.columns = column_name
social_participation.index = range(39)
resources = pd.concat([resources, social_participation], axis=1)

resources.to_csv("data/indigenous_cleanse.csv", index=False)
