from mancala.game.settings import opposite_holes
from abc import abstractmethod
import numpy as np
import pandas as pd


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


class Board:
    def __init__(self, num_stones):
        self.num_stones = num_stones
        self.hole_counts = [self.num_stones] * 6 + [-1] + [self.num_stones] * 6 + [-1]
        self.hole_division = {0: [0, 1, 2, 3, 4, 5], 1: [7, 8, 9, 10, 11, 12]}

    def update(self, player: Player, hole_number: int):
        """Updates the state of the board

        :param player:
        :param hole_number:
        :return (bool): True if the player gets another turn, False if the other player gets a turn
        """

        stone_count = self.hole_counts[hole_number]
        if stone_count == 0:
            print(
                f"Player {player.number}: {player.name} You cannot select a hole that has no stones"
            )
            return True

        self.hole_counts[hole_number] = 0
        while stone_count > 0:
            # Select the next hole
            hole_number += 1
            if hole_number == player.point_hole:
                player.add_points(1)
                # If this is the last stone you can
                if stone_count == 1:
                    return True
            elif hole_number == player.skip_hole:
                continue
            else:
                if hole_number == 14:
                    hole_number = 0
                if self.pit(player, hole_number, stone_count):
                    # TODO refactor
                    if player.current_game.verbose:
                        print(f"{player.name}, {hole_number}, {stone_count}: PIT!")
                    self.add_pit_points(player, hole_number)
                    return False
                else:
                    self.hole_counts[hole_number] += 1
            stone_count -= 1

        return False

    def pit(self, player, hole, stone_count):
        return self.hole_counts[hole] == 0 and hole in player.holes and stone_count == 1

    def add_pit_points(self, player, hole):
        player.add_points(1)
        opposite_hole = opposite_holes[hole]
        player.add_points(self.hole_counts[opposite_hole])
        self.hole_counts[opposite_hole] = 0
        return None

    def get_holes_with_stones(self):
        return [index for index, hole in enumerate(self.hole_counts) if hole > 0]

    def __repr__(self):
        return f"""
    Board:
    {self.hole_counts[7:13][::-1]}
    {self.hole_counts[0:6]}
    """
