import psycopg2
from psycopg2 import sql

# Connection to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="foot_prediction_db",  
            user="airflow_user",     
            password="airflow_password", 
            host="localhost",     
            port="5432"           
        )
        print("Successfully connected to the database!")
        return connection

    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None

# Function to query the database
def query_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table)
        cursor.close()

    except Exception as error:
        print(f"Error executing the query: {error}")

if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        query_db(connection)
        connection.close()
