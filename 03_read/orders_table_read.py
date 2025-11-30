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