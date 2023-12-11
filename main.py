from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

# Create a Flask web server
app = Flask(__name__)

# Set your Telegram Bot token
TOKEN = 'YOUR_BOT_TOKEN'
bot = telegram.Bot(token=TOKEN)

# Create a message handler
def echo(update, context):
    text = update.message.text
    update.message.reply_text(f'You said: {text}')

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telegram.Update.de_json(json_str, bot)
    dp = Dispatcher(bot, None)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.process_update(update)
    return 'OK'

if __name__ == '__main__':
    app.run()
