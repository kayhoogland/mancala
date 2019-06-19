from mancala.game.play import Game
from mancala.agents import RandomBot, GreedyBot
from mancala.api.cli import play_game
import pandas as pd
from tqdm import tqdm


class Simulation:
    def __init__(self, p1, p2, epochs, num_stones=4):
        """Simulation class for Mancala games"""
        self.players = (p1, p2)
        self.epochs = epochs
        self.num_stones = num_stones

        self.scores = pd.DataFrame(columns=[f'{p1.name} score',
                                            f'{p2.name} score',
                                            'Winner'
                                            ])

    def simulate(self, verbose=False):
        """Simulates a number of games and returns a DataFrame with scores"""
        list_of_games = []
        for _ in tqdm(range(self.epochs)):
            game = Game(self.players[0], self.players[1], num_stones=self.num_stones)
            game.verbose = verbose
            p1_points, p2_points = play_game(game, verbose=verbose)
            winner = self.players[0].name if p1_points > p2_points else self.players[1].name
            list_of_games.append((p1_points, p2_points, winner))
        self.scores = pd.DataFrame(data=list_of_games, columns=self.scores.columns)
        return self.scores


def main():
    p1 = RandomBot(name='RandomBot', number=0)
    p2 = GreedyBot(name='GreedyBot', number=1)
    simulation = Simulation(p1, p2, epochs=1000, num_stones=4)
    scores = simulation.simulate(verbose=False)
    print(scores['Winner'].value_counts(normalize=True))


if __name__ == '__main__':
    main()
