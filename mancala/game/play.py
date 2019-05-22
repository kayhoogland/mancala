from mancala.game.create import Board, Player
import itertools as it
import warnings
from numpy import argmax


class Game:
    def __init__(self, p1, p2,  num_stones):
        self.players = [p1, p2]
        self.board = Board(num_stones)
        p1.current_game = self
        p2.current_game = self

        self.turn_of_player = 0

        # list of turns successfully & consecutively executed in the following format
        # [
        #    (player.name, hole_number),
        #    (player.name, hole_number),
        #    ...
        # ]
        self.turns_executed = []

    def start_game(self):
        self.play_game()

    def play_game(self):
        for player in it.cycle(self.players):
            while True:
                if not self._check_is_game_not_finished(player):
                    # Other player gets all the points on his side
                    other_player = self.other_player(player)
                    self.add_final_points(other_player)
                    # The player with the highest score wins
                    scores = [player.points for player in self.players]
                    print(f'Game is finished, {self.players[argmax(scores)].name} won!')
                    print(self)
                    return True

                print(f'Player {player.name} is up!')
                # Print the board to see what moves are available
                print(self)
                hole = int(input())
                # Make it more convenient for the player two to select a hole

    def other_player(self, player):
        return self.players[(1-player.number)]

    def add_final_points(self, player):
        player.add_points(sum([self.board.hole_counts[h] for h in player.holes]))
        for h in player.holes:
            self.board.hole_counts[h] = 0

    def try_move(self, player: Player, hole_number: int):
        """Tries to execute the attempted move in the current game. Returns True if successful, False instead.

        hole_number is a number in range(0, 6) for player.number == 0,
        hole_number is a number in range(7, 13) for player.number == 1,
        """

        # If it is the turn of that player, try to update the board
        if self._check_is_turn_of_player(player) and self._check_is_game_not_finished(player):
            # Try to update the board with the proposed move
            player_gets_another_turn = self.board.update(player, hole_number)

            # if the player is not allowed to do another turn; update whose turn it is
            if not player_gets_another_turn:
                self.turn_of_player = 1 - self.turn_of_player
            self.turns_executed.append((player.name, hole_number))
            return True

        return False

    def _check_is_turn_of_player(self, player: Player):
        """Returns True if it is the turn of the player in the current game, False instead."""
        if self.turn_of_player == player.number:
            return True
        warnings.warn(f"{player.name} tried to take a turn but it is the turn of {self.other_player(player).name}.")
        return False

    def _check_is_game_not_finished(self, player):
        """Returns True if the game is not finished, False instead."""
        stones_in_holes = sum([self.board.hole_counts[h] for h in player.holes])
        return True if stones_in_holes > 0 else False

    def __repr__(self):
        return f'''
        {self.board}
        Score:
        {self.players[0].name}: {self.players[0].points}
        {self.players[1].name}: {self.players[1].points}
        '''
