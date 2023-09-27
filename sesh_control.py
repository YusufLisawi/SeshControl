from dotenv import load_dotenv
import os
import telebot
from time import sleep
import uuid
from utils import sleepnow
from multiprocessing import Process
from pynput.mouse import Controller
import Quartz
import time

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

while not BOT_TOKEN:
    if not BOT_TOKEN:
        BOT_TOKEN = input("Enter your bot token: ")
        if not BOT_TOKEN:
            print("Please enter your bot token")
            continue
        with open(".env", "a") as f:
            f.write(f"BOT_TOKEN={BOT_TOKEN}\n")

bot = telebot.TeleBot(BOT_TOKEN)

print("Bot is running...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "/sleep - put your computer to sleep\n/cluster - open the cluster and take screenshot\n/screenshot - take a screenshot and send it to you\n/image - take an image\n/dontmove - put your computer to sleep if someone move your mouse\n/open - open a link in the default browser")

@bot.message_handler(commands=['sleep'])
def sleep_handler(message):
    os.system("pmset displaysleepnow")
    bot.reply_to(message, "Your computer have been put to sleep.")

@bot.message_handler(commands=['cluster'])
def cluster_handler(message):
    my_uuid = str(uuid.uuid4())
    file_path = f"/tmp/screen_{my_uuid}.jpg"
    os.system("open https://meta.intra.42.fr/clusters")
    bot.reply_to(message, "Opening the cluster...")
    bot.reply_to(message, "Taking screenshot...")
    sleep(5)
    os.system(f"screencapture {file_path}")
    bot.reply_to(message, "Sending screenshot...")
    bot.send_photo(message.chat.id, photo=open(file_path, 'rb'))

@bot.message_handler(commands=['screenshot'])
def screenshot_handler(message):
    my_uuid = str(uuid.uuid4())
    file_path = f"/tmp/screen_{my_uuid}.jpg"
    bot.reply_to(message, "Taking screenshot...")
    os.system(f"screencapture {file_path}")
    bot.reply_to(message, "Sending screenshot...")
    bot.send_photo(message.chat.id, photo=open(file_path, 'rb'))

@bot.message_handler(commands=['image'])
def image_handler(message):
    my_uuid = str(uuid.uuid4())
    file_path = f"/tmp/image_{my_uuid}.jpg"
    bot.reply_to(message, "Sending screenshot...")
    os.system(f"imagesnap {file_path}")
    bot.send_photo(message.chat.id, photo=open(file_path, 'rb'))

@bot.message_handler(commands=['dontmove'])
def dontmove_handler(message):
    bot.reply_to(message, "I will put your computer to sleep if someone move your mouse.")
    p = Process(target=dont_move(message))
    p.start()

def dont_move(message):
    mouse = Controller()
    init_x ,init_y = mouse.position
    while True:
        current_x, current_y = mouse.position
        if current_x != init_x or current_y != init_y:
            bot.reply_to(message, "Someone moved your mouse.")
            file_path = sleepnow()
            bot.reply_to(message, "Your computer have been put to sleep.")
            bot.send_photo(message.chat.id, photo=open(file_path, 'rb'))
            return 1

@bot.message_handler(commands=['open'])
def open_handler(message):
    try:
        link = message.text.split()[1]
        if (link[:8] != "https://"):
            link = "https://" + link
        os.system(f"open {link}")
        bot.reply_to(message, f"Opening {link} in the default browser...")
    except:
        bot.reply_to(message, "Please enter a valid link.")

@bot.message_handler(commands=['lock'])
def lock_handler(message):
    p = Process(target=lock_listener(message))
    p.start()

def dont_move(message):
    mouse = Controller()
    init_x ,init_y = mouse.position
    while True:
        current_x, current_y = mouse.position
        if current_x != init_x or current_y != init_y:
            bot.reply_to(message, "Someone moved your mouse.")
            file_path = sleepnow()
            bot.reply_to(message, "Your computer have been put to sleep.")
            bot.send_photo(message.chat.id, photo=open(file_path, 'rb'))
            return 1

def lock_screen():
    d = Quartz.CGSessionCopyCurrentDictionary()
    return d.get("CGSSessionScreenIsLocked", 0) == 1

def lock_listener(message):
    bot.send_message(message.chat.id, "I will notify you when your session is about to be terminated, I got your back.")
    while True:
        if lock_screen():
            current_time = time.time()
            print("Screen is locked")
            print("Current time: " + str(current_time))
            lock_time = current_time
            while True:
                if not lock_screen():
                    print("Screen is unlocked")
                    break
                elapsed_time = time.time() - lock_time
                if elapsed_time >= 1800:  # 30 minutes
                    bot.send_message(message.chat.id, "Come back your session is about to be terminated!!!!.")
                    break
                else:
                    print(f"Time elapsed: {int(elapsed_time)} seconds")
                time.sleep(60)
        else:
            print("Screen is not locked")
        time.sleep(60)

if __name__ == "__main__":
    
    bot.infinity_polling()

"""
sleep - put your computer to sleep
cluster - open the cluster and take screenshot
screenshot - take a screenshot and send it to you
image - take an image
dontmove - put your computer to sleep if someone move your mouse
open - open a link in the default browser
"""