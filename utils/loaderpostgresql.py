import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os


class Loader:
    def __init__(self, teams_file, matches_file, match_stats_file, db_params):
        self.teams_file = teams_file
        self.matches_file = matches_file
        self.match_stats_file = match_stats_file
        self.db_params = db_params


    def load_csv_to_sqlite(self):
        teams_df = pd.read_csv(self.teams_file)
        matches_df = pd.read_csv(self.matches_file)
        match_stats_df = pd.read_csv(self.match_stats_file)
        
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        def insert_dataframe(df, table_name):
            cols = ', '.join(df.columns)
            values = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"
            data = [tuple(row) for row in df.values]
            execute_values(cur, insert_query, data)

        insert_dataframe(teams_df, 'teams')
        insert_dataframe(matches_df, 'matches')
        insert_dataframe(match_stats_df, 'match_statistics')

        conn.commit()
        cur.close()
        conn.close()
        
        print("Data has been loaded into POSTGRESQL database successfully")
