from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import sqlite3
import time
import json

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
	return app.send_static_file('index.html')


@app.route("/ws")
def cards():
	if request.environ.get('wsgi.websocket'):
		ws = request.environ['wsgi.websocket']
		cards = ["Kyle", "Amy", "Brandon", "Andrew", "Cards"]
		message = {'type': 'join', 'hand': cards}
		ws.send(json.dumps(message))



if __name__ == "__main__":
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()