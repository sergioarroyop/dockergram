import logging
import re
import constantActions
from telegram import ReplyKeyboardMarkup
from dockerActions.containers import showContainers, showLogs, stopContainer

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
        return constantActions.LOGSCONTAINERS
    elif re.search('^Stop container$', update.message.text):
        return constantActions.STOPCONTAINER

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
    return constantActions.STOPCONTAINER