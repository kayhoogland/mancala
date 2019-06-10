import pytest
from mancala.game.create import Player, Board
from mancala.game.play import Game
from mancala.agents import RandomBot, Human


@pytest.fixture(
    scope="module",
    params=[Human(name="John", number=0), Human(name="Claire", number=1)],
)
def players(request):
    return request.param


@pytest.fixture
def player_one():
    return Human(name="John", number=0)


@pytest.fixture
def player_two():
    return Human(name="Claire", number=1)


@pytest.fixture
def board():
    return Board(num_stones=4)


@pytest.fixture
def game_pit(player_one, player_two):
    g = Game(player_one, player_two, 4)
    g.board.hole_counts[0] = 0
    return g


@pytest.fixture
def game(player_one, player_two):
    return Game(player_one, player_two, 4)
