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
    player1_token = players1["player_token"]
    # Then we expect to recieve it's token
    assert isinstance(player1_token, str)

    # When we join player1 again
    rv = client.get("/join/player1")
    players1_second = json.loads(rv.data)
    player1_token_second = players1_second["player_token"]

    # Then we expect to receive the same token as from first join
    assert player1_token_second == player1_token

    # When we join 4 players
    rv = client.get("/join/player2")
    players2 = json.loads(rv.data)
    player2_token = players2["player_token"]
    assert isinstance(player2_token, str)

    rv = client.get("/join/player3")
    players3 = json.loads(rv.data)
    player3_token = players3["player_token"]
    assert isinstance(player3_token, str)

    rv = client.get("/join/player4")
    players4 = json.loads(rv.data)
    player4_token = players4["player_token"]
    assert isinstance(player4_token, str)

    # Then we expect their numbers returned
    rv = client.get("/players")
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
    assert rv.status_code == 400
    assert error == {"error": "There is no user token in the 4oBe4e-user-token header"}

    # Then we expect response code 400

    # And an error message


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
