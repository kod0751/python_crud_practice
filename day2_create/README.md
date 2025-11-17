# Day 2 - MySQL 데이터 추가 (INSERT)

> **학습 날짜**: 2025.11.17

## 🎯 학습 목표

- [x] `INSERT INTO` 문으로 데이터 추가하기
- [x] 여러 데이터를 한 번에 삽입하기 (`executemany`)
- [x] 사용자 입력으로 데이터 추가하기

## 📖 학습 내용

### 1. INSERT 기본 문법

```python
cursor.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ('홍길동', 'hong@test.com')
)
conn.commit()
```

**핵심 포인트**:

- MySQL은 `%s` 플레이스홀더 사용 (SQLite의 `?`와 다름!)
- 반드시 `conn.commit()` 호출해야 저장됨
- `cursor.rowcount`로 추가된 행 개수 확인
- `cursor.lastrowid`로 방금 추가된 ID 확인

### 2. 단일 데이터 삽입 (`insert_user.py`)

```python
cursor.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ('홍길동', 'hong@test.com')
)
conn.commit()
print(f"✅ {cursor.rowcount}개 행 추가됨")
```

- 값은 튜플로 전달: `(값1, 값2)`
- 값이 하나일 때도 콤마 필수: `(값,)`

### 3. 여러 데이터 한 번에 삽입 (`insert_many.py`)

```python
users = [
    ('김철수', 'kim@test.com'),
    ('이영희', 'lee@test.com'),
    ('박민수', 'park@test.com')
]

cursor.executemany(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    users
)
conn.commit()
```

- `executemany()`: 여러 데이터 배치 삽입
- 반복문보다 훨씬 빠름
- 대량 데이터 처리에 효율적

### 4. 사용자 입력 처리 (`input_user.py`)

```python
name = input("이름: ")
email = input("이메일: ")

cursor.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    (name, email)
)
conn.commit()
```

**⚠️ 보안 주의**:

- ❌ `f"INSERT ... VALUES ('{name}')"` ← SQL Injection 위험!
- ✅ `cursor.execute("... VALUES (%s)", (name,))` ← 안전!

### 5. 실습한 테이블들

**users 테이블**

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
)
```

**products 테이블**

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    stock INT NOT NULL
)
```

**students 테이블**

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    grade INT NOT NULL,
    score INT NOT NULL
)
```

**orders 테이블**

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    order_date DATE NOT NULL
)
```

**numbers 테이블**

```sql
CREATE TABLE numbers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value INT NOT NULL
)
```

- `UNIQUE`: 중복 불가
- `DATE`: 날짜 형식 (YYYY-MM-DD)

## 🏋️ 연습 문제 해결

### 문제 1: products 테이블에 데이터 3개 삽입

```python
products = [
    ('노트북', 1200000, 5),
    ('마우스', 25000, 50),
    ('키보드', 89000, 30)
]
cursor.executemany("INSERT INTO products ...", products)
```

### 문제 2: 회원가입 시스템

- 이름, 이메일 입력받기
- 중복 체크 후 추가
- 성공 메시지 출력

### 문제 3: 1~5까지 숫자 저장

```python
for i in range(1, 6):
    cursor.execute("INSERT INTO numbers (value) VALUES (%s)", (i,))
```

### 문제 4: 학생 성적 관리

- 5명 이상 데이터 추가
- 성적순으로 정렬 출력

### 문제 5: 주문 시스템

- 여러 주문 추가
- 총 주문 수, 총 수량 출력

## 🐛 트러블슈팅

### 문제 1: 데이터가 저장되지 않음

```
# INSERT는 성공하는데 SELECT하면 데이터 없음
```

**해결**: `conn.commit()` 추가 필수!

### 문제 2: `Incorrect number of bindings`

```
❌ mysql.connector.errors.ProgrammingError:
   Incorrect number of bindings supplied
```

**해결**: 플레이스홀더 개수와 값 개수 일치 확인

```python
# ❌ VALUES (%s, %s)인데 값은 1개만
# ✅ VALUES (%s, %s)에 (값1, 값2) 전달
```

### 문제 3: Duplicate entry 에러

```
❌ Duplicate entry 'test@test.com' for key 'email'
```

**해결**: 중복 체크 후 삽입

```python
cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
if cursor.fetchone()[0] > 0:
    print("이미 존재하는 이메일!")
```

## 🎯 핵심 정리

### SQLite vs MySQL 비교

| 항목           | SQLite          | MySQL            |
| -------------- | --------------- | ---------------- |
| 플레이스홀더   | `?`             | `%s`             |
| AUTO_INCREMENT | `AUTOINCREMENT` | `AUTO_INCREMENT` |
| 문자열 타입    | `TEXT`          | `VARCHAR(n)`     |

### 자주 하는 실수

1. **commit() 깜빡**

   ```python
   cursor.execute("INSERT ...")
   # conn.commit()  ← 이거 없으면 저장 안됨!
   ```

2. **플레이스홀더 혼동**

   ```python
   # ❌ "VALUES (?)"  # SQLite
   # ✅ "VALUES (%s)"  # MySQL
   ```

3. **SQL Injection**
   ```python
   # ❌ f"VALUES ('{name}')"  # 위험!
   # ✅ "VALUES (%s)", (name,)  # 안전!
   ```

## 🎬 실행 결과

```
✅ MySQL 연결 성공!
✅ 1개의 행이 추가되었습니다.
📝 추가된 데이터 ID: 1

📋 현재 사용자 목록:
  ID: 1 | 이름: 홍길동 | 이메일: hong@test.com

✅ 5개의 행이 추가되었습니다.

==================================================
📝 회원가입 시스템
==================================================
👤 이름: 김테스트
📧 이메일: test@test.com

✅ 회원가입 완료!
🆔 회원번호: 6
==================================================

📦 전체 주문 건수: 5건
📊 총 주문 수량: 15개

🔌 MySQL 연결 종료
```

## 💡 배운 점

1. MySQL과 SQLite의 차이 (특히 플레이스홀더!)
2. `executemany()`로 대량 데이터 효율적으로 삽입
3. SQL Injection 방지의 중요성
4. `commit()`의 필수성 (트랜잭션 개념)

## 🚀 다음 학습 계획

**Day 3 - READ (SELECT)**

- `SELECT` 문으로 데이터 조회
- `WHERE` 조건으로 필터링
- `ORDER BY`로 정렬하기
- `LIMIT`으로 개수 제한
