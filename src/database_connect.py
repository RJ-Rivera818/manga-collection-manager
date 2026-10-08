import os
import mysql.connector

# starts the connection to the database
def database_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("***PASSWORD***"),
            database="manga_collection"
        )
        print("Connected to MySQL!\n")
        return db

    except mysql.connector.Error as error_code:
        print("failed to connect to MySQL database.", error_code)
        print(f"Database connection failed: {error_code}")
        return none
