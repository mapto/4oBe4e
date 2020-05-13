#!/usr/bin/env python3
# coding: utf-8

"""
Manual test:
curl localhost:5000/join/veso
curl localhost:5000/join/ilian
curl localhost:5000/join/lucho
curl localhost:5000/join/marto

curl localhost:5000/players

curl localhost:5000/state

curl -H 'user-token:<user-token>' localhost:5000/play/roll

"""

from fastapi import FastAPI
from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

import dataclasses, json
import uuid

from settings import host, port

from state import Board, GameState, GameMove
from engine import GameEngine
from typing import Dict, Any

static_path = "."

app = FastAPI()

player_token_name: Dict[str, str] = {}
player_token_number: Dict[str, int] = {}
player_number_token: Dict[int, str] = {}
player_name_token: Dict[str, str] = {}
engine: GameEngine


@app.get("/join/<player>")
async def join(player: str) -> JSONResponse:
    global engine  # TODO Where shall we keep the curren running GameEngine/s ?
    if player in player_name_token:
        token = player_name_token[player]
        num = player_token_number[token]
        return JSONResponse(content={"player_token": token, "player_num": num})
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
    return JSONResponse(
        content={"player_token": player_uuid, "player_num": player_number}
    )


@app.get("/players")
async def players():
    return dict(
        [name, player_token_number[token]] for name, token in player_name_token.items()
    )


def __get_player_number(*, user_token: str = Header(None)) -> int:
    try:
        missing_token_message = "There is no user token in the user-token header"
        if user_token is None:
            raise ValueError(missing_token_message)
        user_id = player_token_number[user_token]
        if user_id is None:
            raise ValueError("Unknown user with token:" + user_token)
    except KeyError:
        raise ValueError(missing_token_message)
    return user_id


@app.get("/state")
async def get_state():
    try:
        return JSONResponse(content=engine.state)
    except NameError:
        players = {
            name: player_token_number[token]
            for name, token in player_name_token.items()
        }
        raise HTTPException(
            status_code=400,
            detail={
                "error": "There is no game started yet because there is no 4 players",
                "players": players,
            },
        )


@app.get("/play/roll")
async def play_roll():
    try:
        engine.state
    except:
        players = {
            name: player_token_number[token]
            for name, token in player_name_token.items()
        }
        raise HTTPException(
            status_code=400,
            detail={
                "error": "There is no game started yet because there is no 4 players",
                "players": players,
            },
        )

    try:
        player = __get_player_number()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=ve.args[0])
    else:
        new_state = engine.play(GameMove.roll_dice(player))
        return JSONResponse(content=new_state)


# We pass the dice here to vrify the client had made a choice based on
# the current server state.
# TODO: shall we pass the state number for the same reason?
@app.get("/play/move/<piece>/<dice>")
async def play_move(piece: int, dice: int):
    try:
        engine.state
    except:
        players = {
            name: player_token_number[token]
            for name, token in player_name_token.items()
        }
        raise HTTPException(
            status_code=400,
            detail={
                "error": "There is no game started yet because there is no 4 players",
                "players": players,
            },
        )
    try:
        player = __get_player_number()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=ve.args[0])
    else:
        new_state = engine.play(GameMove.move_piece(player, piece, dice))
        return JSONResponse(content=new_state)


# We pass the dice here to vrify the client had made a choice based on
# the current server state.
# TODO: shall we pass the state number for the same reason?
@app.get("/play/out/<piece>/<dice>")
async def play_out(piece: int, dice: int):
    try:
        engine.state
    except:
        players = {
            name: player_token_number[token]
            for name, token in player_name_token.items()
        }
        raise HTTPException(
            status_code=400,
            detail={
                "error": "There is no game started yet because there is no 4 players",
                "players": players,
            },
        )
    try:
        player = __get_player_number()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=ve.args[0])
    else:
        new_state = engine.play(GameMove.piece_out(player, piece, dice))
        return JSONResponse(content=new_state)


if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run(app, host=host, port=port, debug=True)
