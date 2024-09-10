import os
import pandas as pd


# find the common columns in all csv files from data folder and put it in a list to preserve the column order
common_columns = []
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    df = pd.read_csv(filepath)
    if not common_columns:
        common_columns = list(df.columns)
    else:
        common_columns = [col for col in common_columns if col in df.columns]

print(common_columns)
print(len(common_columns))


# PMerge file
dfs = []
first_file = True
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    df = pd.read_csv(filepath)
    dfs.append(df)

# save dfs into a merge csv file in data folder
merged_df = pd.concat(dfs, ignore_index=True)
merged_df = merged_df[common_columns]
merged_filepath = os.path.join("data", "merge.csv")
merged_df.to_csv(merged_filepath, index=False)
print(f"Merged file saved as merge.csv in data folder")

