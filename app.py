from flask import Flask, request, jsonify, render_template
import db  # 引入資料庫操作
from datetime import datetime

app = Flask(__name__)

# 獲取今天的問題
@app.route('/get-question', methods=['GET'])
def get_question():
    question = db.generate_daily_question()
    return jsonify(question)

# 新增日記
@app.route('/add-diary', methods=['POST'])
def add_diary():
    data = request.json
    content = data['content']
    db.add_diary(content)
    return jsonify({"message": "日記已儲存！"})

# 取得所有日記
@app.route('/get-diaries', methods=['GET'])
def get_diaries():
    diaries = db.get_all_diaries()
    return jsonify(diaries)

# 主頁面
@app.route('/')
def index():
    return render_template('Question.html')

if __name__ == '__main__':
    db.create_tables()  # 創建資料表
    app.run(debug=True)
