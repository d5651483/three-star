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
    "喜歡的興趣（含過往與現在）",
    "令我恐懼的經驗？",
    "什麼情況會造成我感到壓力？",
    "我曾經有的壞習慣，但現在改變了？",
    "印象最深刻的旅遊經驗？",
    "我曾經錯過的機會？",
    "令我後悔的決定？",
    "最遺憾的經驗？",
    "至今最滿意的成就？",
    "我喜歡學習嗎？",
    "最印象深刻的學習經驗？",
    "我覺得工作是為了什麼？",
    "遇過最大的挑戰？",
    "放假時喜歡做的事情？",
    "最喜歡去的地方？為什麼？",
    "我最喜歡做的事？",
    "我覺得我擅長做什麼？",
    "我會如何形容自己的個性？",
    "我很喜歡自己的哪些特質？",
    "用三個詞形容自己",
    "親情、友情、愛情，如何排序？",
    "事業、家庭、個人，最重哪項？",
    "我最討厭的事情？",
    "我不擅長做什麼？",
    "什麼情況會讓我感到焦慮、不安的情緒？",
    "我一想到就會微笑的事情？",
    "覺得很幸福的瞬間？",
    "令我感到放鬆的時刻？",
    "使我起床/讓我感到動力的原因？",
    "我最在意的人、事、物？",
    "曾經收過最滿意的禮物？",
    "現在生活的環境中最喜歡/滿意的部分？",
    "現在生活的環境中不喜歡/不滿意的部分？",
    "如果不考慮成本及可行性，我現在最想做什麼？",
    "如果明天是世界末日，我今天會想做什麼？",
    "我希望十年後的我⋯⋯？",
    "想像中30歲的生活？",
    "想像中40歲的生活？",
    "我希望改變自己或想練習的事情？",
    "如果＿＿＿＿改變了，我會過得更好？",
    "我通常在團隊中擔任的角色？",
    "做過或覺得什麼樣的工作適合自己？",
    "他人曾稱讚我做得好的事情？",
    "他人曾批評過我的事情？",
    "我認為我做得比他人好的事情？",
    "我更擅長獨自工作還是與團體一起工作？",
    "他人通常會如何形容我的個性？",
    "用三個詞形容自己？",
    "他人覺得我好/不好相處的原因？",
    "我會用什麼顏色形容自己？",
    "我覺得我最像什麼動物？為什麼？",
    "我擅長與人相處嗎？"
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