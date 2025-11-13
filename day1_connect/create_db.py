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
            password=os.getenv("DB_PASSWORD"),
            database=database
        )
        
        if connection.is_connected():
            print("✅ DB Connected!")
            return connection
            
    except Error as e:
        print(f"❌ 연결 실패: {e}")
        return None


def create_database(connection, db_name):
    """데이터베이스 생성"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ 데이터베이스 '{db_name}' 생성 완료!")
    except Error as e:
        print(f"❌ 데이터베이스 생성 실패: {e}")


def create_table(connection, create_table_query):
    """테이블 생성"""
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("✅ 테이블 생성 완료!")
    except Error as e:
        print(f"❌ 테이블 생성 실패: {e}")


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
    # 1단계: 데이터베이스 없이 연결 (DB 생성용)
    conn = create_connection()
    
    if conn:
        # 2단계: 데이터베이스 생성
        create_database(conn, 'study_db')
        conn.close()
        
        # 3단계: 생성한 데이터베이스에 연결
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
            
            # 5단계: students 테이블 생성
            students_table = """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT,
                grade VARCHAR(10)
            )
            """
            create_table(conn, students_table)
            
            # 6단계: 테이블 목록 확인
            show_tables(conn)
            
            conn.close()
            print("\n연결이 정상적으로 종료되었습니다.")