from mancala.game.create import Player
import random
import copy
import time
from numpy import argmax


class Human(Player):
    def decide_move(self):
        return int(input(f"{self.name}'s turn: "))


class RandomBot(Player):
    def __init__(self, random_seed: int = 42, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self)
        self.random_seed = random_seed

    def decide_move(self):
        """Chooses a random move based on the passible moveset"""
        time.sleep(1)
        my_possible_moves = self.current_game.possible_moves[self.number]
        return random.choice(my_possible_moves)


class GreedyBot(Player):
    def decide_move(self):
        time.sleep(1)
        my_possible_moves = self.current_game.possible_moves[self.number]
        move_points = []
        for move in my_possible_moves:
            copy_game = copy.deepcopy(self.current_game)
            points_before = copy_game.points[self.number]
            copy_game.players[self.number].make_move(move)
            points_after = copy_game.points[self.number]
            move_points.append(points_after - points_before)

        print(f"Move points: {move_points}")
        return my_possible_moves[argmax(move_points)]
