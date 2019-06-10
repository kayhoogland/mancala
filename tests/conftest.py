import pytest
from mancala.game.create import Player, Board
from mancala.game.play import Game
from mancala.agents import RandomBot, Human


@pytest.fixture(
    scope="module",
    params=[
        Human(name="John", number=0, holes=range(6)),
        Human(name="Claire", number=1, holes=range(7, 13)),
    ],
)
def players(request):
    return request.param


@pytest.fixture
def player_one():
    return Human(name="John", number=0, holes=range(6))


@pytest.fixture
def player_two():
    return Human(name="Claire", number=1, holes=range(7, 13))


@pytest.fixture
def board():
    return Board(num_stones=4)


@pytest.fixture
def board_pit():
    b = Board(num_stones=4)
    b.hole_counts[0] = 0
    return b


@pytest.fixture
def game(player_one, player_two):
    return Game(player_one, player_two, 4)

