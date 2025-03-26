import matplotlib.pyplot as plt
import numpy as np

from src.helpers import check_directory

PATH_FIGURES = 'figures/'

class SimpleScatter:
    '''
    A basic scatter plot.

    Contains, fig, ax, and scat objects.
    '''
    __slots__ = ('fig', 
                 'ax', 
                 'scat'
                 )
    
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi = 100)
        self.scat = self.ax.scatter([],[], s=10)

        self.check_directories()
        return
    
    def check_directories(self) -> None:
        '''
        Ensure any required directores exist
        '''
        check_directory(PATH_FIGURES)
        return None
    
    def save_plot(self, file_name: str) -> None:
        '''
        Save the currently displayed figure as a .png file.
        '''
        if file_name != '':
            print(f'Saving: {file_name}.png')
            self.fig.savefig(f'{file_name}.png', bbox_inches='tight')
        return None
    
    def update_scatter(self, scatter_data: np.ndarray) -> None:
        '''
        Updates the data in the scatter plot.

        scatter_data should be of size (N, 2)
        '''
        xdata = scatter_data[:, 0]
        ydata = scatter_data[:, 1]

        self.scat.set_offsets(scatter_data)
        self.ax.set_xlim([min(xdata)-1,
                          max(xdata)+1
                          ])
        self.ax.set_ylim([min(ydata)-1,
                          max(ydata)+1
                          ])
        return None