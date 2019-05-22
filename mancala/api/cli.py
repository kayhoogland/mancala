"""Runs a command line utility to play Mancala in"""

import fire
from mancala.game.create import Player
from mancala.game.play import Game


def main_new(p1='Sander', p2='Kay', num_stones=5):
    p1 = Player(p1, number=0, holes=range(6))
    p2 = Player(p2, number=1, holes=range(7, 13))
    game = Game(p1, p2, num_stones=num_stones)
    play_game(game)


def play_game(game: Game):
    while True:
        try:
            print('-' * 50)
            print(game)
            print('-' * 50)
            current_player = game.players[game.turn_of_player]
            hole = int(input(f"{current_player.name}'s turn: "))
            current_player.make_move(hole)
        except (ValueError, TypeError) as e:
            print(type(e), 'Please choose an input between 1 and 6')


def cli():
    fire.Fire(main_new)


if __name__ == '__main__':
    cli()
