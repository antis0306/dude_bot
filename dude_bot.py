import telebot
from telebot import types
import datetime
import time
import os
import random
import schedule

chatId = ""
TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

# Read "/wednesday" key, send a response with a Frog pic
@bot.message_handler(commands=["wednesday"])
def sendWednesdayFrog(message):
    chatId = message.chat.id
    sendFrog(chatId)

# Main func to start the bot, read "/dude" key
# Runs schedule for automatic Wednesday Frog pic sendout: wednesdayFrog
# Runs schedule for keening connection alive: connectionPing
@bot.message_handler(commands=["dude"])
def starter(message):
    chatId = message.chat.id
    print(chatId)
    bot.send_message(chatId, "Хуюд...")
    wednesdayFrog(chatId)
    connectionPing(message)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Read "dude_help"
@bot.message_handler(commands=["dude_help"])
def open_coub(message):
    chatId = message.chat.id
    bot.send_message(chatId, "Here's what I can do, dude:")
    bot.send_message(chatId, "/wednesday - Send a frog if it's Wednesday\nAlso I'm sending a Frog picture every Wednesday at 10AM")

# Send a random Frog pic
def sendFrog(chatId):
    if(isWednesday() == True):
        bot.send_photo(chatId, photo=open(getRangomPic("./dudes"), "rb"))
    else:
        bot.send_message(chatId, "It's NOT Wednesday, dude! Stop it!")
        bot.send_photo(chatId, photo=open(getRangomPic("./not"), "rb"))

# Check if it's Wednesday today
# Output: True/False
def isWednesday():
    day = datetime.datetime.today().weekday()
    print (day)
    if (day==2):
        return True
    return False

# Schedule an automatic Wednesday Frog pic send
def wednesdayFrog(chatId):
    schedule.every().wednesday.at("10:00").do(sendFrog, chatId)

# Choose a random pic from dir
# Input: path to dir
# Output: path to a ramdom pic in dir
def getRangomPic(path):
    files = os.listdir(path)
    d = random.choice(files)

    return path+"/"+d

# Ping every 10 min to keep API connection alive
def connectionPing(msg):
    schedule.every(10).minutes.do(setChatId, msg)

# Pointless function for Ping
def setChatId(message):
    chatId = message.chat.id
    dt = datetime.datetime.now()
    print(dt," Ping (chatId Updated)")

bot.polling()
