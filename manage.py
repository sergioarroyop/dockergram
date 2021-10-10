from telegram.ext import Updater
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import emoji
import docker
import os
import logging

from scripts.containers import showContainers, showLogs

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
load_dotenv()
dclient = docker.from_env()

ACTIONS, CONTAINERS, LOGSCONTAINERS = range(3)

def start(update, context):
    first_keyboard = [
        ['Help \N{gear}', 'Containers \N{package}'], 
        #['images', 'volumes'],
        ['Exit \N{door}']
    ]
    reply_markup = ReplyKeyboardMarkup(first_keyboard, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! I'm Dockergram. Select an option to check your docker containers and misc.",
        reply_markup=reply_markup
    )

    return ACTIONS

def containers(update, context):
    containers_keyboard = [
        ['Show containers', 'Container logs'],
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(containers_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Containers menu",reply_markup=reply_markup)

    return CONTAINERS

# Functions
def showContainersCommand(update, context):
    logging.info(msg='Showing containers')
    containers = showContainers()
    context.bot.send_message(chat_id=update.effective_chat.id, text="These are your running containers")
    for container in containers:
        text_formated = 'Id: `%s`\nName: %s\nStatus: %s' % (container['Id'], container['Name'], container['Status'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_formated)

def showContainerLogs(update, context):
    logging.info(msg='Gettings containers')
    containers = showContainers()
    container_name = []
    for container in containers:
        container_name.append(container['Name'])
        #text_formated = 'Id: `%s`\nName: %s' % (container['Id'], container['Name'])
        #context.bot.send_message(chat_id=update.effective_chat.id, text=text_formated)

    containers_logs = [
        container_name,
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(containers_logs, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Select a container",reply_markup=reply_markup)

    return LOGSCONTAINERS

def showContainerLogsId(update, context):
    logging.info(msg='Show ' + update.effective_message.text + ' logs')
    logs = showLogs(update.effective_message.text)
    if len(logs) > 4096:
        for x in range(0, len(logs), 4096):
            context.bot.send_message(chat_id=update.effective_chat.id,text=logs[x:x+4096])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text=logs)


# Functions
def helper(update, context):
    help_text = """
Hello, I'm Dockergram bot :)

Please, select an option in the main menu. I can show you your running containers or maybe other things.
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def done(update, context):
    update.message.reply_text("Bye bye")

    return ConversationHandler.END

def main():

    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    ud = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTIONS: [
                MessageHandler(Filters.regex('^Containers \N{package}$'), containers),
                MessageHandler(Filters.regex('^Help \N{gear}$'), helper),
            ],
            CONTAINERS: [
                MessageHandler(Filters.regex('^Show containers$'), showContainersCommand),
                MessageHandler(Filters.regex('^Container logs$'), showContainerLogs),
                MessageHandler(Filters.regex('^Go back$'), start)
            ],
            LOGSCONTAINERS: [
                MessageHandler(Filters.regex('^Go back$'), start),
                MessageHandler(Filters.text, showContainerLogsId)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.regex('^Exit \N{door}'), done)
        ]
    )
    
    ud.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()