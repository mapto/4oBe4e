#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import request, Response, redirect, send_from_directory
import dataclasses, json
import uuid
from state import Board, GameState, GameMove
from engine import GameEngine
from typing import Dict

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
    global engine
    if player in player_name_token:
        return json.dumps({"player_token": player_name_token[player]})
    if len(player_token_name) == 4:
        players: Dict[str, int] = dict(
            (name, player_token_number[token])
            for name, token in player_name_token.items()
        )
        raise ValueError("Game is full. Players are ", players)
    player_uuid: str = uuid.uuid4().__str__()
    player_token_name[player_uuid] = player
    player_number: int = len(player_token_number)
    player_name_token[player] = player_uuid
    player_token_number[player_uuid] = player_number
    if len(player_token_name) == 4:
        board = Board.create(list(player_token_number.values()))
        engine = GameEngine(board)
    return json.dumps({"player_token": player_uuid})


@app.route("/players")
def players():
    return dict(
        [name, player_token_number[token]] for name, token in player_name_token.items()
    )


def __get_player_number() -> int:
    try:
        user_token = request.headers.get("4oBe4e-user-token")
        if user_token is None:
            raise ValueError("There is no user token in the 4oBe4e-user-token header")
        user_id = player_token_number[user_token]
        if user_id is None:
            raise ValueError("Unknown user with token:" + user_token)
    except KeyError:
        raise ValueError("There is no user token in the 4oBe4e-user-token header")
    return user_id


def __error_response(err: str) -> Response:
    return Response(json.dumps({"error": err}), status=400, mimetype="application/json")


def __state_to_json(state: GameState) -> str:
    return json.dumps(dataclasses.asdict(state))


@app.route("/state")
def get_state():
    if engine == None:
        return Response(
            json.dumps(
                {
                    "error": "There is no game started yet because there is no 4 players",
                    "players": players(),
                }
            ),
            status=400,
            mimetype="application/json",
        )
    return __state_to_json(engine.state)


@app.route("/play/roll")
def play_roll():
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.args[0]))
    else:
        new_state = engine.play(GameMove.roll_dice(player))
        return __state_to_json(new_state)


@app.route("/play/move/<piece>/<dice>")
def play_move(piece: int, dice: int):
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.args[0]))
    else:
        new_state = engine.play(GameMove.move_piece(player, piece, dice))
        return __state_to_json(new_state)


@app.route("/play/out/<piece>/<dice>")
def play_out(piece: int, dice: int):
    try:
        player = __get_player_number()
    except ValueError as ve:
        return __error_response(str(ve.__str__))
    else:
        new_state = engine.play(GameMove.piece_out(player, piece, dice))
        return __state_to_json(new_state)


if __name__ == "__main__":
    app.run(debug=True)
