import sqlite3
from datetime import datetime
import random

class Manager:

    # 建立資料庫
    def __init__(self, db_name, rule):

        self.db_name = db_name
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(rule)
        conn.commit()
        conn.close()
    
    # 連接資料庫
    def connect_db(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***
        return conn

class DiaryManager(Manager):

    # 創建資料表
    def __init__(self):
        super().__init__(
            "Dairy.db", 
            ''' 
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                answer1 TEXT,
                answer2 TEXT,
                answer3 TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            )

    # 新增日記
    def add_diary(self, title, content, answer1, answer2, answer3):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(''' 
            INSERT INTO diaries (title, content, answer1, answer2, answer3)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, answer1, answer2, answer3))
        
        conn.commit()
        conn.close()

        return {"message": "日記已儲存！"}

    # 取得日記
    def get_all_diaries(self):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM diaries ORDER BY created_at DESC')  # 按照創建時間排序
        diaries = cursor.fetchall()
        
        conn.close()

        return diaries

class QuestManager(Manager):

    questions = [
        "今天有什麼特別的事情發生嗎？",
        "描述一下今天的心情。",
        "今天學到了什麼新知識？",
        "今天做了什麼讓你感到驕傲的事？",
        "今天有什麼挑戰？你是如何應對的？",
        "三件你一想到就會微笑的事情？"
    ]

    def __init__(self):

        super().__init__(
            "Question.db", 
            '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            )
        
        self.quest_record = Manager(
            "Quest_Record.db", 
            '''
            CREATE TABLE IF NOT EXISTS quest_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                date DATE NOT NULL
            )
            '''
            )


    # 自動生成隨機問題
    def generate_daily_question(self):

        today = datetime.now().strftime('%Y-%m-%d')
        conn = self.quest_record.connect_db()
        cursor = conn.cursor()

        # 檢查今天是否已有問題
        cursor.execute("SELECT * FROM quest_record WHERE date = ?", (today,))
        question = cursor.fetchone()

        # 如果今天沒有問題，則生成一個新的問題
        if not question:

            random_question = random.choice(self.questions)

            cursor.execute("""
                INSERT INTO quest_record (question, date)
                VALUES (?, ?)
            """, (random_question, today))

            conn.commit()
            question = {'question': random_question, 'date': today}

        else:

            question = {'question': question['question'], 'date': question['date']}
        
        conn.close()

        return question
    
    # 新增問題
    def add_question(self, question, answer):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(''' 
            INSERT INTO questions (question, answer)
            VALUES (?, ?)
        ''', (question, answer))
        
        conn.commit()
        conn.close()

        return {"message": "問題已儲存！"}

    # 取得問題
    def get_all_question(self):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM questions ORDER BY created_at DESC') # 按照創建時間排序
        questions = cursor.fetchall()
        
        conn.close()

        return questions