from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game", methods=["POST", "GET"])
def new_game():
    """Start a new game and return JSON: {game_id, board}."""
    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.route("/api/score-word", methods=["POST"])
def score_word():
    # if not a word: {result: "not-word"}
    # if not on board: {result: "not-on-board"}
    # otherwise, {result: "ok"}
    game_id = request.json["gameId"]
    game = games[game_id]
    word = request.json["word"].upper()
    breakpoint()

    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})

    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})
