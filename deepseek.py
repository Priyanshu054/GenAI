from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from the environment variable `DEEPSEEK_API_KEY`.
load_dotenv(override=True)  
api_key = os.getenv('DEEPSEEK_API_KEY')

deepseek = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = deepseek.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How can you assist me today?"},
    ]
)   

print(response.choices[0].message.content)