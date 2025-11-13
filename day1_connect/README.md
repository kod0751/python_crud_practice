# Day 1 - MySQL 연결 및 테이블 생성 기초

> **학습 날짜**: 2025.11.13

## 🎯 학습 목표

- [x] Python에서 MySQL 데이터베이스 연결하기
- [x] 데이터베이스 생성하기
- [x] 테이블 생성하기

## 📖 오늘 배운 내용

### 1. 환경 설정 (`.env` 파일)

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=study_db
```

**왜 .env를 사용할까?**

- 비밀번호 같은 민감한 정보를 코드에서 분리
- GitHub에 올릴 때 `.gitignore`로 제외 가능
- 개발/운영 환경을 쉽게 전환

### 2. MySQL 기본 연결 (`main.py`)

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="****",
    database="study_db"
)
```

**핵심 포인트**:

- `connection.is_connected()`로 연결 상태 확인
- `try-except`로 에러 처리
- 사용 후 반드시 `connection.close()`

### 3. 데이터베이스 생성 (`create_db.py`)

```sql
CREATE DATABASE IF NOT EXISTS study_db
```

### 4. 테이블 생성

**books 테이블**

```sql
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    price INT
)
```

**students 테이블**

```sql
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    grade VARCHAR(10)
)
```

- `AUTO_INCREMENT`: 자동으로 1씩 증가
- `PRIMARY KEY`: 중복 불가, NULL 불가
- `NOT NULL`: 필수 입력
- `VARCHAR(n)`: 최대 n글자 문자열

### 5. 테이블 조회 (`show_table.py`)

```python
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
```

- `cursor`: SQL 명령 실행 도구
- `fetchall()`: 모든 결과 가져오기
- 결과는 튜플의 리스트 형태

## 🐛 트러블슈팅

### 문제 1: `Access denied for user`

```
❌ 연결 오류: Access denied for user 'root'@'localhost'
```

**해결**: `.env` 파일의 비밀번호 확인

## 🎬 실행 결과

```
✅ DB Connected!
✅ 데이터베이스 'study_db' 생성 완료!
✅ DB Connected!
✅ 테이블 생성 완료!
✅ 테이블 생성 완료!

📋 현재 테이블 목록:
  - books
  - students

연결이 정상적으로 종료되었습니다.
```
