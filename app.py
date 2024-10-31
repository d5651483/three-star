from flask import Flask, request, jsonify, render_template
from db import DiaryManager, QuestManager

# 建立 Manager 實例
diary_manager = DiaryManager()
quest_manager = QuestManager()

# 建立 Flask 應用
app = Flask(__name__)

# 獲取今天的問題
@app.route('/get-question', methods=['GET'])
def get_question():
    """返回今天的問題"""
    question = quest_manager.generate_daily_question()
    return jsonify(question)

# 新增日記
@app.route('/add-diary', methods=['POST'])
def add_diary_route():

    data = request.json

    # 檢查 data
    if data is None: return jsonify({"error": "No data received"}), 400

    title = data.get('title')
    content = data.get('content')
    answers = data.get('answers')

    # 檢查 title and content
    if not title or not content: return jsonify({"error": "Title and content are required"}), 400

    # 檢查 answers
    if not answers or len(answers) != 3: return jsonify({"error": "Invalid answers format"}), 400

    # 新增日記
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

    # 取得日記
    diaries = diary_manager.get_all_diaries()

    # print('All diaries:', diaries)  # 添加此行以檢查所有日記內容

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
    
    return jsonify(formatted_diaries)

# 網頁的主畫面
@app.route('/Homepage')
def homepage():
    return render_template('Homepage.html')

# 顯示問題的頁面
@app.route('/Question')
def question():
    return render_template('Question.html')

# 每日一問紀錄的頁面
@app.route('/QuestionShow')
def questionshow():
    return render_template('QuestionShow.html')

# 顯示日記的主頁面
@app.route('/DairyHome')
def dairyhome():
    return render_template('DairyHome.html')

# 顯示日記頁面
@app.route('/Dairy')
def dairy():
    return render_template('Dairy.html')

# 顯示註冊的主頁面
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 顯示登入的主頁面
@app.route('/signin')
def signin():
    return render_template('signin.html')

# 織夢機主頁
@app.route('/DreamWeaverHome')
def dreamweaverhome():
    return render_template('DreamWeaverHome.html')

# 織夢機頁面
@app.route('/DreamWeaver')
def dreamweaver():
    return render_template('DreamWeaver.html')

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 啟動應用
if __name__ == '__main__':
    app.run(debug=True)