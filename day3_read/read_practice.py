
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def connect_db():
    """데이터베이스 연결"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database='day2_practice'
    )

def read_all_products():
    """전체 상품 조회 - fetchall() 연습"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        print("\n" + "=" * 70)
        print("📦 전체 상품 목록")
        print("=" * 70)
        print(f"{'ID':<5} {'상품명':<15} {'가격':>15} {'재고':>10} {'등록일':<20}")
        print("-" * 70)
        
        for product in products:
            print(f"{product[0]:<5} {product[1]:<15} {product[2]:>12,}원 {product[3]:>10}개 {product[4]}")
        
        print("=" * 70)
        print(f"총 {len(products)}개의 상품")
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def find_product_by_name(product_name):
    """상품명으로 검색 - fetchone() 연습"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE name = %s", (product_name,))
        product = cursor.fetchone()
        
        if product:
            print("\n" + "=" * 50)
            print(f"🔍 '{product_name}' 검색 결과")
            print("=" * 50)
            print(f"  ID: {product[0]}")
            print(f"  상품명: {product[1]}")
            print(f"  가격: {product[2]:,}원")
            print(f"  재고: {product[3]}개")
            print(f"  등록일: {product[4]}")
            print("=" * 50)
        else:
            print(f"\n❌ '{product_name}' 상품을 찾을 수 없습니다.")
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    find_product_by_name("노트북")
    find_product_by_name("스마트워치")