import os

from flask import Flask, request
from openai import OpenAI
from telegram import Update, Bot

# 初始化Flask應用和Telegram機器人
app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


# 新增簡單的首頁路由
@app.route('/')
def index():
    return "Hello Simbo!"


# 定義收到Telegram訊息時的處理函數
async def handle_message(update: Update):
    message_text = update.message.text
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an experienced translator. When you want to translate other languages into Chinese, you will use concise and short text and retain the original meaning. When you get a message which is in Chinese, translate it into English. If it is not Chinese, it will be translated into Traditional Chinese."},
            {"role": "user",
             "content": message_text}
        ]
    )
    async with bot:
        await bot.send_message(chat_id=update.effective_chat.id, text=completion.choices[0].message.content)


# 設定Telegram機器人的webhook路徑，用於接收訊息
@app.route('/telegram', methods=['POST'])
async def webhook():
    json_str = request.get_json()
    update = Update.de_json(json_str, bot)
    await handle_message(update)
    return 'OK'


@app.route('/get_token')
def get_token():
    return TOKEN


if __name__ == '__main__':
    # 啟動Flask應用
    app.run(debug=True)
