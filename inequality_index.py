import pandas as pd
import numpy as np

def develop_level(array1, array2):
    result_array = array1 / array2
    return result_array

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm


df = pd.read_csv("data/indigenous_cleanse.csv")

info = df.iloc[:, [0,1]]
income_inequality = develop_level(df.iloc[:, 2], df.iloc[:, 3])
unemployment_inequality = develop_level(df.iloc[:, 4], df.iloc[:, 5])
Primary_school_dropout_inequality = develop_level(df.iloc[:, 6], df.iloc[:, 7])
middle_school_participation_equality = develop_level(df.iloc[:, 8], df.iloc[:, 9])
internet_access_equality = develop_level(df.iloc[:, 10], df.iloc[:, 11])
social_engagement_equality = develop_level(df.iloc[:, 12], df.iloc[:, 13])
data_dict = {"income inequality": income_inequality, "unemployment inequality": unemployment_inequality, "Primary-school dropout inequality": Primary_school_dropout_inequality,
            "middle-school participation equality": middle_school_participation_equality, "internet access equality": internet_access_equality, "social engagement equality": social_engagement_equality}
inequality_df = pd.DataFrame(data_dict)
inequality_index = pd.concat([info, inequality_df], axis=1)

inequality_index.to_csv("data/inequality_index_unormalised.csv", index=False)

# Normalize
inequality_index.iloc[:, 2:8] = inequality_index.iloc[:, 2:8].apply(normalize)

inequality_index.to_csv("data/inequality_index.csv", index=False)