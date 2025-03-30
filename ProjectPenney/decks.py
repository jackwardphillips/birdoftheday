from src.datagen import datagen

if __name__ == '__main__':
    data_generator = datagen(27)
    decks = data_generator.load_decks()
    print(f'There are currently {len(decks)} decks.')
    decks = int(input('Enter how many decks you would like to create: '))
    data_generator.create_decks(decks)