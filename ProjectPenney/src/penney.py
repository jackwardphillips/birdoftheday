import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

from src.datagen import datagen
datagen = datagen(27) # test seed, over 100,000 decks created

from src.helpers import debugger_factory
from src.helpers import SEQUENCES
from src.helpers import CARD_SEQUENCES

class Penney:
    def __init__(self):
        decks = datagen.load_decks()
        self.decks = decks
        self.sequences = SEQUENCES
        self.cards = CARD_SEQUENCES

    #@debugger_factory()
    def game(self, p1:list, p2:list, deck:np.array) -> tuple[int, int]:
        """
        Simulates Penney's game using sequences of cards.
        Each player chooses a sequence of cards, and the 
        function iterates through a given deck and
        counts how often one player's sequence appears first,
        i.e. they win that trick.
    
        Args:
            p1 (list): Player 1's three-card sequence
            p2 (list): Player 2's three-card sequence
            deck (np.array): A deck of cards
    
        Returns:
            tuple: A tuple (p1_wins, p2_wins) counting each
            player's wins.
        """

        deck = ''.join(deck.astype(str))
        p1_tricks = 0
        p2_tricks = 0
        idx = 0
        while idx < len(deck):
            try:
                p1_idx = deck.index(p1, idx)
            except ValueError:
                p1_idx = len(deck)
            try:
                p2_idx = deck.index(p2, idx)
            except ValueError:
                p2_idx = len(deck)

            if p1_idx == len(deck) and p2_idx == len(deck):
                break

            if p1_idx < p2_idx:
                p1_tricks += 1
                idx = p1_idx + 3
            elif p1_idx > p2_idx:
                p2_tricks += 1
                idx = p2_idx + 3
        
    
        return p1_tricks, p2_tricks
        
    #@debugger_factory()
    def matchup(self, p1: np.array, p2:np.array, decks: np.ndarray) -> float:
        """
        Runs Penney's game over all the decks for
        one card matchup. Uses the last_game() function
        to determine how many decks the last game was
        simulated over and doesn't run those decks again.

        Returns the number of wins and ties for each player.
        """

        p1_wins = 0
        p2_wins = 0
        draws = 0

        untested = self.last_game()
        decks = decks[untested:]
        # iterate over all the decks
        for deck in decks:
            p1_tricks, p2_tricks = self.game(p1, p2, deck)
            if p1_tricks > p2_tricks:
                p1_wins += 1
            elif p2_tricks > p1_tricks:
                p2_wins += 1
            elif p1_tricks == p2_tricks:
                draws += 1
                
        return p1_wins, p2_wins, draws

    @debugger_factory()
    def showdown(self, heatmap:bool = True) -> None:
        """
        Simulates the matchup() function over all the matchups.
        Takes the results and appends the new results to them
        or creates a new dataframe if they don't exist.
        The results are saved to a csv file in the results
        directory. The function also takes an argument, 'heatmap',
        which can be set to True or False. If True, the function
        will create a heatmap of the results and save it to the
        figures directory.
        """

        # Load in previous results
        results_path = Path("results")
        p1win_file = results_path / "p1wins.csv"
        p2win_file = results_path / "p2wins.csv"
        draw_file = results_path / "draws.csv"

        try:
            p1win_df = pd.read_csv(p1win_file, index_col=0).fillna(0).astype(int)
        except FileNotFoundError:
            p1win_df = pd.DataFrame(0, index=self.cards, columns=self.cards, dtype=int)

        try:
            p2win_df = pd.read_csv(p2win_file, index_col=0).fillna(0).astype(int)
        except FileNotFoundError:
            p2win_df = pd.DataFrame(0, index=self.cards, columns=self.cards, dtype=int)

        try:
            draw_df = pd.read_csv(draw_file, index_col=0).fillna(0).astype(int)
        except FileNotFoundError:
            draw_df = pd.DataFrame(0, index=self.cards, columns=self.cards, dtype=int)
        
        
        for i, p1 in enumerate(self.sequences):
            for j, p2 in enumerate(self.sequences):
                if i == j:
                    p1win_df.iloc[i, j] = 0
                    p2win_df.iloc[i, j] = 0
                    draw_df.iloc[i, j] = 0
                else:
                    p1_wins, p2_wins, draws = self.matchup(p1, p2, self.decks)
                    p1win_df.iloc[i, j] = p1_wins + p1win_df.iloc[i, j]
                    p2win_df.iloc[i, j] = p2_wins + p2win_df.iloc[i, j]
                    draw_df.iloc[i, j] = draws + draw_df.iloc[i, j]

        p1win_df.to_csv('results/p1wins.csv')
        p2win_df.to_csv('results/p2wins.csv')
        draw_df.to_csv('results/draws.csv')
        
        if heatmap:
            self.heatmap()
                    
        return

    @debugger_factory()
    def heatmap(self) -> plt.Figure:
        """
        Takes the results from the results folder and creates
        a heatmap.
        """

        p1_wins = pd.read_csv('results/p1wins.csv', index_col=0)
        p2_wins = pd.read_csv('results/p2wins.csv', index_col=0)
        draws = pd.read_csv('results/draws.csv', index_col=0)
        
        int_df = pd.DataFrame(index = self.cards, columns = self.cards, dtype = int)
        str_df = pd.DataFrame(index = self.cards, columns = self.cards, dtype = str)

        for i, p1 in enumerate(self.sequences):
            for j, p2 in enumerate(self.sequences):
                if i == j:
                    int_df.iloc[i, j] = np.nan
                    str_df.iloc[i, j] = ''
                else:
                    wins = int(p1_wins.iloc[i, j])
                    losses = int(p2_wins.iloc[i, j])
                    ties = int(draws.iloc[i, j])
                    
                    total_games = wins + losses + ties
                    win_pct = round((wins / total_games)*100, 0)
                    draw_pct = round((ties / total_games)*100, 0)
                    int_df.iloc[i, j] = win_pct
                    try:
                        win_pct = int(win_pct)
                        draw_pct = int(draw_pct)
                    except:
                        win_pct = 0
                        draw_pct = 0
                    
                    str_df.iloc[i, j] = f'{int(win_pct)}({int(draw_pct)})'
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(int_df, annot=str_df, fmt="", cmap='Purples', linewidths=0.5, ax=ax)
        ax.set_xticklabels(CARD_SEQUENCES, rotation=45, ha='right')
        ax.set_yticklabels(CARD_SEQUENCES, rotation=0)
        ax.set_xlabel("Player 1's Choice")
        ax.set_ylabel("Player 2's Choice")
        ax.set_title(f"Penney's Game Player 1 Win%(Draw%) over {len(self.decks)} decks.")
        
        # Save the figure
        fig_path = f"figures/heatmap_{len(self.decks)}.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
    
        return f'Figure saved to {fig_path}'

    def last_game(self) -> int:
        """
        Loads the heatmap from the last game and returns
        the number of decks that were used in the last
        game. This is used to determine how many decks
        have already been simulated over and to avoid
        running them again.
        """
        folder_path = Path("figures")
        try:
            file_path = sorted(folder_path.glob("*.png"))[-1]
        except:
            return 0

        if file_path:
            filename = file_path.stem
            match = re.search(r'\d+', filename)
            if match:
                return int(match.group())  

        return 0