from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import sqlite3
import time
import json

from random import shuffle
from flask import Flask, request

app = Flask(__name__)

black = create_deck('black.txt')
white = create_deck('white.txt')


def create_deck(file_name):
    with open(file_name) as f:
        color = f.readlines()
    shuffle(color)
    return color

@app.route("/")
def hello():
    return app.send_static_file('index.html')

    
@app.route("/ws")
def cards():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        cards =     
        message = {'type': 'join', 'hand': cards}
        ws.send(json.dumps(message))



if __name__ == "__main__":
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()