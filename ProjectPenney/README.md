### Penney's Game Simulation

This repository contains a simulation of Penney's Game. Penney's game isa "binary sequence generating game between two players" (from Wikipedia). The first player selects a sequence of cards in a deck, choosing between red and black. The second player then chooses their own sequence. Cards  are drawn from the deck and if your sequence appears first, you win that hand. 

## How to Use

The repository contains two folders, a src and data folder. The former contains three .py files, helpers.py, datagen.py, and penney.py. 

Helpers.py contains a debugger factory, as well as the sequences the game is tested on as well as the sequences the heatmap produced in penney.py shows.

Datagen.py is where the decks of cards are created. By calling create_decks, the function will create the amount of decks specified and randomly shuffle them all from a given seed. This seed state is also saved so more decks can be generated with no (or very little) chance of repetition. 

Penney.py is where the game is simulated. The class Penney has three functions: game, game_sim, and heatmap. Game simulates Penney's game over multiple decks of cards. This is used by game_sim, which stores the experimental odds of each sequence against the other sequences. The function heatmap takes the dataframe returned by game_sim and creates a heatmap to visualize the results.

In the provided example.ipynb file, if you download the repository you can see how the game can be simulated.

## Dependencies

This repository uses numpy, pandas, seaborn, and matplotlib.