#!/usr/bin/env python3
# coding: utf-8

"""
4oBe4e Console Client

Usage:
  console_client.py <server_address> <player_name>
  console_client.py (-h | --help)
  console_client.py --version

Options:
  -h --help     Show this screen
  --version     Show version

"""
import console_view

from typing import Any, Dict, List, Tuple

from docopt import docopt  # type: ignore
from colorama import Back, Fore, Style  # type: ignore
import requests


def get_state(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"http://{server_address}/state")
    return req.json()


def get_players(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"http://{server_address}/players")
    return req.json()


def join_player(
    session: requests.sessions.Session, server_address: str, player_name: str
) -> Tuple:
    req = session.get(f"http://{server_address}/join/{player_name}")
    res = req.json()
    return (res["player_num"], res["player_token"])


def roll_dice(session: requests.sessions.Session, server_address: str) -> Dict:
    req = session.get(f"http://{server_address}/play/roll")
    return req.json()


def main():
    args = docopt(__doc__, version="4oBe4e Console Client v0.1")

    server_address = args["<server_address>"]
    player_name = args["<player_name>"]

    session = requests.Session()

    player = join_player(session, server_address, player_name)
    session.headers.update({"4oBe4e-user-token": player[1]})

    state = get_state(session, server_address)
    print(f"\nState: {state}")

    board = console_view.draw_board()
    print()
    for row in board:
        print("".join(row))


if __name__ == "__main__":
    main()
