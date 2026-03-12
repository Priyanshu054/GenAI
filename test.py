import requests

url = "http://localhost:11434/v1/chat/completions"

data = {
    "model": "gemma3",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant. Answer the user's question as concisely as possible."},
        {"role": "user", "content": "Hello! How can you assist me today?"},
    ],
}

r = requests.post(url, json=data)
print(r.json()["choices"][0]["message"]["content"])