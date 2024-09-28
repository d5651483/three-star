import sqlite3
from datetime import datetime
import random

# 連接 SQLite 資料庫
def connect_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回
    return conn

# 創建資料表
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # 創建日記表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 創建每日問題表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            date DATE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# 自動生成隨機問題
def generate_daily_question():
    questions = [
        "今天有什麼特別的事情發生嗎？",
        "描述一下今天的心情。",
        "今天學到了什麼新知識？",
        "今天做了什麼讓你感到驕傲的事？",
        "今天有什麼挑戰？你是如何應對的？"
    ]
    today = datetime.now().strftime('%Y-%m-%d')
    conn = connect_db()
    cursor = conn.cursor()

    # 檢查今天是否已有問題
    cursor.execute("SELECT * FROM daily_questions WHERE date = ?", (today,))
    question = cursor.fetchone()

    # 如果今天沒有問題，則生成一個新的問題
    if not question:
        random_question = random.choice(questions)
        cursor.execute("INSERT INTO daily_questions (question, date) VALUES (?, ?)", (random_question, today))
        conn.commit()
        question = {'question': random_question, 'date': today}
    else:
        question = {'question': question['question'], 'date': question['date']}
    
    conn.close()
    return question

# 新增日記
def add_diary(content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

# 取得所有日記
def get_all_diaries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary")
    diaries = cursor.fetchall()
    conn.close()

    result = [
        {"id": row["id"], "content": row["content"], "created_at": row["created_at"], "updated_at": row["updated_at"]}
        for row in diaries
    ]
    return result
