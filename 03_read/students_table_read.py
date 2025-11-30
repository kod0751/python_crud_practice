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


def find_students_by_grade(grade):
    """학년별 학생 조회"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, score FROM students 
            WHERE grade = %s
            ORDER BY score DESC
        """, (grade,))
        
        students = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print(f"📚 {grade}학년 학생 목록")
        print("=" * 50)
        
        if students:
            for idx, student in enumerate(students, 1):
                print(f"  {idx}. {student[0]:<10} - {student[1]}점")
            
            # 해당 학년 평균
            cursor.execute("""
                SELECT AVG(score) FROM students WHERE grade = %s
            """, (grade,))
            avg = cursor.fetchone()[0]
            print("-" * 50)
            print(f"  {grade}학년 평균: {avg:.2f}점")
        else:
            print(f"  {grade}학년 학생이 없습니다.")
        
        print("=" * 50)
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_top_students(limit=3):
    """상위권 학생 조회 - LIMIT 사용"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, grade, score FROM students 
            ORDER BY score DESC 
            LIMIT %s
        """, (limit,))
        
        students = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print(f"🏆 상위 {limit}명")
        print("=" * 50)
        
        medals = ["🥇", "🥈", "🥉"]
        for idx, student in enumerate(students):
            medal = medals[idx] if idx < 3 else "  "
            print(f"{medal} {idx+1}등: {student[0]} ({student[1]}학년) - {student[2]}점")
        
        print("=" * 50)
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def search_students_by_score(min_score):
    """특정 점수 이상 학생 검색"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, grade, score FROM students 
            WHERE score >= %s
            ORDER BY score DESC
        """, (min_score,))
        
        students = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print(f"✨ {min_score}점 이상 학생")
        print("=" * 50)
        
        if students:
            for student in students:
                grade_symbol = "🌟" if student[2] >= 90 else "⭐"
                print(f"  {grade_symbol} {student[0]:<10} ({student[1]}학년) - {student[2]}점")
            print("-" * 50)
            print(f"  총 {len(students)}명")
        else:
            print(f"  {min_score}점 이상인 학생이 없습니다.")
        
        print("=" * 50)
        
    except Error as e:
        print(f"❌ 오류: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
  search_students_by_score(85)