import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def add_user_interactive():
    """사용자로부터 입력받아 데이터 추가"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='day2_practice'
        )
        cursor = conn.cursor()
        
        print("=" * 50)
        print("📝 새로운 사용자 등록")
        print("=" * 50)
        
        # 사용자 입력
        name = input("👤 이름을 입력하세요: ").strip()
        email = input("📧 이메일을 입력하세요: ").strip()
        
        # 입력 검증
        if not name or not email:
            print("❌ 이름과 이메일은 필수입니다!")
            return
        
        # 중복 확인
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            print(f"❌ '{email}'은 이미 등록된 이메일입니다!")
            return
        
        # 데이터 추가
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, email))
        conn.commit()
        
        print(f"\n✅ '{name}'님의 정보가 성공적으로 추가되었습니다!")
        print(f"📝 사용자 ID: {cursor.lastrowid}")
        print(f"📧 등록 이메일: {email}")
        
        # 전체 사용자 수 확인
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        print(f"👥 전체 등록 사용자: {total_users}명")
        
    except Error as e:
        print(f"❌ 오류 발생: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

add_user_interactive()