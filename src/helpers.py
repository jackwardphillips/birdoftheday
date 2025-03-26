import numpy as np
import time
from datetime import datetime as dt
from typing import Callable

PATH_DATA = 'data'

DEBUG = False
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

SEQUENCES = np.array([0, 0, 0], 
                        [1, 0, 0], 
                        [0, 1, 0], 
                        [0, 0, 1], 
                        [1, 1, 0], 
                        [1, 0, 1], 
                        [0, 1, 1],
                        [1, 1, 1]
                     )

CARD_SEQUENCES = np.array(['R R R',
                           'B R R',
                           'R B R',
                           'R R B',
                           'B B R',
                           'B R B',
                           'R B B',
                           'B B B'
                     ])