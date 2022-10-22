from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import constantActions

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

    return constantActions.ACTIONS

def containers(update, context):
    containers_keyboard = [
        ['Show containers', 'Container logs', 'Stop container'],
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(containers_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Containers menu",reply_markup=reply_markup)

    return constantActions.CONTAINERS

def images(update, context):
    images_keyboard = [
        ['Show images'],
        ['Go back']
    ]
    reply_markup = ReplyKeyboardMarkup(images_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Images menu",reply_markup=reply_markup)

    return constantActions.IMAGES

def helper(update, context):
    help_text = """
Hello, I'm Dockergram bot :)

Please, select an option in the main menu. I can show you your running containers or maybe other things.
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def done(update, context):
    update.message.reply_text("Bye bye")

    return ConversationHandler.END