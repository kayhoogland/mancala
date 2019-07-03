from mancala.game.play import Game
from mancala.agents import RandomBot, GreedyBot, QBot, MyRegression
from mancala.api.cli import play_game

import numpy as np
import pandas as pd
from tqdm import tqdm
import copy
from pathlib import Path


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
        list_of_scores = []
        for _ in tqdm(range(self.epochs)):
            game = Game(self.players[0], self.players[1], num_stones=self.num_stones)
            game.verbose = verbose
            p1_points, p2_points = play_game(game, verbose=verbose)
            winner = self.players[0].name if p1_points > p2_points else self.players[1].name
            list_of_scores.append((p1_points, p2_points, winner))
            list_of_games.append(copy.deepcopy(game))
        self.scores = pd.DataFrame(data=list_of_scores, columns=self.scores.columns)

        list_of_game_rewards = [game.players[0].calculate_rewards() for game in list_of_games]
        return self.scores, list_of_game_rewards


class SimulationProcessor:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    @staticmethod
    def change_dtypes(df):
        """Changes dtypes of imoprtant columns"""
        return (df
            .assign(
            action=lambda d: d['action'].astype(int),
            player=lambda d: d['player'].astype(int),
            delta_score_p0=lambda d: d['delta_score_p0'].astype(int),
            delta_score_p1=lambda d: d['delta_score_p1'].astype(int),
            relevant_round=lambda d: d['relevant_round'].astype(int),
            opponent_score_in_relevant_round=lambda d: d['opponent_score_in_relevant_round'].astype(int),
        )
        )

    @staticmethod
    def add_game_number(df):
        """Adds the Game number to the Dataframe"""
        s = df['BoardState'].apply(lambda row: row == [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        game_series = (pd.DataFrame.from_items(zip(s.index, s.values))
                       .all(axis=0)
                       .cumsum()
                       .rename('game')
                       )
        return df.join(game_series)

    @staticmethod
    def add_normalized_reward(df, span=3):
        return (df
                .assign(normalized_reward=lambda d: (d.groupby(['game', 'player'])['reward']
                                                     .apply(lambda row: row.ewm(span=span)
                                                            .mean())
                                                     )
                        )
                )

    @staticmethod
    def calculate_winner_of_game(df):
        """Calculate the winner of each game and return this as a series"""
        winners_series = (df
                          .groupby(['game'])
                          .apply(lambda game: np.argmax([game['score_p0'].max(), game['score_p1'].max()]))
                          .rename('winner_of_game')
                          )
        return winners_series

    def update_reward(self, df):
        """Updating reward series by Adding/subtracting final points to winner/loser respectively."""

        winners_frame = self.calculate_winner_of_game(df).to_frame()

        new_reward_series = (df
                             .reset_index()  # We need the index for the groupby
                             .groupby(['game', 'player']).agg({'index': 'last',
                                                               'reward': 'last',
                                                               })
                             .reset_index()
                             .merge(winners_frame, left_on='game', right_index=True)
                             .assign(reward=lambda d: d.apply(self.add_final_points_to_last_move, axis=1))
                             .drop(columns=['game', 'player', 'winner_of_game'])
                             .set_index('index')
                             .reindex(df.index)['reward']
                             .fillna(df['reward'])
                             )
        return df.assign(reward=new_reward_series)

    @staticmethod
    def add_ewma_reward(df, alpha=0.1, span=None, halflife=None):
        ewma_reward_series = (df
                              .groupby(['game', 'player'])['reward']
                              .apply(lambda row: row.sort_index(ascending=False).ewm(alpha=alpha,
                                                                                     span=span,
                                                                                     halflife=halflife).mean())
                              .reset_index()
                              .rename({'level_2': 'index', 'reward': 'ewma_reward'}, axis='columns')
                              .set_index('index')
                              .drop(['game', 'player'], axis=1)
                              .sort_index()
                              )
        return df.join(ewma_reward_series)

    @staticmethod
    def add_move_of_player_in_game(df):
        move_in_game_series = (df
                               .assign(dummy=1)
                               .groupby(['game', 'player'])['dummy']
                               .cumsum()
                               .rename('move_of_player_in_game')
                               )
        return df.join(move_in_game_series)

    @staticmethod
    def add_final_points_to_last_move(row, final_reward=100):
        """Adds/subtracts final points to winner/loser respectively.

        Checks for each row if that player is the winner of the game,
        and adds/subtracts final_reward accordingly

        """
        return row['reward'] + ((row['winner_of_game'] == row['player']) * 2 - 1) * final_reward

    def __call__(self, *args, **kwargs):
        data = (pd.read_parquet(self.input_file)
                .pipe(self.change_dtypes)
                .reset_index(drop=True)
                .pipe(self.add_game_number)
                .pipe(self.add_move_of_player_in_game)
                .pipe(self.update_reward)
                .pipe(self.add_ewma_reward)
                )
        data.to_parquet(self.output_file)


def main(epochs):
    p1 = GreedyBot(name='GreedyBot', number=0)
    p2 = GreedyBot(name='GreedyBot2', number=1)
    simulation = Simulation(p1, p2, epochs=epochs, num_stones=4)
    scores, list_of_game_rewards = simulation.simulate(verbose=False)
    pd.concat(list_of_game_rewards).to_parquet(Path('../data') / f'{p1.name}_{p2.name}_{int(epochs / 1000)}k.parquet')
    print(scores['Winner'].value_counts(normalize=True))


def main_q(epochs):
    p1 = QBot(name='QBot', number=0, model_path='../../notebooks/model_Greedy_vs_Random.pth')
    p2 = RandomBot(name='RandomBot', number=1)
    simulation = Simulation(p1, p2, epochs=epochs, num_stones=4)
    scores, list_of_game_rewards = simulation.simulate(verbose=False)
    pd.concat(list_of_game_rewards).to_parquet(Path('../data') / f'{p1.name}_{p2.name}_{int(epochs / 1000)}k.parquet')
    print(scores['Winner'].value_counts(normalize=True))


def process(epochs):
    input_file = f'../data/GreedyBot_GreedyBot2_{int(epochs / 1000)}k.parquet'
    output_file = f'../data/GreedyBot_GreedyBot2_{int(epochs / 1000)}k_clean.parquet'

    simulation_processor = SimulationProcessor(input_file, output_file)
    simulation_processor()


if __name__ == '__main__':
    epochs = 2000
    main_q(epochs)
    # process(epochs)
