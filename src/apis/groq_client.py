import os
from groq import Groq
from src.config import GROQ_API_KEY
from src.utils import retry

class GroqClient:
    """
    Client for Groq Cloud API (Llama-3).
    """
    def __init__(self, api_key=GROQ_API_KEY, model="llama3-8b-8192"):
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set.")
        self.client = Groq(api_key=api_key)
        self.model = model

    @retry(Exception, tries=3, delay=1)
    def generate_content(self, prompt, system_prompt="You are a helpful assistant."):
        """
        Generates text using the Groq API.
        """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content

if __name__ == "__main__":
    try:
        client = GroqClient()
        print("GroqClient initialized.")
    except Exception as e:
        print(f"Error: {e}")
