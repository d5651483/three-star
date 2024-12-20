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

        return {"message": "diary has save"}

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
        
        with open(os.path.join('static', 'question', 'questions.json'), 'r', encoding='utf-8') as file:
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

        return {"message": "question has save"}

    # 取得問題
    def get_all_answers(self):
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # 獲取所有問題和答案，按創建時間排序
        cursor.execute('SELECT * FROM answers ORDER BY created_at DESC')
        answers = cursor.fetchall()

        cursor.execute('SELECT * FROM questions ORDER BY created_at DESC')
        questions = cursor.fetchall()

        conn.close()

        # 建立問題 ID 與問題內容的映射表
        question_map = {question[0]: question[1] for question in questions}

        # 格式化答案
        formatted_questions = [
            {
                'question': question_map.get(answer[1], 'Unknown Question'),  # 根據問題 ID 查找
                'answer': answer[2],
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
            CREATE TABLE IF NOT EXISTS table_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

        self.record_limit = 100
    
    def start_talk(self, chat_num) -> list:

        if chat_num == 0 : self.new_talk(); return []

        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM table_record ORDER BY created_at DESC LIMIT 1 OFFSET ?', (chat_num-1,))

        self.table_name = cursor.fetchone()['table_name']

        conn.commit()
        conn.close()

        return self.allRecord(self.table_name)
    
    def new_talk(self):

        self.table_name = f"table_{int(datetime.now().timestamp())}"
        
        self.createTable(
            f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(f'INSERT INTO table_record (table_name) VALUES (?)', (self.table_name,))
        
        conn.commit()
        conn.close()
    
    def write(self, author, content):
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            INSERT INTO {self.table_name} (author, content)
            VALUES (?, ?)
        ''', (author, content))
        
        conn.commit()
        conn.close()
    
    def lessRecord(self, table_name=None, record_limit=None):

        if table_name is None : table_name = self.table_name
        if record_limit is None : record_limit = self.record_limit

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT ?', (record_limit,))  # 按照創建時間排序
        ai_records = cursor.fetchall()
        
        conn.close()

        # 轉成陣列
        formatted_ai_records = [
            {
                'id': ai_record[0],
                'author': ai_record[1],
                'content': ai_record[2],
                'created_at': ai_record[3]
            }
            for ai_record in ai_records
        ]

        return formatted_ai_records
    
    def allRecord(self, table_name):

        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {table_name}')  # 按照創建時間排序
        ai_records = cursor.fetchall()
        
        conn.close()

        # 轉成陣列
        formatted_ai_records = [
            {
                'id': ai_record[0],
                'author': ai_record[1],
                'content': ai_record[2],
                'created_at': ai_record[3]
            }
            for ai_record in ai_records
        ]

        return formatted_ai_records
    
    def len_table(self):

        conn = self.connect_db()
        cursor = conn.cursor()

        # 執行 SQL 查詢，計算某個表中的數據數量
        cursor.execute("SELECT COUNT(*) table_record")  # 替換為你的表名
        count = cursor.fetchone()[0]  # 取得結果中的數量

        conn.close()

        # 根據數量返回 3 或實際數量
        if count > 3:
            return 3
        else:
            return count