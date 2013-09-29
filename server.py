from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import sqlite3
import time
import json

from random import shuffle
from flask import Flask, request

class Deck:
    def __init__(self, file_name):
        #takes text file and converts cards on lines into a list
        with open(file_name) as f:
            self.deck = f.readlines()
        #sets position as the 
        self.position = len(self.deck)

    #deals one card
    def deal_card(self):
        self.position += 1
        #if deck runs out, the deck will reshuffle
        if self.position >= len(self.deck):
            shuffle(self.deck)
            self.position = 0
        return self.deck[self.position]

    #deals n amount of cards
    def deal_cards(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.deal_card())
        return cards

class Game:
    def __init__(self):
        self.black = Deck('black.txt')
        self.white = Deck('white.txt')
        self.judge_counter = 0
        self.players = []
        self.started = False

        self.cards_played = None

    def add_player(self, name, ws):
        self.players.append((name, ws))

        cards = self.black.deal_cards(7)
        message = {'type': 'join', 'hand': cards}
        ws.send(json.dumps(message))

        #if game has not started and amount of players >= 3 then start game
        if not self.started and len(self.players) == 3:
            self.start_game()

    def start_game(self):
        self.started = True
        self.start_round()

    def receive_message(self, name, ws, msg):
        #ignore until round starts
        if self.cards_played is not None:
            self.play_card(name, ws, msg)

    #chooses the player who gets to choose the card
    def choose_judge(self):
        if self.judge_counter == len(self.players):
            self.judge_counter = 0
        judge, _ = self.players[self.judge_counter]
        self.judge_counter += 1
        return judge 

    def start_round(self):
        self.cards_played = {}

        category_card = self.white.deal_card()
        player_judge = self.choose_judge()
        message = {'type': 'round_start',
                   'category': category_card,
                   'judge': player_judge}
        for name, ws in self.players:
            ws.send(json.dumps(message))

    def play_card(self, name, ws, card):
        self.cards_played[card] = name
        new_card = self.black.draw_card()
        message = {'type': 'draw', 'card': new_card}
        ws.send(json.dumps(message))

        #if amount of cards played are equal to the amount of players minus judge
        #start judging round
        if len(self.cards_played) == len(self.players) - 1:
            self.judge_round()

    def judge_round(self):
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
            if msg is None:
                break
            game.receive_message(name, ws, msg)

if __name__ == "__main__":
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
