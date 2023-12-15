import os

from flask import Flask, request
from telegram import Update
from telegram.ext import CallbackContext, ApplicationBuilder, CommandHandler, ContextTypes

# 初始化Flask應用和Telegram機器人
app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
# bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()


# 新增簡單的首頁路由
@app.route('/')
def index():
    return "Hello Simbo!"


# 定義收到Telegram訊息時的處理函數
async def handle_message(update: Update, context: CallbackContext):
    # message_text = update.message.text
    # response_text = "From Bot: " + message_text
    # await update.message.reply_text(response_text)
    return update.message.text


# 設定Telegram機器人的webhook路徑，用於接收訊息
@app.route('/telegram', methods=['POST'])
async def webhook():
    json_str = request.get_json()
    update = Update.de_json(json_str, bot)
    await handle_message(update, None)
    return 'OK'


@app.route('/get_token')
def get_token():
    return TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # 啟動Flask應用
    app.run(debug=True)
