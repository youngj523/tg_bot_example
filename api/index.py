import os

from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CallbackContext

# 初始化Flask應用和Telegram機器人
app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


# 新增簡單的首頁路由
@app.route('/')
def index():
    return "Hello Simbo!"


# 定義收到Telegram訊息時的處理函數
def handle_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    response_text = "From Bot: " + message_text
    update.message.reply_text(response_text)


# 設定Telegram機器人的webhook路徑，用於接收訊息
@app.route('/telegram', methods=['POST'])
def webhook():
    json_str = request.get_json()
    update = Update.de_json(json_str, bot)
    handle_message(update, None)
    return 'OK'


@app.route('/hook_test')
def hook_test():
    return 'OK'

if __name__ == '__main__':
    # 啟動Flask應用
    app.run(debug=True)
