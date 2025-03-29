import re
from pathlib import Path

from src.penney import Penney
from src.datagen import datagen

def menu():
    datagen = datagen(27)
    penney = Penney()
    decks = datagen.load_decks()
    last_game = penney.last_game()
    
    print(f"""
    There are currently {len(decks)} decks.

    The last game ran with {last_game} decks.

    If you would like to create more decks, enter a positive integer. If not, enter 0 and the game will run over the unscored decks.
    """)

    menu_input = input()

    return

if __name__ == '__main__':
    menu_input = -1
    while menu_input != 0:
        menu()

    print('Running game...')
    penney = Penney()
    penney.showdown()
    
        