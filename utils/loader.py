import pandas as pd
import sqlite3
import os


class Loader:
    def __init__(self, teams_file, matches_file, match_stats_file, db_file):
        self.teams_file = teams_file
        self.matches_file = matches_file
        self.match_stats_file = match_stats_file
        self.db_file = db_file


    def load_csv_to_sqlite(self):
        teams_df = pd.read_csv(self.teams_file)
        matches_df = pd.read_csv(self.matches_file)
        match_stats_df = pd.read_csv(self.match_stats_file)
        
        conn = sqlite3.connect(self.db_file)

        teams_df.to_sql('teams', conn, if_exists='append', index=False)
        matches_df.to_sql('matches', conn, if_exists='append', index=False)
        match_stats_df.to_sql('match_statistics', conn, if_exists='append', index=False)

        conn.close()
        
        print("Data has been loaded into SQLite database successfully")
