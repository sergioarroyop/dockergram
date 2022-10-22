from cgi import test
from telegram.ext import Updater
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import emoji
import re
import docker
import os
import logging

from scripts.containers import showContainers, showLogs, stopContainer
from scripts.images import showImages

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
load_dotenv()
dclient = docker.from_env()

ACTIONS, CONTAINERS, LOGSCONTAINERS, STOPCONTAINER, IMAGES = range(5)

def start(update, context):
    first_keyboard = [
        ['Help \N{gear}', 'Containers \N{package}', 'Images \N{page facing up}'], 
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
        ['Show containers', 'Container logs', 'Stop container'],
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(containers_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Containers menu",reply_markup=reply_markup)

    return CONTAINERS

def images(update, context):
    images_keyboard = [
        ['Show images'],
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(images_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Images menu",reply_markup=reply_markup)

    return IMAGES

# Functions
def showContainersCommand(update, context):
    logging.info(msg='Showing containers')
    containers = showContainers()
    context.bot.send_message(chat_id=update.effective_chat.id, text="These are your running containers")
    for container in containers:
        text_formated = 'Id:<code>%s</code>\nName:<code>%s</code>\nStatus:<code>%s</code>' % (container['Id'], container['Name'], container['Status'])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='HTML',text=text_formated)

def showContainerListCommand(update, context):
    logging.info(msg='Gettings containers')
    containers = showContainers()
    container_name = []
    for container in containers:
        container_name.append(container['Name'])

    containerList = [
        container_name,
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(containerList, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Select a container",reply_markup=reply_markup)

    if re.search('^Container logs$', update.message.text):
        return LOGSCONTAINERS
    elif re.search('^Stop container$', update.message.text):
        return STOPCONTAINER

def showContainerLogsId(update, context):
    logging.info(msg='Show ' + update.effective_message.text + ' logs')
    logs = showLogs(update.effective_message.text)
    if len(logs) > 4096:
        for x in range(0, len(logs), 4096):
            context.bot.send_message(chat_id=update.effective_chat.id,text=logs[x:x+4096])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text=logs)

def stopContainers(update, context):
    logging.info(msg='Stopping ' + update.effective_message.text + ' container')
    stop_log = stopContainer(update.effective_message.text)
    if stop_log == None:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Container stopped succesfuly")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Container stopped error")
        context.bot.send_message(chat_id=update.effective_chat.id,text=stop_log)
    return STOPCONTAINER

def showImagesCommand(update, context):
    logging.info(msg='Showing images')
    images = showImages()
    context.bot.send_message(chat_id=update.effective_chat.id, text="These are your images")
    for image in images:
        text_formated = 'Id:<code>%s</code>\nTags:<code>%s</code>' % (image['Id'], image['Tags'])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='HTML', text=text_formated)

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
                MessageHandler(Filters.regex('^Images \N{page facing up}$'), images),
                MessageHandler(Filters.regex('^Help \N{gear}$'), helper),
            ],
            CONTAINERS: [
                MessageHandler(Filters.regex('^Show containers$'), showContainersCommand),
                MessageHandler(Filters.regex('^Container logs$'), showContainerListCommand),
                MessageHandler(Filters.regex('^Stop container$'), showContainerListCommand),
                MessageHandler(Filters.regex('^Go back$'), start)
            ],
            LOGSCONTAINERS: [
                MessageHandler(Filters.regex('^Go back$'), containers),
                MessageHandler(Filters.text, showContainerLogsId)
            ],
            STOPCONTAINER: [
                MessageHandler(Filters.regex('^Go back$'), containers),
                MessageHandler(Filters.text, stopContainers)
            ],
            IMAGES: [
                MessageHandler(Filters.regex('^Show images$'), showImagesCommand),
                MessageHandler(Filters.regex('^Go back$'), start)
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
