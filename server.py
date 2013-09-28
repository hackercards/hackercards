from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import sqlite3
import time
import json

from random import shuffle
from flask import Flask, request

app = Flask(__name__)


def create_deck(file_name):
    with open(file_name) as f:
        color = f.readlines()
    shuffle(color)
    return color


black = create_deck('black.txt')
white = create_deck('white.txt')
counter = 1




@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route("/ws")
def cards():
    global counter
    if request.environ.get('wsgi.websocket'):
        cards = []
        for x in range(7):
            cards.append(black[counter])
            counter += 1
     
        ws = request.environ['wsgi.websocket']
        message = {'type': 'join', 'hand': cards}
        ws.send(json.dumps(message))



if __name__ == "__main__":
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()