import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv() # .env 파일에서 환경 변수 로드

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),  # ← 여기에 본인 비밀번호 입력
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("✅ MySQL 연결 성공!")
            return connection

    except Error as e:
        print("❌ 연결 오류:", e)
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("🔌 연결 종료")

if __name__ == "__main__":
    conn = create_connection()
    close_connection(conn)
