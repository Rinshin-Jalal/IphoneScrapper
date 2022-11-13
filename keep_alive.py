from flask import Flask
from threading import Thread
import os

app = Flask('/')

port = os.environ.get('PORT')


@app.route('/')
def home():
    return "hello , I am Live"


def run():
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()
