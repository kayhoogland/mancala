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


def play_game(game: Game):
    while not game.game_finished:
        try:
            # TODO: print gamestate in case of multiple moves moves
            print("-" * 50)
            print(game)
            print("-" * 50)
            current_player = game.players[game.turn_of_player]
            current_player.take_turn()
        except (ValueError, TypeError) as e:
            print(type(e), "Please choose an input between 1 and 6")

    # Always output the final score
    print("-" * 50)
    print("Final Score:")
    print(game)
    print("-" * 50)


def cli():
    fire.Fire(main_new)


if __name__ == "__main__":
    cli()
