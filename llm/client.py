import os
from openai import OpenAI

def get_llm_client():
    return OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url="https://api.deepseek.com"
    )