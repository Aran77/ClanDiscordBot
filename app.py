#!/home/propertypitcher/virtualenv/discordbot/3.7/bin/python3.7

from threading import Thread
from flask import Flask
import bot as bot

#set up basic flask app
app = Flask(__name__)

t = Thread(target=bot.run)
t.start()

@app.route('/')
def index():
    return('Discord bot is running!!')



    