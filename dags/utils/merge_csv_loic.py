import os
import pandas as pd

def merge_sorting():
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    # find the common columns in all csv files from data folder and put it in a list to preserve the column order
    common_columns = []
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        df = pd.read_csv(filepath)
        if not common_columns:
            common_columns = list(df.columns)
        else:
            common_columns = [col for col in common_columns if col in df.columns]

    # Merge file
    dfs = []
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        df = pd.read_csv(filepath)
        dfs.append(df)

    # save dfs into a merge csv file in data folder
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df = merged_df[common_columns]
    
    # Handle mixed date formats
    merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce')

    # sort the values by Date and Time in descending order
    merged_df = merged_df.sort_values(by=['Date', 'Time'], ascending=False)

    # save the sorted dataframe in a new csv file
    merged_df.to_csv(os.path.join(data_folder, 'final_data_sorted.csv'), index=False)

