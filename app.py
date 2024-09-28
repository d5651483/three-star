from flask import Flask, request, jsonify, render_template
import db  # 引入資料庫操作模組
from datetime import datetime  # 引入日期時間模組

# DiaryManager 類別，負責管理與日記相關的操作
class DiaryManager:
    def __init__(self):
        pass

    def add_diary(self, content):
        """
        新增日記到資料庫中。
        :param content: 日記內容
        """
        db.add_diary(content)  # 將日記內容存入資料庫
        return {"message": "日記已儲存！"}

    def get_all_diaries(self):
        """
        取得所有日記。
        :return: 日記列表
        """
        diaries = db.get_all_diaries()  # 從資料庫中取得所有日記
        return diaries

# 建立 DiaryManager 實例
diary_manager = DiaryManager()

# 建立 Flask 應用
app = Flask(__name__)

# 獲取今天的問題
@app.route('/get-question', methods=['GET'])
def get_question():
    """
    這個路由會在使用者訪問 /get-question 時，返回今天的問題。
    問題是從資料庫中生成的每日問題。
    """
    question = db.generate_daily_question()  # 從資料庫中取得今日問題
    return jsonify(question)  # 將問題轉成 JSON 格式返回

# 新增日記
@app.route('/add-diary', methods=['POST'])
def add_diary():
    """
    這個路由會在使用者透過 POST 請求發送日記內容時，將日記儲存在資料庫中。
    前端會以 JSON 格式傳遞日記內容，後端將其儲存。
    """
    data = request.json  # 取得前端傳來的 JSON 資料
    content = data['content']  # 從 JSON 資料中提取日記內容
    response = diary_manager.add_diary(content)  # 使用 DiaryManager 類別來新增日記
    return jsonify(response)  # 返回成功訊息

# 取得所有日記
@app.route('/get-diaries', methods=['GET'])
def get_diaries():
    """
    這個路由會在使用者訪問 /get-diaries 時，返回所有儲存在資料庫中的日記。
    """
    diaries = diary_manager.get_all_diaries()  # 使用 DiaryManager 類別來取得所有日記
    return jsonify(diaries)  # 將日記列表轉成 JSON 格式返回

# 顯示問題的主頁面
@app.route('/Question')
def question():
    """
    這個路由會在使用者訪問 /Question 時，返回顯示問題的網頁。
    """
    return render_template('Question.html')  # 返回 Question.html 模板

# 顯示日記的主頁面
@app.route('/Dairy')
def dairy():
    """
    這個路由會在使用者訪問 /Dairy 時，返回顯示日記的網頁。
    """
    return render_template('Dairy.html')  # 返回 Dairy.html 模板

# 首頁
@app.route('/')
def index():
    """
    這個路由會在使用者訪問網站根目錄時，返回主頁面。
    """
    return render_template('index.html')  # 返回 Hi.html 模板

# 啟動應用
if __name__ == '__main__':
    db.create_tables()  # 在應用啟動前創建資料表
    app.run(debug=True)  # 啟動 Flask 應用並啟用 debug 模式
