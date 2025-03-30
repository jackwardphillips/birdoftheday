from src.penney import Penney
from src.datagen import datagen

if __name__ == '__main__':
    print('Running game...')
    penney = Penney()
    generator = datagen(27)
    print(penney.last_game())
    print(len(generator.load_decks()))
    if penney.last_game() == len(generator.load_decks()):
        print('No new decks, check out the heatmap!.')
    else:
        penney.showdown()
        penney.heatmap()
        