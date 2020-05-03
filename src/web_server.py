#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import request, Response, redirect, send_from_directory
import dataclasses, json
import uuid
from state import Board, GameState, GameMove
from engine import GameEngine
from typing import Dict
from flask.json import jsonify

static_path = "."

app = Flask(__name__, static_url_path="/.")

player_token_name: Dict[str, str] = {}
player_token_number: Dict[str, int] = {}
player_number_token: Dict[int, str] = {}
player_name_token: Dict[str, str] = {}
engine: GameEngine

doc = """
Manual test:
curl localhost:5000/join/veso
curl localhost:5000/join/ilian
curl localhost:5000/join/lucho
curl localhost:5000/join/marto

curl localhost:5000/players

curl localhost:5000/state

curl -H '4oBe4e-user-token:<user-token>' localhost:5000/play/roll

"""


@app.route("/join/<player>")
def join(player: str):
    global engine  # TODO Where shall we keep the curren running GameEngine/s ?
    if player in player_name_token:
        token = player_name_token[player]
        num = player_token_number[token]
        return jsonify({"player_token": token, "player_num": num})
    if len(player_token_name) == 4:
        players: Dict[str, int] = dict(
            (name, player_token_number[token])
            for name, token in player_name_token.items()
        )
        raise ValueError("Game is full. Players are ", players)
    player_uuid: str = str(uuid.uuid4())
    player_token_name[player_uuid] = player
    player_number: int = len(player_token_number)
    player_name_token[player] = player_uuid
    player_token_number[player_uuid] = player_number
    if len(player_token_name) == 4:
        board = Board.create(list(player_token_number.values()))
        engine = GameEngine(board)
    return jsonify({"player_token": player_uuid, "player_num": player_number})


@app.route("/players")
def players():
    return dict(
        [name, player_token_number[token]] for name, token in player_name_token.items()
    )


def __get_player_number() -> int:
    try:
        user_token = request.headers.get("4oBe4e-user-token")
        missing_token_message = "There is no user token in the 4oBe4e-user-token header"
        if user_token is None:
            raise ValueError(missing_token_message)
        user_id = player_token_number[user_token]
        if user_id is None:
            raise ValueError("Unknown user with token:" + user_token)
    except KeyError:
        raise ValueError(missing_token_message)
    return user_id


def __error_response(err: str) -> Response:
    return __error_response__(json.dumps({"error": err}))


def __error_response__(err: str) -> Response:
    return Response(err, status=400, mimetype="application/json")


def __no_game_response() -> Response:
    return __error_response__(
        json.dumps(
            {
                "error": "There is no game started yet because there is no 4 players",
                "players": players(),
            }
        )
    )


def __state_to_json(state: GameState) -> Response:
    return jsonify(dataclasses.asdict(state))


@app.route("/state")
def get_state():
    try:
        return __state_to_json(engine.state)
    except NameError:
        return __no_game_response()


@app.route("/play/roll")
def play_roll():
    try:
        engine.state
    except:
        return __no_game_response()
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.args[0]))
    else:
        new_state = engine.play(GameMove.roll_dice(player))
        return __state_to_json(new_state)


# We pass the dice here to vrify the client had made a choice based on
# the current server state.
# TODO: shall we pass the state number for the same reason?
@app.route("/play/move/<piece>/<dice>")
def play_move(piece: int, dice: int):
    piece = int(piece)
    dice = int(dice)
    try:
        engine.state
    except:
        return __no_game_response()
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.args[0]))
    else:
        new_state = engine.play(GameMove.move_piece(player, piece, dice))
        return __state_to_json(new_state)


# We pass the dice here to vrify the client had made a choice based on
# the current server state.
# TODO: shall we pass the state number for the same reason?
@app.route("/play/out/<piece>/<dice>")
def play_out(piece: int, dice: int):
    piece = int(piece)
    dice = int(dice)
    try:
        engine.state
    except:
        return __no_game_response()
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.__str__))
    else:
        new_state = engine.play(GameMove.piece_out(player, piece, dice))
        return __state_to_json(new_state)


if __name__ == "__main__":
    app.run(debug=True)
