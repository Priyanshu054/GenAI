from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from the environment variable `GEMINI_API_KEY`.
load_dotenv(override=True)  
api_key = os.getenv('GEMINI_API_KEY')

gemini = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = gemini.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How can you assist me today?"},
    ], max_tokens=100
)   

print(response.choices[0].message.content)
