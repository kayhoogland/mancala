from .create import Board, Player
from .settings import opposite_holes
import itertools as it
from numpy import argmax


class Game:
    def __init__(self, board: Board):
        self.board = board
        self.players = self.board.players

    def start_game(self):
        self.play_game()

    def play_game(self):
        for player in it.cycle(self.players):
            while True:
                if self.game_is_finished(player):
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
                if player.number == 1:
                    hole += 7
                try:
                    another_turn = self.make_move(player, hole)
                    # If you last stone ends in your point hole, you can have another go
                    if another_turn:
                        continue
                    else:
                        break
                except ValueError:
                    # Retry if you select an invalid hole
                    print('You cannot make a move for this hole, try again')
                    continue

    def make_move(self, player: Player, hole: int) -> bool:
        if hole not in player.holes:
            raise ValueError('You can only select holes on your side')

        stone_count = self.board.hole_counts[hole]
        if stone_count == 0:
            raise ValueError('You cannot select a hole that has no stones')

        self.board.hole_counts[hole] = 0
        while stone_count > 0:
            # Select the next hole
            hole += 1
            if hole == player.point_hole:
                player.add_points(1)
                # If this is the last stone you can
                if stone_count == 1:
                    return True
            elif hole == player.skip_hole:
                continue
            else:
                if hole == 14:
                    hole = 0
                if self.pit(player, hole, stone_count):
                    print('PIT!')
                    self.add_pit_points(player, hole)
                    return False
                else:
                    self.board.hole_counts[hole] += 1
            stone_count -= 1

        return False

    def other_player(self, player):
        if player.number == 0:
            return self.players[1]
        else:
            return self.players[0]

    def game_is_finished(self, player):
        stones_in_holes = sum([self.board.hole_counts[h] for h in player.holes])
        if stones_in_holes == 0:
            return True
        else:
            return False

    def add_final_points(self, player):
        player.add_points(sum([self.board.hole_counts[h] for h in player.holes]))
        for h in player.holes:
            self.board.hole_counts[h] = 0

    def pit(self, player, hole, stone_count):
        return self.board.hole_counts[hole] == 0 and hole in player.holes and stone_count == 1

    def add_pit_points(self, player, hole):
        player.add_points(1)
        opposite_hole = opposite_holes[hole]
        player.add_points(self.board.hole_counts[opposite_hole])
        self.board.hole_counts[opposite_hole] = 0
        return None

    def __repr__(self):
        return f'''
        {self.board}
        Score:
        {self.players[0].name} : {self.players[0].points}
        {self.players[1].name} : {self.players[1].points}
        '''
