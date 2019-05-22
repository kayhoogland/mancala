"""Runs a command line utility to play Mancala in"""

import fire
from mancala.game.create import Player
from mancala.game.play import Game


def main_new(p1_name='Sander', p2_name='Kay', num_stones=5):
    p1 = Player(p1_name, number=0, holes=range(6))
    p2 = Player(p2_name, number=1, holes=range(7, 13))
    game = Game(p1, p2, num_stones=num_stones)
    print(game)
    p1.make_move(1)
    print(game)
    p2.make_move(10)
    print(game)
    p2.make_move(1)
    print(game)

def cli():
    fire.Fire(main_new)


if __name__ == '__main__':
    cli()
