#!/usr/bin/env python3
# coding: utf-8

"""
4oBe4e Console Client

Usage:
  console_client.py <server_address> <player_name> [--logger=<level>]
  console_client.py (-h | --help)
  console_client.py --version

Options:
  -h --help         Show this screen
  --version         Show version
  --logger=<level>  Log level [default: warning]

"""
import logging
from time import sleep
from typing import Any, Dict, List, Set, Tuple

from docopt import docopt  # type: ignore
from colorama import Back, Fore, Style  # type: ignore
import requests

from const import HOME_ZONE, END_PROGRESS, LAST_ON_PATH, PLAYER_COLOURS
from util import progress_to_position

# Players' board attributes
players: List[Dict[str, Any]] = [
    {
        "colour": PLAYER_COLOURS[0],
        "home": [[5, [2, 3]], [6, [2, 3]]],
        "target": [[7, [6, 7]], [8, [6, 7]]],
        "finish": [[9, [*range(3, 8)]], None],
    },
    {
        "colour": PLAYER_COLOURS[1],
        "home": [[2, [12, 13]], [3, [12, 13]]],
        "target": [[6, [10, 11]], [7, [10, 11]]],
        "finish": [[3, [9]], [4, [9]], [5, [9]], [6, [9]], [7, [9]]],
    },
    {
        "colour": PLAYER_COLOURS[2],
        "home": [[12, [15, 16]], [13, [15, 16]]],
        "target": [[10, [11, 12]], [11, [11, 12]]],
        "finish": [[9, [*range(11, 16)]], None],
    },
    {
        "colour": PLAYER_COLOURS[3],
        "home": [[15, [5, 6]], [16, [5, 6]]],
        "target": [[11, [7, 8]], [12, [7, 8]]],
        "finish": [[11, [9]], [12, [9]], [13, [9]], [14, [9]], [15, [9]]],
    },
]


def _colour(name: str = "WHITE") -> str:
    return eval(f"Fore.{name}")


def draw_board() -> List[List[Any]]:
    """ Draw an ASCII board with the current pieces.
    """

    ROWS = 19
    COLS = 19
    HOME_SHAPE = "[ ]"
    TARGET_SHAPE = "{ }"
    FOOTPATH_SHAPE = "( )"
    FINISH_SHAPE = " + "

    # Init board
    board = [[Style.RESET_ALL + "   "] * COLS for row in range(ROWS)]

    # Fill board frame
    for i in range(len(board)):
        board[i][:: len(board[i]) - 1] = [Fore.MAGENTA + " . ", Fore.MAGENTA + " . "]

    for i in 0, -1:
        board[i][:] = (Fore.CYAN + " . ") * len(board[i])

    # Fill player areas
    for p in players:
        for h in p["home"]:
            for c in h[1]:
                board[h[0]][c] = _colour(p["colour"]) + HOME_SHAPE
        for t in p["target"]:
            for c in t[1]:
                board[t[0]][c] = _colour(p["colour"]) + TARGET_SHAPE
        for f in p["finish"]:
            if f:
                for c in f[1]:
                    board[f[0]][c] = _colour(p["colour"]) + FINISH_SHAPE

    # Fill footpath
    footpath: List[List[List[int]]] = [
        [[2, 16], [8, 9, 10]],
        [[3, 4, 14, 15], [8, 10]],
        [[5, 13], [5, 6, 7, 8, 10, 11, 12, 13]],
        [[6, 7, 11, 12], [5, 13]],
        [[8, 10], [2, 3, 4, 5, 13, 14, 15, 16]],
        [[9], [2, 16]],
    ]

    for fp in footpath:
        for r in fp[0]:
            for c in fp[1]:
                board[r][c] = Fore.WHITE + FOOTPATH_SHAPE

    # Fill Trophies
    board[9][9] = ">|<"
    board[-1][-1] = Style.RESET_ALL + "🏳️‍🌈"

    return board


def redraw(pieces: List[Dict]) -> None:
    """The screen update function. Do not modify this for now."""

    board = draw_board()
    draw_pieces_on_board(board, pieces)

    print()
    for row in board:
        print("".join(row))


def _cant_overlap(piece_number: int, player_number: int, piece_progress=0) -> bool:
    """Even though this is piece-related logic, it has to do only with visualisation.
    Thus in view, rather than object logic"""
    return not (HOME_ZONE < piece_progress < END_PROGRESS)


def draw_pieces_on_board(board: List[List[Any]], pieces: List[Dict]) -> List[List[Any]]:
    """ It is not part of a job of this method to resolve game logic,
    such as collision of pieces of different players on the path"""
    for piece in pieces:
        (x, y) = put_piece_on_board(piece["number"], piece["player"], piece["progress"])
        player_progress = [
            p["progress"] for p in pieces if p["player"] == piece["player"]
        ]
        count = player_progress.count(piece["progress"])
        val = (
            str(piece["number"])
            if _cant_overlap(piece["number"], piece["player"], piece["progress"])
            or count == 1
            else str(count)
        )
        board[x][y] = f"{_colour(players[piece['player']]['colour'])}.{val}."

    return board


