import os
import json
import sqlite3
from datetime import datetime

class Manager:

    # 建立資料庫
    def __init__(self, db_name : str):

        db_path = "database"

        self.db_name = os.path.join(db_path, db_name)

    def createTable(self, rule : str):

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(rule)
        conn.commit()
        conn.close()
    
    # 連接資料庫
    def connect_db(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回
        return conn

class DiaryManager(Manager):

    # 創建資料表
    def __init__(self):
        super().__init__("Dairy.db")
        
        self.createTable(
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

        # 轉成陣列
        formatted_diaries = [
            {
                'id': diary[0],
                'title': diary[1],
                'content': diary[2],
                'answers': [
                    diary[3] if diary[3] else '未回答',
                    diary[4] if diary[4] else '未回答',
                    diary[5] if diary[5] else '未回答'
                ],
                'created_at': diary[6]
            }
            for diary in diaries
        ]

        return formatted_diaries

class QuestManager(Manager):

    def __init__(self):

        super().__init__("Question.db")
        
        self.createTable(
            '''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

        self.createTable(
            '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                created_at TEXT
            )
            '''
        )
        
        with open('static\\question\\questions.json', 'r', encoding='utf-8') as file:
            self.questions = json.load(file)

        self.count_questions = len(self.questions)
        self.start_date = datetime.strptime("2024-09-01", "%Y-%m-%d").date()

    # 生成問題
    def generate_daily_question(self):

        today = datetime.today().date()
        conn = self.connect_db()
        cursor = conn.cursor()

        # 檢查今天是否已有問題
        cursor.execute("""
            SELECT * FROM questions
            WHERE created_at = ?
            ORDER BY created_at DESC LIMIT 1
        """, (today,))

        question = cursor.fetchone()

        # 如果今天沒有問題，則生成一個新的問題
        if not question:

            question_number = (today - self.start_date).days % self.count_questions # 按照時間循環

            ori_question = self.questions[str(question_number+1)] # 取得題目

            # 寫入題目
            cursor.execute(
                'INSERT INTO questions (question, created_at) VALUES (?, ?)',
                (ori_question, today)
            )
            conn.commit()

            question = {'question': ori_question}

        else:

            question = {'question': question[1]}
        
        conn.close()

        return question
    
    # 新增回答
    def add_answer(self, answer):

        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM questions
            WHERE DATE(created_at) = DATE('now') 
            ORDER BY created_at DESC LIMIT 1
        """)

        question_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO answers (question_id, answer)
            VALUES (?, ?)
        ''', (question_id, answer))
        
        conn.commit()
        conn.close()

        return {"message": "問題已儲存！"}

    # 取得問題
    def get_all_answers(self):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM answers ORDER BY created_at DESC') # 按照創建時間排序
        answers = cursor.fetchall()

        cursor.execute('SELECT * FROM questions ORDER BY created_at DESC') # 按照創建時間排序
        questions = cursor.fetchall()

        conn.close()

        formatted_questions = [
            {
                'question' : questions[answer[1]][1],
                'answer' : answer[2],
                'created_at': answer[3]
            }
            for answer in answers
        ]

        return formatted_questions
   
class AIManager(Manager):

    def __init__(self) -> None:
        super().__init__("AI.db")
        
        self.createTable(
            '''
            CREATE TABLE IF NOT EXISTS ai_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                sent_at TEXT
            )
            '''
        )
    
    def write(self):
        pass