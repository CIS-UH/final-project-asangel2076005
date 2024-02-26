import mysql.connector
from mysql.connector import Error


def create_connection(hostname, username, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=user_password,
            database=database_name
        )
        print("Connection to MySQL DB Successful")
    except Error as e:
        print(f"The error {e} occurred")

    return connection


# Delivers a query
def execute_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error {e} occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error {e} occurred")
