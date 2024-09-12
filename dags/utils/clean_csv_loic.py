import os
import pandas as pd

def clean():
    # Path to the folder containing the CSV files
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    # Iterate through all the CSV files in the folder
    for file in os.listdir(data_folder):
        if file.endswith('.csv'):
            file_path = os.path.join(data_folder, file)
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Check for completely empty rows
            rows_before = len(df)
            df = df.dropna(how='all')  # Remove completely empty rows
            rows_after = len(df)
            
            # If rows have been removed, save the modified file
            if rows_before != rows_after:
                df.to_csv(file_path, index=False)
                print(f"Empty rows removed in: {file}")

    print("Processing completed.")

