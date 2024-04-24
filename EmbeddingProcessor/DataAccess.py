# dataAccess.py

import mysql.connector
# Used Single Store Vector Database for ths project
# Database connection parameters
config = {
    'user': {Insert vector database username},
    'password': {Insert vector database password},
    'host': {Insert vector database host link},
    'database': {Insert vector database name},
    'port': 3306
}

def get_database_connection():
    return mysql.connector.connect(**config)

def insert_test_record():
    connection = get_database_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO MediaFile (filename, filetype, category, transcript, summary) VALUES (%s, %s, %s, %s, %s)"
    values = ("test.mp4", "video", "test_category", "This is a test transcript.", "This is a test summary.")

    cursor.execute(sql, values)
    connection.commit()
    
    print(f"Inserted record ID: {cursor.lastrowid}")
    cursor.close()
    connection.close()

def query_media_files():
    connection = get_database_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM MediaFile"
    cursor.execute(sql)

    for row in cursor:
        print(f"Row: {row}")

    cursor.close()
    connection.close()
