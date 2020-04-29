#!/usr/bin/env python3
# coding: utf-8

import pytest  # type: ignore

from web_server import app
import dataclasses, json
from state import GameState, Board, GameMove, ROLL_DICE
from engine import GameEngine, Dice


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


player1_token: str = ""
player2_token: str = ""
player3_token: str = ""
player4_token: str = ""


def test_roll_no_game(monkeypatch, client):
    # Given the game hasn't started yet
    # When we try to roll befor the game has begun (4 players joined)
    rv = client.get("/play/roll")
    error = json.loads(rv.data)
    # Then we expect response code 400
    assert rv.status_code == 400
    # And an error message
    assert json.dumps(error) == json.dumps(
        {
            "error": "There is no game started yet because there is no 4 players",
            "players": {},
        }
    )


def test_play_move_piece_no_game(monkeypatch, client):
    # Given the game hasn't started yet
    # When we try to move a piece befor the game has begun (4 players joined)
    rv = client.get("/play/move/0/2")
    error = json.loads(rv.data)
    # Then we expect response code 400
    assert rv.status_code == 400
    # And an error message
    assert json.dumps(error) == json.dumps(
        {
            "error": "There is no game started yet because there is no 4 players",
            "players": {},
        }
    )


def test_play_piece_out_no_game(monkeypatch, client):
    # Given the game hasn't started yet
    # When we try to move a piece out befor the game has begun (4 players joined)
    rv = client.get("/play/out/0/6")
    error = json.loads(rv.data)
    # Then we expect response code 400
    assert rv.status_code == 400
    # And an error message
    assert json.dumps(error) == json.dumps(
        {
            "error": "There is no game started yet because there is no 4 players",
            "players": {},
        }
    )


def test_join(monkeypatch, client):
    # Given
    global player1_token
    global player2_token
    global player3_token
    global player4_token

    # When we call /players
    rv = client.get("/players")
    # Then we expect no players in the begining
    assert b"{}" in rv.data

    # When we join player1
    rv = client.get("/join/player1")
    players1 = json.loads(rv.data)
    assert rv.headers["content-type"].lower() == "application/json"
    # Then we expect to recieve it's token
    player1_token = players1["player_token"]
    assert isinstance(player1_token, str)
    # And to recieve it's number
    assert players1["player_num"] == 0

    # When we ask for state before the game has begun (4 players joined)
    rv = client.get("/state")
    error = json.loads(rv.data)
    # Then we expect response code 400
    assert rv.status_code == 400
    assert rv.headers["content-type"].lower() == "application/json"
    # And an error message
    assert json.dumps(error) == json.dumps(
        {
            "error": "There is no game started yet because there is no 4 players",
            "players": {"player1": 0},
        }
    )

    # When we join player1 again
    rv = client.get("/join/player1")
    players1_second = json.loads(rv.data)
    player1_token_second = players1_second["player_token"]
    # And to recieve it's number
    assert players1_second["player_num"] == 0

    # Then we expect to receive the same token as from first join
    assert player1_token_second == player1_token

    # When we join 4 players
    rv = client.get("/join/player2")
    players2 = json.loads(rv.data)
    player2_token = players2["player_token"]
    assert isinstance(player2_token, str)
    assert players2["player_num"] == 1

    rv = client.get("/join/player3")
    players3 = json.loads(rv.data)
    player3_token = players3["player_token"]
    assert isinstance(player3_token, str)
    assert players3["player_num"] == 2

    rv = client.get("/join/player4")
    players4 = json.loads(rv.data)
    player4_token = players4["player_token"]
    assert isinstance(player4_token, str)
    assert players4["player_num"] == 3

    # Then we expect their numbers returned
    rv = client.get("/players")
    assert rv.headers["content-type"].lower() == "application/json"
    players = json.loads(rv.data)
    assert players == {
        "player1": 0,
        "player2": 1,
        "player3": 2,
        "player4": 3,
    }

    assert player1_token_second == player1_token


def test_state(monkeypatch, client):
    # Given we have joined 4 players in the previous test

    # When we call /state
    rv = client.get("/state")
    game_state = json.loads(rv.data)

    board = Board.create(players=[0, 1, 2, 3])
    state = GameState.create(board)

    # Then we want the same state as the default for 4 players
    assert game_state == dataclasses.asdict(state)


def test_roll_no_user_token(monkeypatch, client):
    # Given 4 players had joined in the previous tests and the game had starte

    # When we try to play with incorrect user token
    rv = client.get("/play/roll", headers={"4oBe4e-user-token": "wrong-token"})
    error = json.loads(rv.data)

    # Then we expect response code 400
    assert rv.status_code == 400

    # And expect content type application/json
    assert rv.headers["content-type"].lower() == "application/json"

    # And an error message
    assert error == {"error": "There is no user token in the 4oBe4e-user-token header"}


def test_roll(monkeypatch, client):
    # Given 4 players had joined in the previous tests and the game had starte

    # When we try to play with the correct user token
    rv = client.get("/play/roll", headers={"4oBe4e-user-token": player1_token})
    game_state = json.loads(rv.data)

    board = Board.create(players=[0, 1, 2, 3])
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: game_state["dice"])
    game = GameEngine(board, dice)
    game.play(GameMove.roll_dice(player=0))

    # Then we want the same state as the default for 4 players
    assert game_state == dataclasses.asdict(game.get_state())
