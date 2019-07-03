import pytest

from mancala.game.play import GameState
import numpy as np

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


def test_get_state(game):
    expected_state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    assert game.board_state == expected_state

    # check the state after a move
    game.try_move(game.players[0], 1)
    expected_state = [4, 0, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 0]
    assert game.board_state == expected_state

    # check the state after a move
    game.try_move(game.players[1], 9)
    expected_state = [4, 0, 5, 5, 5, 5, 0, 4, 4, 0, 5, 5, 5, 1]
    assert game.board_state == expected_state

# TODO add test for if game is done


def test_game_state(game):
    assert game.game_stack == [GameState(BoardState=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=np.nan,
                                         player=np.nan,
                                         score_p0=0,
                                         score_p1=0)
                               ]

    # check the stack after a move
    game.players[0].make_move(2)
    assert game.game_stack == [GameState(BoardState=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=np.nan,
                                         player=np.nan,
                                         score_p0=0,
                                         score_p1=0),
                               GameState(BoardState=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=2,
                                         player=0,
                                         score_p0=0,
                                         score_p1=0),
                               ]

    # check the stack after another move
    game.try_move(game.players[1], 9)
    assert game.game_stack == [GameState(BoardState=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=np.nan,
                                         player=np.nan,
                                         score_p0=0,
                                         score_p1=0),
                               GameState(BoardState=[4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=2,
                                         player=0,
                                         score_p0=0,
                                         score_p1=0),
                               GameState(BoardState=[4, 0, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 0],
                                         action=3,
                                         player=1,
                                         score_p0=0,
                                         score_p1=1)
                               ]


def test_dataframe_rounds(game):
    game.try_move(game.players[0], 0)
    game.try_move(game.players[1], 7)
    game.try_move(game.players[0], 1)

    assert list(game.create_dataframe_game_stack()['round']) == [0, 1, 1, 2]
