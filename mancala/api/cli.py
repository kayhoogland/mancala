"""Runs a command line utility to play Mancala in"""

import fire
from mancala.game.play import Game
from mancala.agents import RandomBot, Human, GreedyBot


def main_new(p1="Sander", p2="Kay", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = Human(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def main_bot(p1="Sander", p2="RandomBot", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = RandomBot(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def main_greedybot(p1="Sander", p2="GreedyBot", num_stones=4):
    p1 = Human(name=p1, number=0)
    p2 = GreedyBot(name=p2, number=1)
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def main_random_greedybot(p1="RandomBot", p2="GreedyBot", num_stones=4):
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
    fire.Fire(main_random_greedybot)


if __name__ == "__main__":
    cli()