def put_piece_on_board(
    piece_number: int, player_number: int, piece_progress=0
) -> Tuple[int, int]:
    """Currently player is in [1..4], piece is in [0..3]. Do we need to change this?
    TODO: Refactor to implement startegy pattern
    """
    coords = (0, 0)
    progress = piece_progress
    if progress == 0:
        coords = __coord_in_home(piece_number, player_number, piece_progress)
    elif 0 < progress <= LAST_ON_PATH:
        coords = __coord_on_path(piece_number, player_number, piece_progress)
    elif LAST_ON_PATH < progress < END_PROGRESS:
        coords = __coord_on_finish(piece_number, player_number, piece_progress)
    elif progress == END_PROGRESS:
        coords = __coord_in_target(piece_number, player_number, piece_progress)
    else:
        raise NotImplementedError()

    return coords


def get_state(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"{server_address}/state")
    return req.json()


def get_players(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"{server_address}/players")
    return req.json()


def join_player(
    session: requests.sessions.Session, server_address: str, player_name: str
) -> Tuple:
    req = session.get(f"{server_address}/join/{player_name}")
    res = req.json()
    return (res["player_num"], res["player_token"])


def roll_dice(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"{server_address}/play/roll")
    return req.json()


def move_piece(
    session: requests.sessions.Session,
    server_address: str,
    piece_number: int,
    dice: int,
) -> Dict:
    req = session.get(f"{server_address}/play/move/{piece_number}/{dice}")
    return req.json()


def put_piece(
    session: requests.sessions.Session,
    server_address: str,
    piece_number: int,
    dice: int,
) -> Dict:
    req = session.get(f"{server_address}/play/out/{piece_number}/{dice}")
    return req.json()


def __coord_in_home(
    piece_number: int, player_number: int, piece_progress=0
) -> Tuple[int, int]:
    """Draw in home positions: each piece has its location. Progress is always same, thus irrelevant
    
    >>> __coord_in_home(0, 0)
    (5, 2)

    >>> __coord_in_home(1, 1)
    (2, 13)

    >>> __coord_in_home(2, 2)
    (13, 15)

    >>> __coord_in_home(3, 3)
    (16, 6)
    """
    assert piece_progress == 0

    zones = [(5, 2), (2, 12), (12, 15), (15, 5)]
    shift = [(0, 0), (0, 1), (1, 0), (1, 1)]

    return (
        zones[player_number][0] + shift[piece_number][0],
        zones[player_number][1] + shift[piece_number][1],
    )


def __coord_on_path(
    piece_number: int, player_number: int, piece_progress=0
) -> Tuple[int, int]:
    """Draws on path: if two or more pieces on same cell, instead of number,
    draws a placeholder, which does not need to show piece number
    Logic split this in 4 different cases, determined by player offset.
    Parameter piece does't influence logic.

    Player Progress to Position conversion:
        P0     1..56: (pos)
        P1     1..42: (p_num * shift + pos)
              43..56: (p_num * shift + pos) % end_progress
        P2     1..28: (p_num * shift + pos)
              29..56: (p_num * shift + pos) % end_progress
        P3     1..14: (p_num * shift + pos)
              15..56: (p_num * shift + pos) % end_progress


    Test player 1:
    >>> __coord_on_path(player_number=0, piece_number=1, piece_progress=1)
    (8, 2)

    Test player 2:
    >>> __coord_on_path(player_number=1, piece_number=1, piece_progress=1)
    (2, 10)

    Test player 3:
    >>> __coord_on_path(player_number=2, piece_number=1, piece_progress=1)
    (10, 16)

    Test player 4:
    >>> __coord_on_path(player_number=3, piece_number=1, piece_progress=1)
    (16, 8)

    Test path wrap:
    >>> __coord_on_path(player_number=3, piece_number=1, piece_progress=56)
    (16, 9)

    Test overlap:
    >>> __coord_on_path(player_number=1, piece_number=1, piece_progress=17)
    (10, 14)
    """

    assert 1 <= piece_progress <= LAST_ON_PATH and 0 <= player_number <= 3

    POSITION_TO_ROWCOL: Tuple[Tuple[int, int], ...] = (
        (0, 0),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (7, 5),
        (6, 5),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (4, 8),
        (3, 8),
        (2, 8),
        (2, 9),
        (2, 10),
        (3, 10),
        (4, 10),
        (5, 10),
        (5, 11),
        (5, 12),
        (5, 13),
        (6, 13),
        (7, 13),
        (8, 13),
        (8, 14),
        (8, 15),
        (8, 16),
        (9, 16),
        (10, 16),
        (10, 15),
        (10, 14),
        (10, 13),
        (11, 13),
        (12, 13),
        (13, 13),
        (13, 12),
        (13, 11),
        (13, 10),
        (14, 10),
        (15, 10),
        (16, 10),
        (16, 9),
        (16, 8),
        (15, 8),
        (14, 8),
        (13, 8),
        (13, 7),
        (13, 6),
        (13, 5),
        (12, 5),
        (11, 5),
        (10, 5),
        (10, 4),
        (10, 3),
        (10, 2),
        (9, 2),
    )

    return POSITION_TO_ROWCOL[progress_to_position(player_number, piece_progress)]


