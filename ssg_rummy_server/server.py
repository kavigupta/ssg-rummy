from collections import defaultdict
import json
import uuid

from flask import Flask, render_template, request, redirect
from flask_sock import Sock, ConnectionClosed
from permacache.locked_shelf import LockedShelf

from .game_state import GameState

app = Flask(__name__)
sock = Sock(app)


def database():
    return LockedShelf("data/shelf", multiprocess_safe=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game")
def game():
    return render_template("game.html")


@app.route("/create_game", methods=["POST"])
def create_game():
    names = request.form["names"].split(",")
    game_id = str(uuid.uuid4())
    with database() as db:
        db[game_id] = GameState.create(names)
    # TODO escape things properly
    # TODO intermediate landing page
    return redirect(f"/game?user={names[0]}&game_id={game_id}", code=302)


open_sockets = defaultdict(list)


@sock.route("/update_game_state")
def update_game_state(ws):
    print("Websocket opened", ws, flush=True)
    added_to_queue = False
    while True:
        data = json.loads(ws.receive())
        print("received data", data, "on websocket", ws)
        game_id = data["game_id"]
        # TODO handle game doesn't exist error
        user = data["user"]

        if not added_to_queue:
            open_sockets[game_id].append((user, ws))
            added_to_queue = True
            print("Added", ws, " to open sockets queue, with game id", game_id)

        command = data["command"]
        with database() as db:
            game_state = db[game_id]
            game_state.act(user, command)
            db[game_id] = game_state
            print("Game state updated to", flush=True)
            print(game_state, flush=True)
            for socket_user, to_update in open_sockets[game_id][:]:
                print("Attempting to update", to_update, flush=True)
                try:
                    to_update.send(game_state.summary(socket_user))
                except ConnectionClosed:
                    print("ERROR: Connection closed", flush=True)
                    open_sockets[game_id].remove((socket_user, to_update))
                    print("Removed")


app.debug = True
