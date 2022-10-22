import logging
from dockerActions.images import showImages

def showImagesCommand(update, context):
    logging.info(msg='Showing images')
    images = showImages()
    context.bot.send_message(chat_id=update.effective_chat.id, text="These are your images")
    for image in images:
        text_formated = 'Id:<code>%s</code>\nTags:<code>%s</code>' % (image['Id'], image['Tags'])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='HTML', text=text_formated)