from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4  


app = Flask(__name__)

# ✅ Groq API Config
API_KEY = "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"
MODEL = "llama3-8b-8192"

# ✅ MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Change if hosted remotely
db = client["chatbot_db"]
collection = db["conversations"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/conversations')
def conversations():
    # Fetch all conversations from MongoDB, newest first
    chats = list(collection.find().sort("timestamp", -1))
    return render_template('conversations.html', chats=chats)


@app.route('/recent_chats')
def recent_chats():
    chats = list(collection.find().sort("timestamp", -1).limit(5))
    for chat in chats:
        chat['_id'] = str(chat['_id'])  # convert ObjectId to string
    return jsonify(chats)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json  # ✅ FIXED
    user_message = data.get('message')
    chat_id = data.get('chat_id') or str(uuid4())

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]

        collection.insert_one({
            "chat_id": chat_id,
            "timestamp": datetime.now(),
            "user_message": user_message,
            "bot_reply": bot_reply
        })

        return jsonify({'reply': bot_reply})
    else:
        error_msg = f"Error: {response.status_code} - {response.text}"

        collection.insert_one({
            "chat_id": chat_id,
            "timestamp": datetime.now(),
            "user_message": user_message,
            "bot_reply": error_msg
        })

        return jsonify({'reply': error_msg}), 500


   


if __name__ == '__main__':
    app.run(debug=True)
