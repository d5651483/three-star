import os
import json
import sqlite3
from datetime import datetime

class Manager:

    # 建立資料庫
    def __init__(self, db_name, rule):

        db_path = "database"

        self.db_name = os.path.join(db_path, db_name)

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
        
        with open('static\question\question.json', 'r', encoding='utf-8') as file:
            self.questions = json.load(file)

        self.count_questions = len(self.questions)
        self.start_date = datetime.strptime("2024-09-01", "%Y-%m-%d")

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

            question_number = (self.start_date - today) % self.count_questions # 按照時間循環

            ori_question = self.questions[str(question_number+1)]

            cursor.execute("""
                INSERT INTO quest_record (question, date)
                VALUES (?, ?)
            """, (ori_question, today))

            conn.commit()
            question = {'question': ori_question, 'date': today}

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

        formatted_questions = [
            {
                'question' : question[1],
                'answer' : question[2],
                'created_at': question[3]
            }
            for question in questions
        ]

        return formatted_questions