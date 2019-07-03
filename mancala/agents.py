from mancala.game.create import Player
import random
import copy
import time
from numpy import argmax
import operator
from abc import abstractmethod


class Human(Player):
    def decide_move(self):
        return int(input(f"{self.name}'s turn: "))


class Bot(Player):
    def __init__(self, sleep_timer: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_timer = sleep_timer

    @abstractmethod
    def decide_move(self):
        pass


class RandomBot(Bot):
    def __init__(self, random_seed: int = 42, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_seed = random_seed

    def decide_move(self):
        """Chooses a random move based on the passible moveset"""
        time.sleep(self.sleep_timer)
        my_possible_moves = self.current_game.possible_moves[self.number]
        return random.choice(my_possible_moves)


class GreedyBot(Bot):
    def decide_move(self):
        time.sleep(self.sleep_timer)
        move_points = []
        my_possible_moves = self.current_game.possible_moves[self.number]
        for move in my_possible_moves:
            copy_game = copy.deepcopy(self.current_game)
            copy_game.verbose = False

            points_before = copy_game.points[self.number]
            copy_game.players[self.number].make_move(move)
            points_after = copy_game.points[self.number]
            move_points.append(points_after - points_before)

        if self.current_game.verbose:
            print(f"Move points: {move_points}")
        return my_possible_moves[argmax(move_points)]

    def decide_move_recursive(self, moves=None, move_points=None, current_game=None):
        if not current_game:
            current_game = self.current_game

        if not moves:
            moves = []

        if not move_points:
            move_points = {}

        my_possible_moves = current_game.possible_moves[self.number]

        for move in my_possible_moves:
            copy_game = copy.deepcopy(current_game)
            copy_game.verbose = False

            points_before = copy_game.points[self.number]
            copy_game.players[self.number].make_move(move)
            points_after = copy_game.points[self.number]

            moves.append(move)
            if copy_game.turn_of_player == self.number:
                self.decide_move_recursive(
                    moves=moves, move_points=move_points, current_game=copy_game
                )
            move_points[tuple(moves)] = points_after - points_before

        if self.current_game.verbose:
            print(f"Move points: {move_points}")
        best_turn = max(move_points.iteritems(), key=operator.itemgetter(1))[0]

        return my_possible_moves[best_turn]


class MaximinBot(Bot):
    def decide_move(self):
        time.sleep(self.sleep_timer)
        my_possible_moves = self.current_game.possible_moves[self.number]
        move_points = []
        for move in my_possible_moves:
            copy_game = copy.deepcopy(self.current_game)
            copy_game.verbose = False
            opponent_number = copy_game.other_player().number
            copy_game.players[opponent_number] = GreedyBot(
                "GreedyTempBot", number=opponent_number
            )

            points_before = copy_game.points[self.number]
            while copy_game.turn_of_player == self.number:
                move = copy_game.players[self.number].decide_move(move)
                copy_game.players[self.number].make_move(move)
            points_after = copy_game.points[self.number]

            move_points.append(points_after - points_before)

        if self.current_game.verbose:
            print(f"Move points: {move_points}")
        return my_possible_moves[argmax(move_points)]
