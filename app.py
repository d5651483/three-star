from flask import Flask, request, jsonify, render_template
from db import DiaryManager, QuestManager

# 建立 Flask 應用
app = Flask(__name__)

# 建立 Manager 實例
diary_manager = DiaryManager()
quest_manager = QuestManager()

# 獲取今天的問題
@app.route('/genarate-question', methods=['GET'])
def genarate_question():

    question = quest_manager.generate_daily_question()

    return jsonify(question)

# 新增問題
@app.route('/add-question', methods=['POST'])
def add_question():

    data = request.json

    # 檢查 data
    if data is None: return jsonify({"error": "No data received"}), 400

    question = data.get('question')
    answer = data.get('answer')

    # 檢查 title and content
    if not question or not answer: return jsonify({"error": "Title and content are required"}), 400

    # 新增日記
    quest_manager.add_question(
        question,
        answer
    )

    return jsonify({"message": "Question added successfully"}), 200

@app.route('/get-questions', methods=['GET'])
def get_question():

    # 取得問題
    questions = quest_manager.get_all_question()

    # 轉成陣列
    formatted_questions = [
        {
            'question' : question[1],
            'answer' : question[2],
            'created_at': question[3]
        }
        for question in questions
    ]
    
    print(formatted_questions)

    return jsonify(formatted_questions)

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

# 路徑與 html 名稱
routes_name = {
    '/Homepage': 'Homepage.html',
    '/QuestionShow': 'QuestionShow.html',
    '/DairyHome': 'DairyHome.html',
    '/Dairy': 'Dairy.html',
    '/signup': 'signup.html',
    '/signin': 'signin.html',
    '/DreamWeaverHome': 'DreamWeaverHome.html',
    '/DreamWeaver': 'DreamWeaver.html',
    '/': 'Question.html'
}

# 定義路徑的函數
def def_route(route, template):

    def local_function():
        return render_template(template)
    
    local_function.__name__ = f'route_{route.lstrip("/")}'

    app.route(route)(local_function)

# 定義路徑
routes = [def_route(route, template) for route, template in routes_name.items()]

# 啟動
if __name__ == '__main__':
    app.run(debug=True)