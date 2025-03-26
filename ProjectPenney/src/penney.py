import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import deque

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

    @debugger_factory()
    def game(self, p1:list, p2:list, decks:np.array) -> tuple[int, int]:
        """
        Simulates Penney's game using sequences of cards.
        Each player chooses a sequence of cards, and the 
        function iterates through one or multiple decks and
        counts how often one player's sequence appears first,
        i.e. they win that trick.
    
        Args:
            p1 (np.array): Player 1's three-card sequence
            p2 (np.array): Player 2's three-card sequence
            decks (np.array): A collection of decks of cards
    
        Returns:
            tuple: A tuple (p1_wins, p2_wins) counting each
            player's wins.
        """
        
        p1_wins = 0 
        p2_wins = 0

        deck_length = len(decks[0])
        
        for deck in self.decks:
            
            p1_tricks = 0
            p2_tricks = 0
        
            i = 0
            while i < deck_length - 2: # stay in bounds
                if deck[i:i+3] == p1:
                    p1_tricks += 1
                    i = i+3
                
                elif deck[i:i+3] == p2:
                    p2_tricks += 1
                    i = i+3

                else:
                    i+1
            ######
            # for card in deck:
            #     hand.append(card) # draw cards
            #     if len(hand) >= 3: # don't check for your sequence until there are at least 3 cards
            #         if np.array_equal(np.array(hand), p1): # checks if the last 3 cards in the hand are the sequence
            #             p1_tricks += 1
            #             hand.clear()
            #         elif np.array_equal(np.array(hand), p2):
            #             p2_tricks += 1
            #             hand.clear()
            if p1_tricks > p2_tricks:
                p1_wins += 1
            elif p2_tricks > p1_tricks:
                p2_wins += 1
    
        return p1_wins, p2_wins
        
    @debugger_factory()
    def game_sim(self) -> pd.DataFrame:
        """
        Runs Penney's game over all different sequences
        and returns a matrix of the results.
        """
        
        win_matrix = np.zeros((8, 8))
    
        for i, p1 in enumerate(self.sequences): # enumerate over each sequence
            for j, p2 in enumerate(self.sequences):
                if i != j: # don't test sequences against themselves
                    p1_wins, p2_wins = self.game(p1, p2, self.decks)
                    if p1_wins + p2_wins == 0:
                        win_matrix[i, j] = 0
                    else:
                        win_matrix[i, j] = p1_wins/(p1_wins+p2_wins) 
    
        win_df = pd.DataFrame(win_matrix, index=[str(seq) for seq in self.sequences], columns=[str(seq) for seq in self.sequences])
        win_df = win_df.replace(0.0, np.nan)
        
        return win_df

    @debugger_factory()
    def heatmap(self, df:pd.DataFrame) -> plt.Figure:
        """
        Takes the results from game_sim() and creates
        a heatmap.
    
        Args:
            df (pd.DataFrame): A data frame of the results of game_sim
        """
    
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df, annot=True, cmap='Purples', linewidths=0.5, ax=ax)
        ax.set_xticklabels(CARD_SEQUENCES, rotation=45, ha='right')
        ax.set_yticklabels(CARD_SEQUENCES, rotation=0)
        ax.set_title(f"Penney's Game Winning Percentages over {len(self.decks)} decks.")
    
        return