def __coord_on_finish(
    piece_number: int, player_number: int, piece_progress=0
) -> Tuple[int, int]:
    """Piece number is irrelevant
    
    >>> __coord_on_finish(1, 0, 57)
    (9, 3)

    >>> __coord_on_finish(1, 0, 61)
    (9, 7)
    
    >>> __coord_on_finish(1, 1, 57)
    (3, 9)

    >>> __coord_on_finish(1, 2, 58)
    (9, 14)

    >>> __coord_on_finish(1, 3, 59)
    (13, 9)

    >>> __coord_on_finish(1, 3, 61)
    (11, 9)
    """
    pos = piece_progress - LAST_ON_PATH
    assert 0 < pos < 6

    player = player_number
    (x, y) = (0, 0)

    if player in [0, 2]:
        x = 9
        y = pos + 2 if player == 0 else 15 - (pos - 1)
    elif player in [1, 3]:
        x = pos + 2 if player == 1 else 15 - (pos - 1)
        y = 9
    else:
        raise NotImplementedError()

    return (x, y)


def __coord_in_target(
    piece_number: int, player_number: int, piece_progress=0
) -> Tuple[int, int]:
    """Draw in target positions: each piece has its location.
    Progress is always same, thus irrelevant
    
    >>> __coord_in_target(0, 0, 62)
    (7, 6)

    >>> __coord_in_target(1, 1, 62)
    (6, 11)

    >>> __coord_in_target(2, 2, 62)
    (11, 11)

    >>> __coord_in_target(3, 3, 62)
    (12, 8)
    """
    assert piece_progress == 62

    zones = [(7, 6), (6, 10), (10, 11), (11, 7)]
    shift = [(0, 0), (0, 1), (1, 0), (1, 1)]

    return (
        zones[player_number][0] + shift[piece_number][0],
        zones[player_number][1] + shift[piece_number][1],
    )


def main():
    """Main loop."""

    # Parse args
    args = docopt(__doc__, version="4oBe4e Console Client v0.1")

    server_address = args["<server_address>"]
    player_name = args["<player_name>"]
    log_level = args["--logger"]

    # Configure logger
    logging.basicConfig(level=log_level.upper(), format="%(levelname)s: %(message)s")
    log = logging.getLogger(__name__)

    # Init a Requests session
    session = requests.Session()

    # Join game
    player_number, player_token = join_player(session, server_address, player_name)
    session.headers.update({"4oBe4e-user-token": player_token})

    # Changes on state update
    state_serial = -1
    while True:
        log.debug(">>> Polling state")
        state = get_state(session, server_address)
        log.debug(state)
        if "error" in state:
            log.error(f">>> No valid game found ({state['error']})")
        else:
            # TODO:
            # check if_winner
            if state["number"] != state_serial:
                state_serial = state["number"]
                redraw(state["board"]["pieces"])
                if state["current_player"] == player_number:
                    log.debug(f">>> In turn")
                    if state["valid_actions"][0]["move_type"] == 1:
                        input(f"Press ENTER to roll dice")
                        dice = roll_dice(session, server_address)["dice"]
                        print(f">>> Rolled {dice}")
                        continue
                    else:
                        dice = state["dice"]
                        actions = {}
                        for action in state["valid_actions"]:
                            actions[action["piece"]] = action["move_type"]
                        log.debug(actions)
                        piece = int(
                            input(
                                f">>> Rolled {dice}, choose a piece {[piece for piece in actions.keys()]}: "
                            )
                        )
                        if actions[piece] == 2:
                            move_piece(session, server_address, piece, dice)
                        if actions[piece] == 3:
                            put_piece(session, server_address, piece, dice)
                        continue
                else:
                    log.debug(
                        f">>> Not in turn (player: {player_number} | player_in_turn: {state['current_player']})"
                    )
            else:
                log.debug(">>> No state change")

        # Pause before polling for state changes
        log.debug(">>> Sleeping")
        sleep(1)

    # DEBUG import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
