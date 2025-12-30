import requests
import json
from dotenv import load_dotenv
import os

# Load API key from the environment variable `GEMINI_API_KEY`.
load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

payload = {
    "model": "gemini-2.5-flash-lite",
    "messages": [
        {"role": "user", "content": "Tell me a fun fact"}]
}

payload_json = json.dumps(payload)

response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    headers=headers,
    data=payload_json
)

print(response.json()['choices'][0]['message']['content'])
