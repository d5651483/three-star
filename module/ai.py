from os import getenv
from dotenv import load_dotenv
import requests  # 使用 requests 库來發送 HTTP 請求
from module.db import AIManager

class AI_Talker:

    def __init__(self) -> None:
        # 使用 OpenAI API 的參數
        load_dotenv()
        self.openai_api_key = getenv("OPENAI_API_KEY")
        self.api_url = getenv("APIURL")

        self.ai_mananger = AIManager()

    def get_response(self, user_input) -> dict:
        
        self.ai_mananger.write('User', user_input)

        satir_prompt = self.generate_content(user_input)

        # 發送請求至 OpenAI API
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": satir_prompt}]
        }

        # 使用 requests 库發送 POST 請求
        response = requests.post(self.api_url, headers=headers, json=data)
        response_json = response.json()

        if response.status_code == 200 and "choices" in response_json:
            bot_response = response_json["choices"][0]["message"]["content"]
            self.ai_mananger.write('織夢機', bot_response)
            return {"response": bot_response}
        else:
            return {"response": "Sorry, I couldn't process your request."}

    def generate_content(self, user_input) -> str:

        records = self.ai_mananger.lessRecord()

        memery = "回答紀錄 : \n"

        for record in records:

            memery += f"{record['author']} : {record['content']} \n"

        satir_prompt = f"""
            情況 : 使用者提問 : "{user_input}".
            回答方式 : 使用開放式問答，你當引導者，一次一個問題。
            回答技巧 : 用最近有哪些選擇或是事件會讓你感到不安、迷茫 作為開頭。目的是確保用戶產生對自我的反思。
            回答注意事項 : 直接進行引導，不需要說你如何引導我。給予具體的描述，並使用開放式問答。
            態度 : 使用薩提爾自我覺察練習，產生人性化的回覆。回應具有感情，溫度感。
            意圖 : 產生有用且相關的答案，不深入討論具有危險性值的回答，如自殺。精簡回答，一次一個問題，提供具體回應。
            利用薩提爾的對話方式進行引導
            回答 :
        """
        return memery + satir_prompt

