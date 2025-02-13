import psycopg2
import os

# Load environment variables if needed
from dotenv import load_dotenv
load_dotenv()

def check_db_connection():
    try:
        # Get the DATABASE_URL environment variable (you can directly hardcode the connection string if needed)
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://neondb_owner:npg_8rmaWYnKUk0T@ep-floral-snow-a2y1cpoq-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require')

        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute a query to check if the database is accessible
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        
        if result:
            print("Successfully connected to the Neon PostgreSQL database!")
        
        # Close the connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    check_db_connection()
