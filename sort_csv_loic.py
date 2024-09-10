# load the merge.csv
import pandas as pd
df = pd.read_csv('data/merge.csv')

# change the date format of the column Date
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# sort the values by Date and Time in descending order
df = df.sort_values(by=['Date', 'Time'], ascending=False)

# save the sorted dataframe in a new csv file
df.to_csv('data/merge_sorted.csv', index=False)
print("File merge_sorted.csv saved in data folder")

