from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from the environment variable `OPENAI_API_KEY`.
load_dotenv(override=True)  
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI(api_key=api_key)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How can you assist me today?"},
    ]
)   

print(response.choices[0].message.content)