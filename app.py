from flask import Flask, request, jsonify, render_template
import sqlite3  # 使用 SQLite 資料庫
from datetime import datetime  # 引入日期時間模組

# 資料庫操作
import sqlite3

DATABASE = 'diary.db'

def connect_db():
    """建立與 SQLite 資料庫的連線"""
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    """創建 diaries 資料表，如果表不存在"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            answer1 TEXT,
            answer2 TEXT,
            answer3 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_diary_to_db(title, content, answer1, answer2, answer3):
    """新增日記到資料庫"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(''' 
        INSERT INTO diaries (title, content, answer1, answer2, answer3)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, content, answer1, answer2, answer3))
    
    conn.commit()
    conn.close()

class DiaryManager:
    def add_diary(self, title, content, answer1, answer2, answer3):
        """新增日記到資料庫中"""
        add_diary_to_db(title, content, answer1, answer2, answer3)
        return {"message": "日記已儲存！"}


def get_all_diaries():
    """取得所有日記"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM diaries ORDER BY created_at DESC')  # 按照創建時間排序
    diaries = cursor.fetchall()
    
    conn.close()
    return diaries


# DiaryManager 類別，負責管理與日記相關的操作
class DiaryManager:
    def __init__(self):
        pass

    def add_diary(self, title, content, answer1, answer2, answer3):
        """新增日記到資料庫中"""
        add_diary_to_db(title, content, answer1, answer2, answer3)
        return {"message": "日記已儲存！"}

    def get_all_diaries(self):
        """取得所有日記"""
        diaries = get_all_diaries()
        return diaries

# 建立 DiaryManager 實例
diary_manager = DiaryManager()



# 建立 Flask 應用
app = Flask(__name__)

# 獲取今天的問題
@app.route('/get-question', methods=['GET'])
def get_question():
    """返回今天的問題"""
    question = generate_daily_question()
    return jsonify(question)

def generate_daily_question():
    """生成每日問題（示範用途，可擴展）"""
    questions = ["三件你一想到就會微笑的事情？"]
    return {"question": questions}

# 新增日記
@app.route('/add-diary', methods=['POST'])
def add_diary_route():
    data = request.json

    # 檢查數據是否正確接收到
    if data is None:
        return jsonify({"error": "No data received"}), 400

    title = data.get('title')
    content = data.get('content')
    answers = data.get('answers')

    # 檢查 title 和 content 是否存在
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    # 檢查 answers 是否為列表且長度為3
    if not answers or len(answers) != 3:
        return jsonify({"error": "Invalid answers format"}), 400

    # 調用 add_diary 方法，傳遞正確的參數
    diary_manager.add_diary(
        title,
        content,
        answers[0],
        answers[1],
        answers[2]
    )
    
    return jsonify({"message": "Diary added successfully"}), 200





# 取得所有日記
@app.route('/get-diaries', methods=['GET'])
def get_diaries_route():
    """取得所有日記"""
    diaries = diary_manager.get_all_diaries()
    print('All diaries:', diaries)  # 添加此行以檢查所有日記內容
    formatted_diaries = []
    
    for diary in diaries:
        formatted_diaries.append({
            'id': diary[0],
            'title': diary[1],
            'content': diary[2],
            'answers': [
                diary[3] if diary[3] else '未回答',
                diary[4] if diary[4] else '未回答',
                diary[5] if diary[5] else '未回答'
            ],
            'created_at': diary[6]
        })
    
    return jsonify(formatted_diaries)

# 網頁的主畫面
@app.route('/Homepage')
def homepage():
    """返回網頁的主畫面"""
    return render_template('Homepage.html')

# 顯示問題的頁面
@app.route('/Question')
def question():
    """返回顯示問題的網頁"""
    return render_template('Question.html')

# 每日一問紀錄的頁面
@app.route('/QuestionShow')
def questionshow():
    """返回每日一問紀錄的網頁"""
    return render_template('QuestionShow.html')

# 顯示日記的主頁面
@app.route('/DairyHome')
def dairyhome():
    """返回日記的主畫面"""
    return render_template('DairyHome.html')

# 顯示日記頁面
@app.route('/Dairy')
def dairy():
    """返回顯示日記的網頁"""
    return render_template('Dairy.html')

# 顯示註冊的主頁面
@app.route('/signup')
def signup():
    """返回顯示註冊的主頁面"""
    return render_template('signup.html')

# 顯示登入的主頁面
@app.route('/signin')
def signin():
    """返回顯示登入的主頁面"""
    return render_template('signin.html')

# 織夢機主頁
@app.route('/DreamWeaverHome')
def dreamweaverhome():
    """返回織夢機主頁"""
    return render_template('DreamWeaverHome.html')

# 織夢機頁面
@app.route('/DreamWeaver')
def dreamweaver():
    """返回織夢機網頁"""
    return render_template('DreamWeaver.html')

# 首頁
@app.route('/')
def index():
    """返回主頁面"""
    return render_template('index.html')

# 啟動應用
if __name__ == '__main__':
    create_tables()  # 在應用啟動前創建資料表
    app.run(debug=True)
