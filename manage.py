from email.mime import image
from telegram.ext import Updater
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from dotenv import load_dotenv
import emoji
import os
import logging
import constantActions
import telegramFunctions.menu as menuFunctions, telegramFunctions.containers as containerFunctions, telegramFunctions.images as imageFunctions

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
load_dotenv()

def main():

    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    ud = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', menuFunctions.start)],
        states={
            constantActions.ACTIONS: [
                MessageHandler(Filters.regex('^Containers \N{package}$'), menuFunctions.containers),
                MessageHandler(Filters.regex('^Images \N{page facing up}$'), menuFunctions.images),
                MessageHandler(Filters.regex('^Help \N{gear}$'), menuFunctions.helper),
            ],
            constantActions.CONTAINERS: [
                MessageHandler(Filters.regex('^Show containers$'), containerFunctions.showContainersCommand),
                MessageHandler(Filters.regex('^Container logs$'), containerFunctions.showContainerListCommand),
                MessageHandler(Filters.regex('^Stop container$'), containerFunctions.showContainerListCommand),
                MessageHandler(Filters.regex('^Go back$'), menuFunctions.start)
            ],
            constantActions.LOGSCONTAINERS: [
                MessageHandler(Filters.regex('^Go back$'), menuFunctions.containers),
                MessageHandler(Filters.text, containerFunctions.showContainerLogsId)
            ],
            constantActions.STOPCONTAINER: [
                MessageHandler(Filters.regex('^Go back$'), menuFunctions.containers),
                MessageHandler(Filters.text, containerFunctions.stopContainers)
            ],
            constantActions.IMAGES: [
                MessageHandler(Filters.regex('^Show images$'), imageFunctions.showImagesCommand),
                MessageHandler(Filters.regex('^Go back$'), menuFunctions.start)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.regex('^Exit \N{door}'), menuFunctions.done)
        ]
    )
    
    ud.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
