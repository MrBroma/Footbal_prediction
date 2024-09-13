import pandas as pd
import psycopg2
import os

# Function to create the table if it doesn't exist
def create_table_if_not_exists(cursor, table_name, data):
    # Generate SQL query to create the table with column types based on pandas data types
    columns = data.columns
    column_types = ', '.join([f"{col} TEXT" for col in columns])  # Default to TEXT, can adjust based on dtype

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {column_types}
    );
    """
    cursor.execute(create_table_query)
    print(f"Table {table_name} created or verified!")

# Function to insert data into the PostgreSQL database
def insert_data_to_db():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="foot_prediction_db", 
            user="airflow_user", 
            password="airflow_password", 
            host="postgres",  # Ensure this matches your docker-compose service name
            port="5432"
        )
        cursor = connection.cursor()

        # Load CSV data with pandas
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/final_data_sorted.csv")
        data = pd.read_csv(csv_file, low_memory=False)
        table_name = "football_stats"

        # Create table if it doesn't exist
        create_table_if_not_exists(cursor, table_name, data)

        # Insert data using batch insert for efficiency
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(data.columns))})"
        cursor.executemany(insert_query, data.values.tolist())

        # Commit the transaction
        connection.commit()
        print("Data inserted into the database successfully!")

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except psycopg2.Error as db_error:
        print(f"Database error occurred: {db_error}")
    except Exception as error:
        print(f"An error occurred: {error}")

insert_data_to_db()
