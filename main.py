import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 設定日誌
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 輸入你的 Telegram Bot token
TOKEN = '6651199681:AAG6Sq0RPApdF3ZFygDDRFYml5LUAtQwFw0'

# 創建 Updater 物件，用於處理 Telegram Bot 的 API 請求
updater = Updater(token=TOKEN, use_context=True)

# 創建一個處理 `/start` 命令的函數
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}!',
        reply_markup=None,
    )

# 創建一個處理收到的訊息的函數
def echo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    text = update.message.text
    update.message.reply_text(f'Hello {user.mention_html()}! You said: {text}')

# 創建一個處理未知命令的函數
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I don't understand that command.")

# 創建指令處理器和訊息處理器
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dp.add_handler(MessageHandler(Filters.command, unknown))

# 開始運行 Bot
updater.start_polling()
updater.idle()
