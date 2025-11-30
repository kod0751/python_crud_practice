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



conn = create_connection()

if conn:
  create_database(conn, 'study_db')
  conn.close()

