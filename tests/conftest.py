import pytest
from mancala.game.create import Player, Board


@pytest.fixture(
    scope="module",
    params=[
        Player(name="John", number=0, holes=range(6)),
        Player(name="Claire", number=1, holes=range(7, 13)),
    ],
)
def players(request):
    return request.param


@pytest.fixture
def player_one():
    return Player(name="John", number=0, holes=range(6))


@pytest.fixture
def player_two():
    return Player(name="Claire", number=1, holes=range(7, 13))


@pytest.fixture
def board():
    return Board(num_stones=4)


@pytest.fixture
def board_pit():
    b = Board(num_stones=4)
    b.hole_counts[0] = 0
    return b
