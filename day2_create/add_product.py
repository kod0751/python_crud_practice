import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import re

load_dotenv()

def add_product():
  """새로운 상품 추가 함수"""
  try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='day2_practice'
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price INT NOT NULL,
                stock INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        prodouct_data = [
            ('노트북', 1200000, 10),
            ('스마트폰', 800000, 25),
            ('태블릿', 600000, 15),
            ('모니터', 300000, 8),
            ('키보드', 50000, 50)
        ]

        insert_query = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, prodouct_data)
        
        conn.commit()

        print(f"✅ {cursor.rowcount}개의 상품이 추가되었습니다.")

        cursor.execute("SELECT * FROM products")

        print("=" * 70)
        print(f"{'ID':<5} {'상품명':<15} {'가격':>15} {'재고':>10} {'등록일':<20}")
        print("=" * 70)
        
        for row in cursor.fetchall():
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:>12,}원 {row[3]:>10}개 {row[4]}")
        
        print("=" * 70)
        
  except Error as e:
        print(f"❌ 오류: {e}")
        
  finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def validate_email(email):
    """이메일 형식 검증"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def user_registration():
    """회원가입 시스템"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='day2_practice'
        )
        cursor = conn.cursor()
        
        print("\n" + "=" * 50)
        print("🎉 회원가입 시스템")
        print("=" * 50 + "\n")
        
        while True:
            # 이름 입력
            name = input("👤 이름: ").strip()
            if len(name) < 2:
                print("❌ 이름은 2글자 이상이어야 합니다.\n")
                continue
            
            # 이메일 입력
            email = input("📧 이메일: ").strip()
            
            # 이메일 형식 검증
            if not validate_email(email):
                print("❌ 올바른 이메일 형식이 아닙니다.\n")
                continue
            
            # 중복 확인
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                print(f"❌ '{email}'은 이미 사용 중입니다.\n")
                continue
            
            # 데이터 추가
            insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, email))
            conn.commit()
            
            print("\n" + "=" * 50)
            print("✅ 회원가입 완료!")
            print("=" * 50)
            print(f"👤 이름: {name}")
            print(f"📧 이메일: {email}")
            print(f"🆔 회원번호: {cursor.lastrowid}")
            print("=" * 50 + "\n")
            
            break
        
    except Error as e:
        print(f"❌ 데이터베이스 오류: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_numbers():
    """1부터 5까지 숫자 저장"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='day2_practice'
        )
        cursor = conn.cursor()
        
        # 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS numbers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                value INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """)
        
        # 방법 1: 반복문으로 하나씩 추가
        print("📝 방법 1: 반복문으로 하나씩 추가")
        for i in range(1, 6):
            cursor.execute("INSERT INTO numbers (value) VALUES (%s)", (i,))
            print(f"  ✓ {i} 추가됨")
        
        conn.commit()
        print(f"✅ {cursor.rowcount}개의 숫자가 추가되었습니다.\n")
        
        # 결과 확인
        cursor.execute("SELECT * FROM numbers ORDER BY value")
        results = cursor.fetchall()
        
        print("📋 저장된 숫자:")
        print("  ", [row[1] for row in results])
        
    except Error as e:
        print(f"❌ 오류: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

insert_numbers()