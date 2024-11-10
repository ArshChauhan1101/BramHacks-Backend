import mysql.connector
from mysql.connector import Error
import json

class DatabaseConfig:
    def __init__(self):
        self.host = "127.0.0.1"  # Explicitly use 127.0.0.1 (instead of localhost)
        self.port = 3306  # Specify port explicitly
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

    def initialize_tables(self):
        schema_sql_path = 'database/schemas.sql'
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                with open(schema_sql_path, 'r') as file:
                    schema_sql = file.read()
                    cursor.execute(schema_sql, multi=True)
                    connection.commit()
                print("Tables created and initialized.")
            except Error as e:
                print(f"Error initializing tables: {e}")
            finally:
                cursor.close()
                connection.close()

    def insert_complaints_from_json(self, json_path):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Step 1: Delete all previous entries from the complaints table
                cursor.execute("DELETE FROM Complaint")
                connection.commit()
                print("All previous complaints deleted.")
                
                # Step 2: Insert new complaints from the JSON file
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
    if db_config.create_database():
        db_config.initialize_tables()  # Initialize tables from schemas.sql
        db_config.insert_complaints_from_json('database/complaints.json')  # Insert complaints from JSON
