"""Runs a command line utility to play Mancala in"""

import fire
from mancala.game.play import Game
from mancala.agents import RandomBot, Human, GreedyBot


def two_player_game(p1="Sander", p2="Kay", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = Human(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def random_bot_game(p1="Sander", p2="RandomBot", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = RandomBot(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def greedy_bot_game(p1="Sander", p2="GreedyBot", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = GreedyBot(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def bot_game(p1="RandomBot", p2="GreedyBot", num_stones=4):
    p1 = RandomBot(name=p1, number=0)
    p2 = GreedyBot(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def play_game(game: Game, verbose=True):
    """Returns the points obtained by each player"""
    while not game.game_finished:
        # TODO: print gamestate in case of multiple moves moves
        if verbose: print("-" * 50)
        if verbose: print(game)
        if verbose: print("-" * 50)
        current_player = game.players[game.turn_of_player]
        current_player.take_turn()

    # Always output the final score
    if verbose: print("-" * 50)
    if verbose: print("Final Score:")
    if verbose: print(game)
    if verbose: print("-" * 50)
    return game.points[0], game.points[1]


def cli():
    fire.Fire(
        {1: greedy_bot_game,
         2: two_player_game,
         'random': random_bot_game,
         'greedy': greedy_bot_game,
         'bots': bot_game,
         }
    )


if __name__ == "__main__":
    cli()
