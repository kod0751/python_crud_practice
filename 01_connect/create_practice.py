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



conn = create_connection()

