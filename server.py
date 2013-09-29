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

class Deck:
    def __init__(self, file_name):
        with open(file_name) as f:
            self.deck = f.readlines()
        shuffle(self.deck)
        self.position = 0

    def deal_card(self):
        if self.position > len(self.deck)
            shuffle(self.deck)
            position = 0
        return self.deck[position]

    def deal_cards(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.deal_card())
        return cards

class Game:
    def __init__(self):
        self.black = Deck('black.txt')
        self.white = Deck('white.txt')
        self.players = []
        self.started = False

    def add_player(self, name, ws):
        self.players.append((name, ws))

        cards = self.black.deal_cards(7)
        message = {'type': 'join', 'hand': cards}
        ws.send(json.dumps(message))

        if not self.started and len(self.players) == 3:
            self.start_game()


    def start_game(self):
        self.started = True

    def receive_message(self, name, msg):
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
