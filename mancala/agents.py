import random
import copy
import time

import numpy as np
from numpy import argmax
import operator
from abc import abstractmethod
import torch
from torch import nn
import torch.nn.functional as F

class MyRegression(nn.Module):
    def __init__(self, k, hidden):
        super().__init__()
        self.linear1 = nn.Linear(k, hidden * 2)
        self.linear2 = nn.Linear(hidden * 2, hidden)
        self.linear_last = nn.Linear(hidden, 6)

    def forward(self, x_in):
        hidden = F.relu(self.linear1(x_in))
        hidden = F.relu(self.linear2(hidden))
        return self.linear_last(hidden)

class Player:
    def __init__(self, name, number):
        self.name = name
        self.current_game = None

        # I don't really like it that a player has all this information below.
        # I have the feeling these things need to be stored in the Game object.
        # This is important for when you reset a game, but don't want to reset a player.
        # this will do for now, but keep in mind for the future
        self.number = number

        self.holes = range(6) if number == 0 else range(7, 13)
        self.point_hole = 6 if number == 0 else 13
        self.skip_hole = 13 if number == 0 else 6

    def start_game(self, game):
        self.current_game = game

    def add_points(self, points):
        # TODO: Kay: is this function really necessary?
        self.current_game.points[self.number] += points

    def take_turn(self):
        """Until it is not your turn anymore, make moves"""
        while self.current_game.turn_of_player == self.number:
            move = self.decide_move()
            self.make_move(move)

    @abstractmethod
    def decide_move(self):
        pass

    def hole_number_to_action(self, hole_number: int):
        """action needs to end in the range (1, 7), inverse of action_to_hole_number"""
        if self.number == 1:
            hole_number -= 7
        hole_number += 1

        action = hole_number
        return action

    def action_to_hole_number(self, action: int):

        # make the action 1 smaller so it comes in the range(0, 6) for indexing
        action -= 1
        # the second player (player.number==1) needs to add 7 to its action before we send it to the game
        if self.number == 1:
            action += 7

        hole_number = action
        return hole_number

    def calculate_rewards(self):
        game_stack = (self.current_game.create_dataframe_game_stack()
                      .assign(relevant_round=lambda d: np.select([d['player'] == 0, d['player'] == 1],
                                                                 [d['round'], d['round'] + 1],
                                                                 default=np.nan)
                              )
                      )

        round_scores = (game_stack
                        .groupby(['player', 'round']).agg({'delta_score_p0': 'sum',
                                                           'delta_score_p1': 'sum'
                                                           })
                        .reset_index()
                        .assign(score_in_round=lambda d: np.select([d['player'] == 0, d['player'] == 1],
                                                                             [d['delta_score_p0'], d['delta_score_p1']],
                                                                             default=np.nan
                                                                             ),
                                other_player=lambda d: 1 - d['player']
                                )
                        .drop(['delta_score_p0', 'delta_score_p1', 'player'], axis='columns')
                        )
        return (game_stack
                .merge(round_scores,
                       left_on=['player', 'relevant_round'],
                       right_on=['other_player', 'round'],
                       how='left')
                .rename(columns={'score_in_round': 'opponent_score_in_relevant_round',
                                 'round_x': 'round'})
                .drop(columns=['round_y'])
                .assign(opponent_score_in_relevant_round = lambda d: d['opponent_score_in_relevant_round'].fillna(0),
                        reward=lambda d: np.where(d['player'] == 0,

                                                  d['delta_score_p0'] - d['opponent_score_in_relevant_round'],
                                                  d['delta_score_p1'] - d['opponent_score_in_relevant_round'])
                        )
                .iloc[1:]  # Drop the first row because it contains initial information which doesn't contain a move.
                )

    def make_move(self, hole_number: int):
        """

        :param hole_number: (int) number between [1, 6]
        :return (bool): True if move was successful, False instead.
        """
        correct_hole_number = self._validate_and_update_hole_number(hole_number)

        # Explicitly check if the correct_hole_number is a boolean & False
        # We do this because an valid option in the game is to select hole nr. 0.
        # without explicit checking if this is a bool, this would result in unwanted behaviour
        if not correct_hole_number and isinstance(correct_hole_number, bool):
            return False
        return self.current_game.try_move(self, correct_hole_number)

    def _validate_and_update_hole_number(self, action: int):
        if action not in range(1, 7):
            if self.current_game.verbose:
                print(
                    f"Player {self.number}: {self.name} You selected hole number {action}, You can choose a hole between 1 and 6."
                )
            return False

        return self.action_to_hole_number(action)

    def __repr__(self):
        return f"Player {self.name} has {self.current_game.points[self.number]} points."


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


class QBot(Bot):
    """"""

    def __init__(self, model_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = torch.load(model_path)

    def decide_move(self):
        my_possible_moves = self.current_game.possible_moves[self.number]
        torch_input = torch.FloatTensor(self.current_game.board_state)
        output_tensor = self.model(torch_input)

        for i in range(6):
            if i + 1 not in my_possible_moves:
                output_tensor[i] = -999

        move = np.argmax(output_tensor.detach().numpy()) + 1
        return move


class MinMaxBot(Bot):
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
