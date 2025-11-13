import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def create_connection(database=None):
    """MySQL 서버에 연결하는 함수"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),  # 실제 비밀번호로 변경!
            database=database
        )
        
        if connection.is_connected():
            print("✅ DB Connected!")
            return connection
            
    except Error as e:
        print(f"❌ 연결 실패: {e}")
        return None



def show_tables(connection):
    """테이블 목록 조회"""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        print("\n📋 현재 테이블 목록:")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  (테이블 없음)")
    except Error as e:
        print(f"❌ 테이블 조회 실패: {e}")


# ========== 실습 코드 ==========
if __name__ == "__main__":

        conn = create_connection('study_db')
        
        if conn:

            show_tables(conn)
            
            conn.close()
            print("\n연결이 정상적으로 종료되었습니다.")