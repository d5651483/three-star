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
        satir_prompt = f"""
            Situation: The user asks: "{user_input}".
            Attitude: Respond in an informative, engaging, and clear way.
            Thinking: The aim is to ensure the user feels informed and satisfied with the response.
            Intent: Generate a helpful and relevant answer.
            Response:
        """
        return satir_prompt

