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


def read_all_students():
    """전체 학생 조회"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students ORDER BY score DESC")
        students = cursor.fetchall()
        
        print("\n" + "=" * 60)
        print("🎓 전체 학생 목록 (성적순)")
        print("=" * 60)
        print(f"{'순위':<5} {'이름':<10} {'학년':<10} {'점수':<10}")
        print("-" * 60)
        
        for rank, student in enumerate(students, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
            print(f"{medal} {rank:<3} {student[1]:<10} {student[2]}학년{'':<5} {student[3]}점")
        
        print("=" * 60)
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

read_all_students()