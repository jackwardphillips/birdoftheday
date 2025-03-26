# All the code needed to define interface components

# Widgets are all sorts of interface components
from PyQt5 import QtWidgets as qtw

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from typing import Callable

class WindowWithVerticalSlots(qtw.QWidget):
    '''
    A window with a title and an empty
    vertical container (QVBoxLayout).

    Intended use of this class is to inherit
    and extend.
    '''
    def __init__(self, title: str):
        super().__init__()

        # Set the window title
        self.setWindowTitle(title)

        # Create an empty vertical layout container
        self.my_layout = qtw.QVBoxLayout(self)
        return
    
class WindowWithFigureAbove(WindowWithVerticalSlots):
    '''
    A window with a vertical layout and matplotlib figure above.
    '''
    def __init__(self,
                 fig: plt.Figure,
                 title: str = 'Window with a Figure'
                 ):
        super().__init__(title=title)

        # Put the figure into a canvas
        self.canvas = FigureCanvasQTAgg(fig)
        # Add that to the layout
        self.my_layout.addWidget(self.canvas)
        return

class ButtonRow(qtw.QHBoxLayout):
    '''
    A row of buttons. Names must be provided for each button.
    '''
    def __init__(self,
                 names: list[str]
                 ):
        super().__init__()
        
        self.buttons = []
        for name in names:
            self.buttons.append(qtw.QPushButton(name))
            self.addWidget(self.buttons[-1])
        return
    
class ButtonBox(qtw.QVBoxLayout):
    '''
    A vertical container of ButtonRow objects.
    Specify nrows and ncols when creating.
    '''
    def __init__(self,
                 nrows: int,
                 ncols: int
                 ):
        super().__init__()

        self.rows = []
        for _ in range(nrows):
            names = [str(n) for n in range(ncols)]
            self.rows.append(ButtonRow(names))
            self.addLayout(self.rows[-1])
        return

def configure_button(button: qtw.QPushButton,
                     text: str,
                     command: Callable
                     ) -> None:
    button.setText(text)
    button.clicked.connect(command)
    return None

class InputPopup(qtw.QDialog):
    '''
    A popup window with a text box and an OK button
    to allow the user to enter freeform text.
    '''

    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)

        # Place to enter some text
        self.text_entry = qtw.QLineEdit(self)

        # OK button to click
        self.ok_button = qtw.QPushButton('Ok', self)

        # When the button is clicked, it calls the accept() method
        # of the QDialog, which lets the application know that 
        # the interaction with the dialog is complete.
        self.ok_button.clicked.connect(self.accept)

        # Create a vertical layout and add the widgets
        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.text_entry)
        self.my_layout.addWidget(self.ok_button)
        return

    def get_text(self) -> str:
        return self.text_entry.text()