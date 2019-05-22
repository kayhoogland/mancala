"""Runs a command line utility to play Mancala in"""

import fire
from mancala.game.create import Board
from mancala.game.play import Game


def main(num_stones=4, p1='Sander', p2='Kay'):
    game = Game(Board(num_stones, p1, p2))
    game.play_game()


def cli():
    fire.Fire(main)


if __name__ == '__main__':
    cli()
