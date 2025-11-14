import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

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

add_product()