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
            print(f"✅ DB Connected! ({database or 'no database'})")
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


def insert_single_user(conn):
    """단일 사용자 데이터 추가"""
    try:
        cursor = conn.cursor()
        
        # 테이블 생성 (없으면)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table_query)
        
        # 데이터 추가
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        user_data = ('홍길동', 'hong@test.com')
        
        cursor.execute(insert_query, user_data)
        conn.commit()
        
        print(f"✅ {cursor.rowcount}개의 행이 추가되었습니다.")
        print(f"📝 추가된 데이터 ID: {cursor.lastrowid}")
        
        # 확인
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        print("\n📋 현재 사용자 목록:")
        for row in results:
            print(f"  ID: {row[0]} | 이름: {row[1]} | 이메일: {row[2]}")
        
    except Error as e:
        print(f"❌ 오류 발생: {e}")
        
    finally:
        cursor.close()


if __name__ == "__main__":
    # 1️⃣ 서버 연결
    conn = create_connection()

    if conn:
        # 2️⃣ 데이터베이스 생성
        create_database(conn, 'day2_practice')
        conn.close()

        # 3️⃣ 새로 생성한 DB로 연결
        conn = create_connection('day2_practice')

        if conn:
            # 4️⃣ 이미 연결된 conn을 insert 함수에 전달
            insert_single_user(conn)
            conn.close()
