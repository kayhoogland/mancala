import pytest


@pytest.mark.parametrize(
    "attribute",
    ["name", "current_game", "number", "holes", "point_hole", "skip_hole", "points"],
)
def test_attributes_player(attribute, players):
    assert hasattr(players, attribute)


@pytest.mark.parametrize(
    "hole_number,exp_result", [(7, False), (0, False), (22, False), ("foo", False)]
)
def test_validate_and_update_hole_number_False(player_one, hole_number, exp_result):
    assert player_one._validate_and_update_hole_number(hole_number) is exp_result


@pytest.mark.parametrize(
    "hole_number,exp_result", [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
)
def test_validate_and_update_hole_number_True(player_one, hole_number, exp_result):
    assert player_one._validate_and_update_hole_number(hole_number) == exp_result


@pytest.mark.parametrize("attribute", ["num_stones", "hole_counts"])
def test_attributes_board(attribute, board):
    assert hasattr(board, attribute)


def test_pit_True(board_pit, player_one):
    assert board_pit.pit(player_one, 0, 1)


def test_pit_False(board_pit, player_two):
    assert not board_pit.pit(player_two, 0, 1)


def test_add_pit_points(board_pit, player_one):
    board_pit.add_pit_points(player_one, 0)
    assert board_pit.hole_counts[12] == 0
    assert board_pit.hole_counts[0] == 0
    assert player_one.points == 5
