from collections import defaultdict
import json

from flask import Flask, render_template
from flask_sock import Sock, ConnectionClosed
from permacache.locked_shelf import LockedShelf

from .game_state import GameState

app = Flask(__name__)
sock = Sock(app)

def database():
    return LockedShelf("data/shelf", multiprocess_safe=True)


@app.route("/game")
def game():
    import os

    print(os.getcwd(), flush=True)
    return render_template("game.html")

open_sockets = defaultdict(list)

@sock.route("/echo")
def echo(ws):
    print("Websocket opened", ws, flush=True)
    added_to_queue = False
    while True:
        data = json.loads(ws.receive())
        print("received data", data, "on websocket", ws)
        game_id = data["game_id"]
        user = data["user"]
        
        if not added_to_queue:
            open_sockets[game_id].append(ws)
            added_to_queue = True
            print("Added", ws, " to open sockets queue, with game id", game_id)

        command = data["command"]
        with database() as db:
            if game_id not in db:
                game_state = GameState.create()
            else:
                game_state = db[game_id]
            user_visible_state = game_state.act(user, command)
            db[game_id] = game_state
            for to_update in open_sockets[game_id][:]:
                print("Attempting to update", to_update, flush=True)
                try:
                    to_update.send(user_visible_state)
                except ConnectionClosed:
                    print("ERROR: Connection closed", flush=True)
                    open_sockets[game_id].remove(to_update)
                    print("Removed")

app.debug = True
