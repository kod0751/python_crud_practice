import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def create_connection(database=None):
  try: 
    connection = mysql.connector.connect(
      host=os.getenv("DB_HOST"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      database=database
    )
    if connection.is_connected():
      print('DB Connected!')
      return connection
  
  except Error as e:
    print(f"❌ 연결 실패: {e}")
    return None

def create_database(connection, db_name):
  '데이터베이스 생성'
  try:
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
    print(f"✅ 데이터베이스 '{db_name}' 생성 완료!")
  except Error as e:
    print(f"❌ 데이터베이스 생성 실패: {e}")

def create_table(connection, create_table_query):
  '테이블 생성'
  try:
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    print("✅ 테이블 생성 완료!")
  except Error as e:
    print(f"❌ 테이블 생성 실패: {e}")



conn = create_connection()

if conn:
  create_database(conn, 'study_db')
  conn.close()

  conn = create_connection('study_db')

  if conn:
    # 4단계: books 테이블 생성
    books_table = """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        author VARCHAR(100),
        price INT
    )
    """
    create_table(conn, books_table)

  conn.close()
