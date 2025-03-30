### Penney's Game Simulation

This repository contains a simulation of Penney's Game. Penney's game isa "binary sequence generating game between two players" (from Wikipedia). The first player selects a sequence of cards in a deck, choosing between red and black. The second player then chooses their own sequence. Cards  are drawn from the deck and if your sequence appears first, you win that hand. 

## How to Use

The repository contains four folders and two main python scripts. The first folder is the src folder, which contains the code for creating the shuffled decks of cards and simulating the game. The second is the data folder, where seeds and instances are saved so the deck generator doesn't duplicate any decks. The third is the results folder, which stores the number of wins and draws for each player, so the game can be simulated over more decks without simulating over decks that have already been tested. The last is the figures folder, which is where heatmaps are saved. Heatmaps are saved with the number of decks they were created from in the name.

The two python scripts are decks.py and game.py. Decks.py is where you can create decks, running

uv run main.py

will prompt you to enter a number to create more decks, and will create them. It will also tell you how many decks already exist. The second python script is game.py, where the game is actually simulated. It will run the game and create a new heatmap for you.

## Dependencies

This repository uses numpy, pandas, seaborn, matplotlib, pathlib, re, datetime, os, and json.