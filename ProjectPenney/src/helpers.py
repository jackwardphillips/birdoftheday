import numpy as np
import time
from datetime import datetime as dt
from typing import Callable

PATH_DATA = 'data'

# if DEBUG is set to true, debugger_factory will print arguments
DEBUG = False
# if TIMER is set to true, debugger_factory will print the execution time
TIMER = True

def debugger_factory() -> Callable:
    def debugger(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            wrapper.last_execution_time = 0
            if DEBUG:
                print(f'{func.__name__} was called with:')
                print('Positional arguments:', args)
                print('Keyword arguments:', kwargs)

            if TIMER:
                t0 = dt.now()
                results = func(*args, **kwargs)
                wrapper.last_execution_time = (dt.now() - t0).total_seconds()
                print(f'{func.__name__} ran for {wrapper.last_execution_time} seconds.')
                return results
            else:
                return func
        return wrapper
    return debugger

# sequences that the game function can understand
SEQUENCES = np.array(['000',
                      '100',
                      '010',
                      '001',
                      '110',
                      '101',
                      '011',
                      '111'])

# sequences that the user will be able to interpret
CARD_SEQUENCES = np.array(['R R R',
                           'B R R',
                           'R B R',
                           'R R B',
                           'B B R',
                           'B R B',
                           'R B B',
                           'B B B'
                     ])