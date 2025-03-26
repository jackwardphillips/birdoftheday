from PyQt5 import QtWidgets as qtw
import sys

from src.qtcomponents import WindowWithVerticalSlots, InputPopup

# Your application will contain exactly one instance
# of a QApplication object (or derived subclass)
class SayHelloApp(qtw.QApplication):
    '''
    Contains a VerticalHelloBox to
    prompt the user for their name and
    say hello!
    '''
    def __init__(self):
        # Call the constructor for the parent class
        # The one required argument is usually sys.argv
        # which are command line parameters. We don't need
        # any now, hence the empty list.
        super().__init__([])

        # Add the VerticalHelloBox
        self.main_widget = VerticalHelloBox()

        # Run the application
        self.main_widget.show()
        sys.exit(self.exec_())
        return
    
class VerticalHelloBox(WindowWithVerticalSlots):
    '''
    Contains a textbox and a button the user can press
    which opens up another window for them to them to enter
    their name.
    '''
    def __init__(self):
        super().__init__(title='Example Interface using PyQt5')
        self.configure()
        return

    def configure(self) -> None:
        self.greeting_box = qtw.QLabel(self)
        self.hello_button = qtw.QPushButton('Who are you?', self)

        # Bind the button to a function, so that when the button is pressed
        # the function is called.
        self.hello_button.clicked.connect(self.hello_button_clicked)
        
        # Add the two objects to the layout
        self.my_layout.addWidget(self.greeting_box)
        self.my_layout.addWidget(self.hello_button)
        return None
    
    def hello_button_clicked(self) -> None:
        # Create a new InputPopup
        name_getter = InputPopup('Your name:')

        # Run the dialog box and wait for the user to click the button
        if name_getter.exec_() == qtw.QDialog.Accepted:
            # Set the text in the main window to whatever the user input
            self.greeting_box.setText(f'Hello {name_getter.get_text()}!')
        return None