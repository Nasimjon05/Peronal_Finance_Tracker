import psycopg2
from psycopg2 import OperationalError

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database="finance_tracker",  # your database name
            user="postgres",            # your postgres username
            password="nasimjondev23",    # your postgres password
            host="localhost",
            port="5432"
        )
        print("Connection to PostgreSQL successful!")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    
    return connection
    