import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import deque
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
        one card matchup.

        Returns the number of wins and ties for each player.
        """

        p1_wins = 0
        p2_wins = 0
        draws = 0
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
    def showdown(self, heatmap:bool = True) -> pd.DataFrame:
        """
        """
        
        int_df = pd.DataFrame(index = self.cards, columns = self.cards, dtype = int)
        str_df = pd.DataFrame(index = self.cards, columns = self.cards, dtype = str)
        for i, p1 in enumerate(self.sequences):
            for j, p2 in enumerate(self.sequences):
                if i == j:
                    int_df.iloc[i, j] = np.nan
                    str_df.iloc[i, j] = ''
                else:
                    p1_wins, p2_wins, draws = self.matchup(p1, p2, self.decks)
                    total_games = p1_wins + p2_wins + draws
                    win_pct = round((p1_wins / total_games)*100, 0)
                    draw_pct = round((draws / total_games)*100, 0)
                    int_df.iloc[i, j] = win_pct
                    str_df.iloc[i, j] = f'{int(win_pct)}({int(draw_pct)})'
        if heatmap:
            self.heatmap(int_df, str_df)
                    
        return int_df, str_df

    @debugger_factory()
    def heatmap(self, int_df:pd.DataFrame, str_df:pd.DataFrame) -> plt.Figure:
        """
        Takes the results from game_sim() and creates
        a heatmap.
    
        Args:
            df (pd.DataFrame): A data frame of the results of game_sim
        """
    
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(int_df, annot=str_df, fmt="", cmap='Purples', linewidths=0.5, ax=ax)
        ax.set_xticklabels(CARD_SEQUENCES, rotation=45, ha='right')
        ax.set_yticklabels(CARD_SEQUENCES, rotation=0)
        ax.set_xlabel("Player 1's Choice")
        ax.set_ylabel("Player 2's Choice")
        ax.set_title(f"Penney's Game Player 1 Win%(Draw%) over {len(self.decks)} decks.")

        folder = Path(figures)
        for file in folder
            os.remove(file)
        
        # Save the figure
        fig_path = f"figures/heatmap_{len(self.decks)}.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
    
        return f'Figure saved to {fig_path}'

    def last_game() -> int:
        folder_path = Path("figures")
        file_path = next(folder_path.glob("*.png"), None)  # Get the first .png file, or None if no file

        if file_path:
            filename = file_path.stem
            match = re.search(r'\d+', filename)
            if match:
                return int(match.group())  

        return 0  

    def 

            