import streamlit as st
from openai import OpenAI
from typing import List, Dict

class AIAssistant:
    def __init__(self):
        try:
            self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        except Exception:
            self.client = None
            
        self.history: List[Dict[str, str]] = []
        self.system_prompt = "You are a helpful assistant."

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def send_message(self, user_message: str):
        if not self.client:
            return "Error: OpenAI API Key not found in .streamlit/secrets.toml"

        self.history.append({"role": "user", "content": user_message})

        messages_to_send = [{"role": "system", "content": self.system_prompt}] + self.history

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages_to_send
            )
            ai_text = response.choices[0].message.content
            
            self.history.append({"role": "assistant", "content": ai_text})
            return ai_text

        except Exception as e:
            return f"Error contacting OpenAI: {e}"

    def clear_history(self):
        self.history = []