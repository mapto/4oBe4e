#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import request, redirect, send_from_directory
import dataclasses, json
import uuid
from state import Board, GameState, MovePiece, PieceOut, RollDice
from engine import GameEngine
from flask import jsonify
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
        return player_name_token[player]
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
    return player_uuid


@app.route("/players")
def players():
    return dict(
        [name, player_token_number[token]] for name, token in player_name_token.items()
    )


def __get_player_number() -> int:
    user_token = request.headers.get("4oBe4e-user-token")
    if user_token is None:
        raise ValueError("There is no user token in the 4oBe4e-user-token header")
    user_id = player_token_number[user_token]
    if user_id is None:
        raise ValueError("Unknown user with token:" + user_token)
    return user_id


def __state_to_json(state: GameState) -> str:
    return json.dumps(dataclasses.asdict(state))


@app.route("/state")
def get_state():
    if engine == None:
        raise SystemError("there is still no game")
    return __state_to_json(engine.state)


@app.route("/play/roll")
def play_roll():
    player = __get_player_number()
    new_state = engine.play(RollDice(player))
    return __state_to_json(new_state)


@app.route("/play/move/<piece>/<dice>")
def play_move(piece: int, dice: int):
    player = __get_player_number()
    piece_obj = (
        engine.state.board.pieces
    )  # TODO select the correct peice based on piece num and player num
    new_state = engine.play(MovePiece(player, piece_obj, dice))
    return __state_to_json(new_state)


@app.route("/play/out/<piece>/<dice>")
def play_out(piece: int, dice: int):
    player = __get_player_number()
    piece_obj = engine.state.board.pieces
    new_state = engine.play(PieceOut(player, piece_obj, dice))
    return __state_to_json(new_state)


if __name__ == "__main__":
    app.run(debug=True)
