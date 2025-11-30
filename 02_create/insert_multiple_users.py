import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def insert_multiple_users():
    """여러 사용자 데이터 한 번에 추가"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='day2_practice'
        )
        cursor = conn.cursor()
        
        # 여러 사용자 데이터 준비
        users_data = [
            ('김철수', 'kim@test.com'),
            ('이영희', 'lee@test.com'),
            ('박민수', 'park@test.com'),
            ('최지연', 'choi@test.com'),
            ('정대현', 'jung@test.com')
        ]
        
        # executemany로 한 번에 삽입
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.executemany(insert_query, users_data)
        
        conn.commit()
        
        print(f"✅ {cursor.rowcount}개의 행이 추가되었습니다.")
        
        # 방금 추가된 데이터 확인
        cursor.execute("""
            SELECT * FROM users 
            ORDER BY id DESC 
            LIMIT %s
        """, (len(users_data),))
        
        print("\n📋 추가된 사용자 목록:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]} | 이름: {row[1]} | 이메일: {row[2]}")
        
    except Error as e:
        print(f"❌ 오류: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

insert_multiple_users()