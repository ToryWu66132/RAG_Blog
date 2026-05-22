from openai import OpenAI

class DeepSeekLLM:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.deepseek.com",
            api_key="API_KEY"
        )

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content