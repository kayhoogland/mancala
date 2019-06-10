from mancala.game.create import Player
import random
import time


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
        my_possible_moves = self.current_game.possible_moves[self.number]
        time.sleep(1)
        return random.choice(my_possible_moves)
