from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
load_dotenv()
dclient = docker.from_env()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def helper(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="This are the availables commands:\n /help")

def main():

    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    ud = updater.dispatcher

    ud.add_handler(CommandHandler('start', start))
    ud.add_handler(CommandHandler('help', helper))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()