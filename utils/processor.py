import pandas as pd
import os



class Processor():
    def __init__(self, input_file, output_directory):
        self.input_file = input_file
        self.output_directory = output_directory

    def process_and_save_csv(self):
    
        df = pd.read_csv(self.input_file)

        df = df.rename(columns={
            'AS': 'ASCR',
            'HS': 'HSCR'
        })

        df = df[['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR',
            'HTHG', 'HTAG', 'HTR', 'HSCR', 'ASCR', 'HST', 'AST', 'HF', 'AF', 'HC',
            'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD',
            'BWA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'MaxH', 'MaxD', 'MaxA',
            'AvgH', 'AvgD', 'AvgA']]

        teams = pd.DataFrame(pd.concat([df['HomeTeam'], df['AwayTeam']]).unique(), columns=['TeamName'])
        teams['TeamID'] = range(1, len(teams) + 1)
        teams = teams[['TeamID', 'TeamName']]

        team_mapping = dict(zip(teams['TeamID'], teams['TeamName']))
        
        matches = df[['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR']].copy()
        matches['MatchID'] = range(1, len(matches) + 1)

        matches['HomeTeamID'] = matches['HomeTeam'].map(team_mapping)
        matches['AwayTeamID'] = matches['AwayTeam'].map(team_mapping)

        matches = matches[['MatchID', 'Div', 'Date', 'Time', 'HomeTeamID', 'AwayTeamID', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR']]

        match_statistics = df[['HSCR', 'ASCR', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']].copy()
        match_statistics['MatchID'] = range(1, len(match_statistics) + 1)
        match_statistics = match_statistics[['MatchID', 'HSCR', 'ASCR', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        all_dataframes = {
            "teams.csv": teams,
            "matches.csv": matches,
            "match_statistics.csv": match_statistics,
        }    


        for filename, df in all_dataframes.items():
            file_path = os.path.join(self.output_directory, filename)
            df.to_csv(file_path, index = False)

        print("All CSV files have been created successfully in the new directory")   