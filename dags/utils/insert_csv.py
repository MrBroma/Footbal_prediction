import psycopg2
import pandas as pd
import os

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/final_data_sorted.csv")


def insert_data_to_db():
    df = pd.read_csv(csv_file_path)

    conn = psycopg2.connect(
        host="postgres",  
        database="football_prediction",
        user="airflow_user",
        password="airflow_password"
    )
    cur = conn.cursor()

    table_name = "football_stats"

    column_defs = []
    for column in df.columns:
        if df[column].dtype == 'object':
            column_type = "VARCHAR"
        elif 'int' in str(df[column].dtype):
            column_type = "INT"
        elif 'float' in str(df[column].dtype):
            column_type = "FLOAT"
        else:
            column_type = "VARCHAR"  

        column_defs.append(f'"{column}" {column_type}')

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"
    cur.execute(create_table_query)

    insert_query = f"INSERT INTO {table_name} ({', '.join([f'\"{col}\"' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"

    for row in df.itertuples(index=False, name=None):
        cur.execute(insert_query, row)

    conn.commit()

    cur.close()
    conn.close()

