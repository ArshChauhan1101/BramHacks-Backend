import mysql.connector
from mysql.connector import Error
import os

class DatabaseConfig:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "Sc@22101996"
        self.database = "Arsh"

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            connection.commit()
            print(f"Database '{self.database}' created successfully (or already exists).")
            return True
        except Error as e:
            print(f"Error creating database: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connection to database successful.")
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_sql_file(self, filepath):
        connection = self.get_connection()
        if connection is None:
            print("Failed to connect to the database for executing SQL file.")
            return False

        try:
            cursor = connection.cursor()
            with open(filepath, 'r') as file:
                sql_commands = file.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
            connection.commit()
            print("SQL file executed successfully.")
            return True
        except Error as e:
            print(f"Error executing SQL file: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    db_config = DatabaseConfig()
    if db_config.create_database():  # Try creating the database
        print("Database creation process complete.")
        # Execute SQL commands from the schemas.sql file located in the database folder
        sql_file_path = os.path.join("database", "schemas.sql")
        db_config.execute_sql_file(sql_file_path)
    else:
        print("Failed to create the database.")
