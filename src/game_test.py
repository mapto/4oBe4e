#!/usr/bin/env python3
# coding: utf-8

from player import Player
from piece import Piece

from game import do_move, is_valid_move

Player.create()
Player.create()


def test_do_move_take_out_of_home():
    p1 = Player.get(1)
    piece = Piece(0, 0, 15)
    status = [piece, Piece(1, 0, 0)]

    assert is_valid_move(piece, 6, status)

    success = do_move(status, p1, 0, 6)

    assert success
    assert status[0].progress() == 0
    assert status[1].progress() == 1


def test_do_move_cant_out_of_home():
    p1 = Player.get(1)
    piece = Piece(1, 0, 0)
    status = [piece]

    assert not is_valid_move(piece, 5, status)

    success = do_move(status, p1, 0, 5)

    assert not success
    assert status[0].progress() == 0


def test_do_move_blocked_out_of_home():
    p1 = Player.get(1)
    piece = Piece(1, 0, 0)
    status = [piece, Piece(0, 0, 15), Piece(0, 1, 15)]

    assert not is_valid_move(piece, 6, status)

    success = do_move(status, p1, 0, 6)

    assert not success
    assert status[0].progress() == 0


def test_do_move_on_path():
    p1 = Player.get(1)
    piece = Piece(0, 0, 16)
    status = [piece, Piece(1, 0, 1)]

    assert is_valid_move(piece, 1, status)

    success = do_move(status, p1, 0, 1)

    assert success
    assert status[0].progress() == 0
    assert status[1].progress() == 2


def test_do_move_on_target():
    p0 = Player.get(0)
    status = [Piece(0, 0, 56), Piece(1, 0, 33)]

    success = do_move(status, p0, 0, 1)

    assert success
    assert status[0].progress() == 57
    assert status[1].progress() == 33


def test_do_move_on_finish():
    p0 = Player.get(0)
    status = [Piece(0, 0, 56)]

    success = do_move(status, p0, 0, 6)

    assert success
    assert status[0].progress() == 62


def test_do_move_cant_finish():
    p0 = Player.get(0)
    status = [Piece(0, 0, 58)]

    success = do_move(status, p0, 0, 6)

    assert not success
    assert status[0].progress() == 58
