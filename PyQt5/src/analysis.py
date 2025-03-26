import pandas as pd
import numpy as np

from src.helpers import check_directory

PATH_DATA = 'data/'

class RandomDataAnalysis:
    '''
    Contains a data object which is a pandas DataFrame with columns labeled 'x' and 'y'
    '''
    
    __slots__ = ('data')

    def __init__(self):
        self.make_random_data()
        self.check_directories()
        return
    
    def check_directories(self) -> None:
        '''
        Ensure any required directories exist
        '''
        check_directory(PATH_DATA)
        return None

    def save_data(self, file_name: str) -> None:
        '''
        Output the currently loaded data as a .csv file.
        '''
        if file_name != '':
            print(f'Saving: {file_name}.csv')
            self.data.to_csv(f'{file_name}.csv', index=False)
        return None
    
    def load_data(self, file_name: str) -> None:
        '''
        Load a data file.
        '''
        self.data = pd.read_csv(file_name)
        return None

    def make_random_data(self, 
                         num_points:int = 100
                         ) -> None:
        '''
        Generate some random data.
        '''
        data = np.random.normal(size=(num_points, 2))
        data[:,1] = data[:,0] + 0.5*data[:,1]**2
        self.data = pd.DataFrame(data, columns=['x','y'])
        return None
    
    def get_data(self, 
                 as_frame: bool = False
                 ) -> np.ndarray | pd.DataFrame:
        '''
        Return the current data as either a pandas DataFrame or a numpy array
        '''
        if as_frame:
            return self.data
        else:
            return self.data.values
    
    def get_x(self) -> np.ndarray:
        return self.data['x'].to_numpy()
    
    def get_y(self) -> np.ndarray:
        return self.data['y'].to_numpy()