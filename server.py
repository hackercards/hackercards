from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import sqlite3
import time
import json

from random import shuffle
from flask import Flask, request

def create_deck(file_name):
    with open(file_name) as f:
        color = f.readlines()
    shuffle(color)
    return color

class Game:
    def __init__(self):
        self.black = create_deck('black.txt')
        self.white = create_deck('white.txt')
        self.counter = 1

        self.players = {}


    def add_player(self, name, ws):
        self.players[name] = ws

        cards = []
        for x in range(7):
            cards.append(self.black[self.counter])
            self.counter += 1

        message = {'type': 'join', 'hand': cards}
        ws.send(json.dumps(message))

    def receive_message(name, msg):
        pass


app = Flask(__name__)

game = Game()

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/ws")
def cards():
    global counter
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        name = ws.receive()
        game.add_player(name, ws)
        while True:
            msg = ws.receive()
            game.receive_message(name, msg)

if __name__ == "__main__":
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
