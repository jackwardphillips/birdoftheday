import numpy as np
import os
import json
from src.helpers import PATH_DATA
from src.helpers import debugger_factory

HALF_DECK_SIZE = 26

class datagen:
    
    def __init__(self, 
                 seed: int
                ):
        self.seed = seed
        self.rng = np.random.default_rng(self.seed)
        self.state = self.rng.bit_generator.state
        self.half_deck_size = HALF_DECK_SIZE

        if os.path.exists(f'data/decks_{self.seed}.npy'):
            with open(f'data/state_{self.seed}.json', 'r') as f:
                self.rng.bit_generator.state = json.load(f)
        else:
            with open(f'data/state_{self.seed}.json', 'w') as f:
                json.dump(self.state, f)

    @debugger_factory()
    def create_decks(self,
                  n_decks: int
                 ) -> np.ndarray:
        """
        Efficiently generate `n_decks` shuffled decks using NumPy.
        Save the generated decks to a .npy file and the seed to a
        .json file. If no file for the specified seed exists, create 
        one. Otherwise, the new data is appended to previously
        generated data.
        """
        
        # create the decks
        init_deck = [0]*self.half_deck_size + [1]*self.half_deck_size  # Base deck
        decks = np.tile(init_deck, (n_decks, 1))
        
        self.rng.permuted(decks, axis=1, out=decks)

        # save the decks
        if os.path.exists(f'data/decks_{self.seed}.npy'):
            current = np.load(f'data/decks_{self.seed}.npy') # get the existing data
            combine = np.vstack((current, decks)) # append the new data
            np.save(f'data/decks_{self.seed}.npy', combine) # overwrite with the new data
        else:
            np.save(f'data/decks_{self.seed}.npy', decks)

        # save the state
        state = self.rng.bit_generator.state
        with open(f'data/state_{self.seed}.json', 'w') as f:
            json.dump(state, f)

        return

    @debugger_factory()
    def load_decks(self) -> np.ndarray:
        """
        Returns the decks for the instance's seed.
        """
        if os.path.exists(f'data/decks_{self.seed}.npy'):
            decks = np.load(f'data/decks_{self.seed}.npy')
            print(f'Loaded {len(decks)} decks.')
            return decks
        else:
            return 'File not found.'

    @debugger_factory()
    def get_seed(self):
        """
        Returns the seed the instance is running on.
        """
        return f'This instance is running with {self.seed} as its seed.'

    @debugger_factory()
    def get_file_path(self) -> str:
        """
        Returns the file path the decks are being saved to.
        """
        return f'data/decks_{self.seed}.npy'

    @debugger_factory()
    def delete_data(self, decks: bool = True, state: bool = True) -> str:
        """
        Deletes all of the decks and state for the instance's 
        seed, which can be set to true or false. Asks for
        confirmation before deleting each file, using "yes"
        to confirm. Prints confirmations and errors for
        deleting files. 
        """
        deck_path = f'data/decks_{self.seed}.npy'
        state_path = f'data/state_{self.seed}.json'
        if decks: # deletes the decks
            if os.path.exists(deck_path):
                confirmation = input(f'Are you sure you want to delete {deck_path}? This cannot be undone.')
                if confirmation.lower() == 'yes':
                    try:
                        os.remove(deck_path)
                        print(f"File '{deck_path}' deleted successfully.")
                        
                    except OSError as e:
                        print(f"Error deleting file: {e}")
                else:
                    print("File deletion canceled.")
            else:
                print("No data exists for this seed yet.")
                
        if state: # assuming you delete the decks you also want to delete the state
            if os.path.exists(state_path):
                confirmation = input(f'Are you sure you want to delete {state_path}? This cannot be undone.')
                if confirmation.lower() == 'yes':
                    try:
                        os.remove(state_path)
                        print(f"File '{state_path}' deleted successfully.")

                        # Reset the seed
                        self.rng = np.random.default_rng(self.seed)
                        self.state = self.rng.bit_generator.state
                                    
                    except OSError as e:
                        print(f"Error deleting file: {e}")
                else:
                    print("File deletion canceled.")
            else:
                print("No state exists for this seed yet.")