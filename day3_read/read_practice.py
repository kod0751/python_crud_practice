
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

def search_products_by_price(min_price, max_price):
    """가격 범위로 검색 - WHERE + BETWEEN"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM products 
            WHERE price BETWEEN %s AND %s
            ORDER BY price ASC
        """, (min_price, max_price))
        
        products = cursor.fetchall()
        
        print("\n" + "=" * 70)
        print(f"💰 가격 범위 검색: {min_price:,}원 ~ {max_price:,}원")
        print("=" * 70)
        
        if products:
            print(f"{'ID':<5} {'상품명':<15} {'가격':>15} {'재고':>10}")
            print("-" * 70)
            for p in products:
                print(f"{p[0]:<5} {p[1]:<15} {p[2]:>12,}원 {p[3]:>10}개")
            print("=" * 70)
            print(f"총 {len(products)}개의 상품 발견")
        else:
            print("해당 가격대의 상품이 없습니다.")
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    search_products_by_price(50000, 150000)