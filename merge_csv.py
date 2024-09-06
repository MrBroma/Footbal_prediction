import os
import pandas as pd




# find the common columns in all csv files from data folder and put it in a variable
common_columns = set()
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    df = pd.read_csv(filepath)
    common_columns = common_columns.intersection(set(df.columns)) if common_columns else set(df.columns)

print(common_columns)
print(len(common_columns))











