from mancala.game.create import Board, Player
import itertools as it
import warnings
from numpy import argmax
import pandas as pd


class Game:
    def __init__(self, p1, p2, num_stones, verbose: bool = True):
        self.players = [p1, p2]
        self.points = [0, 0]
        self.board = Board(num_stones)
        self.turn_of_player = 0
        self.game_finished = False
        self.possible_moves = {0: (1, 2, 3, 4, 5, 6), 1: (1, 2, 3, 4, 5, 6)}

        p1.current_game = self
        p2.current_game = self
        self.verbose = verbose

        # TODO: implement board history so you can roll back in time?

        # list of turns successfully & consecutively executed in the following format
        # [
        #    (player.name, hole_number),
        #    (player.name, hole_number),
        #    ...
        # ]
        self.turns_executed = []

    def other_player(self, player: Player):
        return self.players[(1 - player.number)]

    def add_final_points(self, player: Player):
        self.points[player.number] += sum(
            [self.board.hole_counts[h] for h in player.holes]
        )
        for h in player.holes:
            self.board.hole_counts[h] = 0

    def try_move(self, player: Player, hole_number: int):
        """Tries to execute the attempted move in the current game. Returns True if successful, False instead.

        hole_number is a number in range(0, 6) for player.number == 0,
        hole_number is a number in range(7, 13) for player.number == 1,
        """

        # If it is the turn of that player, try to update the board
        if not self.game_finished and self._check_is_turn_of_player(player):
            # Try to update the board with the proposed move
            player_gets_another_turn = self.board.update(player, hole_number)
            self._update_possible_moves()

            # Update state of the game
            # if the player is not allowed to do another turn; update whose turn it is
            if not player_gets_another_turn:
                self.turn_of_player = 1 - self.turn_of_player
            self.turns_executed.append((player.name, hole_number))
            self.game_finished = self._check_is_game_finished(player)
            return True
        return False

    def _update_possible_moves(self):
        # TODO: Need refactor
        holes_with_stones = self.board.get_holes_with_stones()
        possible_moves_p1 = []
        possible_moves_p2 = []
        for h in holes_with_stones:
            if h < 6:
                possible_moves_p1.append(h + 1)
            if 6 < h < 13:
                possible_moves_p2.append(h - 6)

        self.possible_moves[0] = tuple(possible_moves_p1)
        self.possible_moves[1] = tuple(possible_moves_p2)

    def _check_is_turn_of_player(self, player: Player):
        """Returns True if it is the turn of the player in the current game, False instead."""
        if self.turn_of_player == player.number:
            return True
        warnings.warn(
            f"{player.name} tried to take a turn but it is the turn of {self.other_player(player).name}."
        )
        return False

    def _check_is_game_finished(self, player):
        """Returns True if the game is not finished, False instead."""
        stones_in_holes_p1 = sum([self.board.hole_counts[h] for h in player.holes])
        stones_in_holes_p2 = sum([self.board.hole_counts[h] for h in self.other_player(player).holes])

        if stones_in_holes_p1 == 0 or stones_in_holes_p2 == 0:
            self.add_final_points(player)
            self.add_final_points(self.other_player(player))
            self.turn_of_player = -1
            # TODO: incorporate if a game is a tie.
            if self.verbose:
                print(
                    f"Game is finished, {self.players[argmax(self.points)].name} won!"
                )
            return True
        return False

    def __repr__(self):
        return f"""
        {self.board}
        
        Score:
        {self.players[0].name}: {self.points[0]}
        {self.players[1].name}: {self.points[1]}
        """
