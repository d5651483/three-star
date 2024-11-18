from os import getenv
from dotenv import load_dotenv
from flask import request

class AI_Manager:

    def __init__(self) -> None:

        # 使用 OpenAI API 的參數
        load_dotenv()
        self.openai_api_key = getenv("OPENAI_API_KEY")
        self.api_url = getenv("APIURL")

    def get_response(self, user_input) -> dict:
        
        satir_prompt = self.generate_content(user_input)
        
        # 發送請求至 OpenAI API
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": satir_prompt}]
        }

        response = request.post(self.api_url, headers=headers, json=data)
        response_json = response.json()
        
        if response.status_code == 200 and "choices" in response_json:
            bot_response = response_json["choices"][0]["message"]["content"]
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