import pandas as pd
import os


class Merger:
        
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory



    def merge_csv_files(self):

        csv_files = [i for i in os.listdir(self.input_directory) if i.endswith('.csv')]    
        

        
        dataframes = [pd.read_csv(os.path.join(self.input_directory, file)) for file in csv_files]



        first_df_columns = dataframes[0].columns.tolist()
        common_columns = [col for col in  first_df_columns if all(col in df.columns for df in dataframes)]

        filtered_dataframes = [df[common_columns] for df in dataframes]
        merged_df = pd.concat(filtered_dataframes, ignore_index=True)
        merged_df = merged_df.dropna(how = 'all')

        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        output_file = os.path.join(self.output_directory, 'Merged_file_common_columns.csv')
        merged_df.to_csv(output_file, index= False)
        print(f"Merged CSV saved to: {output_file}")

    