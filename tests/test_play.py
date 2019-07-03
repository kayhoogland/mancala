import pytest


def test_update_possible_moves(game):
    game.try_move(game.players[0], 1)
    expected_1 = {0: (1, 3, 4, 5, 6), 1: (1, 2, 3, 4, 5, 6)}
    assert game.possible_moves == expected_1

    game.try_move(game.players[1], 8)
    expected_2 = {0: (1, 3, 4, 5, 6), 1: (1, 3, 4, 5, 6)}
    assert game.possible_moves == expected_2

    # Should result in opening up all the moves for Player two
    game.try_move(game.players[0], 3)
    expected_3 = {0: (1, 3, 5, 6), 1: (1, 2, 3, 4, 5, 6)}
    assert game.possible_moves == expected_3

