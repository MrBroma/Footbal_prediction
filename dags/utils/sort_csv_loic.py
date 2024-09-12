# load the merge.csv
import pandas as pd
import os


def sorting():

    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    df = pd.read_csv(os.path.join(data_folder, 'merge.csv'))

    # change the date format of the column Date
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # sort the values by Date and Time in descending order
    df = df.sort_values(by=['Date', 'Time'], ascending=False)

    # save the sorted dataframe in a new csv file
    df.to_csv(os.path.join(data_folder, 'final_data_sorted.csv'), index=False)
    print("File merge_sorted.csv saved in data folder")

