def test_draw_board():
    """ Test against a base64 representation of the ASCII board. """

    from main import draw_board
    from hashlib import md5

    board_md5 = "e0126f60aff057284b112d0e19286dc0"

    board = str(draw_board()).encode("utf-8")

    assert md5(board).hexdigest() == board_md5
