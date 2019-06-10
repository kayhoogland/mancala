import pytest


@pytest.mark.parametrize(
    "attribute", ["name", "current_game", "number", "holes", "point_hole", "skip_hole"]
)
def test_attributes_player(attribute, players):
    assert hasattr(players, attribute)


@pytest.mark.parametrize(
    "hole_number,exp_result", [(7, False), (0, False), (22, False), ("foo", False)]
)
def test_validate_and_update_hole_number_False(game, hole_number, exp_result):
    assert game.players[0]._validate_and_update_hole_number(hole_number) is exp_result


@pytest.mark.parametrize(
    "hole_number,exp_result", [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
)
def test_validate_and_update_hole_number_True(player_one, hole_number, exp_result):
    assert player_one._validate_and_update_hole_number(hole_number) == exp_result


@pytest.mark.parametrize("attribute", ["num_stones", "hole_counts"])
def test_attributes_board(attribute, board):
    assert hasattr(board, attribute)


def test_pit_True(game_pit, player_one):
    assert game_pit.board.pit(player_one, 0, 1)


def test_pit_False(game_pit, player_two):
    assert not game_pit.board.pit(player_two, 0, 1)


def test_add_pit_points(game_pit, player_one):
    game_pit.board.add_pit_points(player_one, 0)
    assert game_pit.board.hole_counts[12] == 0
    assert game_pit.board.hole_counts[0] == 0
    assert game_pit.points[player_one.number] == 5
