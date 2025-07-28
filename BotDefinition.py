import requests

API_KEY = "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"  # Replace with your actual Groq API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-8b-8192",  # You can also try: "llama3-70b-8192", "mixtral-8x7b-32768"
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the meaning of life?"}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print("Bot:", reply)
else:
    print("Error:", response.status_code, response.text)
