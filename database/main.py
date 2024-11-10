import mysql.connector
from mysql.connector import Error
import json
import os

class DatabaseConfig:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "Sc@22101996"
        self.database = "Bramhacks"

    def database_exists(self):
        """Check if the database already exists."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{self.database}'")
            exists = cursor.fetchone() is not None
            return exists
        except Error as e:
            print(f"Error checking database existence: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_database(self):
        """Create the database if it does not already exist."""
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
            print(f"Database '{self.database}' created successfully.")
            return True
        except Error as e:
            print(f"Error creating database: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_connection(self):
        """Establish a connection to the database."""
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
        """Execute SQL commands from a file to set up tables."""
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

    def reset_complaints_table(self):
        """Delete all entries in the Complaint table."""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Complaint")
                connection.commit()
                print("All previous complaints deleted.")
            except Error as e:
                print(f"Error deleting complaints data: {e}")
            finally:
                cursor.close()
                connection.close()

    def insert_complaints_from_json(self, json_path):
        """Insert complaints data from a JSON file."""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                with open(json_path, 'r') as file:
                    complaints = json.load(file)
                    for complaint in complaints:
                        sql = """
                            INSERT INTO Complaint (id, userComplaint, categoryId, subCategoryId)
                            VALUES (%s, %s, %s, %s)
                        """
                        values = (
                            complaint["id"],
                            complaint["complaint"],
                            complaint["category"],  # Assuming this field in JSON matches categoryId
                            complaint["subcategory"]  # Assuming this field in JSON matches subCategoryId
                        )
                        cursor.execute(sql, values)
                    connection.commit()
                    print("Complaints data inserted successfully.")
            except Error as e:
                print(f"Error inserting complaints data: {e}")
            finally:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    db_config = DatabaseConfig()
    
    # Check if database already exists
    if db_config.database_exists():
        print("Database already exists.")
    else:
        print("Database does not exist. Creating and initializing database.")
        # Create the database and run the schema SQL file if not created
        if db_config.create_database():
            schema_file_path = os.path.join("database", "schemas.sql")
            db_config.execute_sql_file(schema_file_path)
        else:
            print("Failed to create the database.")
            exit(1)

    # Reset complaints data and insert new data from JSON
    db_config.reset_complaints_table()
    json_file_path = os.path.join("database", "complaints.json")
    db_config.insert_complaints_from_json(json_file_path)
