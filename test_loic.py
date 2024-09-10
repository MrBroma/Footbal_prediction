

dfs = []
first_file = True
common_columns = None

# Iterate over all files in the "data" folder
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    
    # Read each CSV file into a DataFrame
    df = pd.read_csv(filepath)
    
    if first_file:
        # For the first file, save the columns to be used as reference
        common_columns = df.columns
        df = df[common_columns]  # Keep the columns in the order of the first file
        first_file = False
    else:
        # For subsequent files, retain only the columns present in the first file
        df = df.reindex(columns=common_columns)
    
    dfs.append(df)  # Add the processed DataFrame to the list

# Concatenate all DataFrames, ignoring the index to reset it
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_filepath = os.path.join("data", "merge.csv")
merged_df.to_csv(merged_filepath, index=False)

print(f"Merged file saved as merge.csv in data folder")
