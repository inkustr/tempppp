from flask import Flask
import google.generativeai as genai
# import env
from os import env

app = Flask(__name__)
API_KEY = env.get("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


# id: Int -> chat: array of some shit
chats = dict()

@app.route('/<chat_id>/<query>')
def hello_world(chat_id: int, query: str):  # put application's code here
    chat = None
    if chat_id in chats:
        chat = model.start_chat(history=chats[chat_id].history)
    else:
        chat = model.start_chat(history=[])
        chats[chat_id] = chat

    chat.send_message(query)
    chats[chat_id] = chat

    history = []

    for msg in chat.history:
        history.append(
            {
                "role": msg.role,
                "text": msg.parts[0].text
            }
        )

    return history

if __name__ == '__main__':
    app.run()