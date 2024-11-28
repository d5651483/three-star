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
            情況：使用者提問："{user_input}"。織夢機扮演的是一個回答者的角色，使用者則是有疑惑的人。
            回答方式：使用開放式問答，引導使用者進行自我反思，一次提問一個問題。盡量精簡，只說重點。
            回答技巧：從最近提問人的選擇或事件開始，這樣可以幫助使用者反思當下的情緒或想法，盡量不重複相同的回答。
            回應方式：直接進行引導，避免深入探討自殺等危險性話題，讓對話保持正向和支持。
            態度：保持溫暖和同理心，運用薩提爾自我覺察練習方法，讓回應充滿感情和理解。
            意圖：提供有幫助、具體且相關的回答，讓使用者能夠進行深度的自我探索和情感釋放。
            要做的事：觀察使用者是否有迷茫與不安，又或是對某些東西具有熱忱，並且往這些方向追問。
            需要注意的內容：回答的提問要簡單扼要，回答的時候不需要加上誰說的，不要重複跳針重複一件事情。
            回答(織夢機) :
        """
        return memery + satir_prompt

