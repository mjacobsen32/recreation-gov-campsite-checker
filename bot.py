from telegram import Update
from telegram.ext import *
from helpers import *
from constants import API_KEY, parks_file

json_output = False

def make_parks_list(parks_file):
    l = []
    with open(parks_file, 'r') as P:
        for line in P:
           l.append(line.rstrip())
    return(l) 

def response(req):
    return(req)

def start_command(update: Update,context):
    update.message.reply_text("Type a command to begin")

def show_available(update: Update,context):
    cmd = "python camping.py --start-date 2021-08-20 --end-date 2021-09-15 --stdin < parks.txt"
    update.message.reply_text(str(get_available(cmd))) 

def show_sites(update: Update,context):
    update.message.reply_text("displaying sites... ")

def handle_message(update: Update,context):
    text = str(update.message.text).lower()
    update.message.reply_text(response(text))

def check_new(context: CallbackContext):
    job = context.job
    cmd = "python camping.py --start-date 2021-08-20 --end-date 2021-09-15 --stdin < parks.txt"
    available = get_available(cmd)
    none = "There are no campsites available :("
    if none not in available:
        context.bot.send_message(job.context, text=available)

def monitor(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(check_new, (60*5), context=chat_id, name=str(chat_id))

if __name__ == "__main__":
    updater = Updater(API_KEY)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("availability",show_available))
    dp.add_handler(CommandHandler("show_sites",show_sites))
    dp.add_handler(CommandHandler("monitor",monitor))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(1)
    updater.idle()