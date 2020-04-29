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
from time import sleep
from typing import Any, Dict, List, Tuple

from docopt import docopt  # type: ignore
import requests
import logging

logging.basicConfig(format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


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

    player_number, player_token = join_player(session, server_address, player_name)
    session.headers.update({"4oBe4e-user-token": player_token})

    # Changes on state update
    state_serial = -1
    while True:
        state = get_state(session, server_address)
        if "error" in state:
            log.error(f"No valid game found ({state['error']})")
        else:
            # TODO:
            # draw the board
            # check if_winner
            if state["number"] != state_serial:
                state_serial = state["number"]
                if state["current_player"] == player_number:
                    # TODO:
                    # roll the dice
                    # make a move
                    log.debug("In turn")
                else:
                    log.debug(
                        f"Not in turn (player: {player_number} | player_in_turn: {state['current_player']})"
                    )
            else:
                log.debug("No change in state")

        # Pause before polling for state changes
        sleep(5)
        log.debug("Polling state")

    # DEBUG import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
