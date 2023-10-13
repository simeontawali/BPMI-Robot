"""
BPMI Robotic Annular Pipe Sanitization System
File Name: gui_tkinter.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: gui code for PyQt implementation
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: 
    Initial structure and research

Dependencies:
    PyQt6 Installation

References:
    https://wiki.python.org/moin/PyQt
    https://pypi.org/project/PyQt6/
    https://realpython.com/python-pyqt-gui-calculator/#getting-to-know-pyqt
    https://www.pythonguis.com/pyqt6-tutorial/

Additional Notes:
    python -m pip install pyqt6

"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QDockWidget, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QColor

class operator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BPMI Robotics")
        self.setGeometry(100, 100, 800, 600)  # Adjust the dimensions as needed

        self.central_widget = QMainWindow()

        # Create a QTextEdit widget
        self.error_terminal = QTextEdit()
        self.error_terminal.setReadOnly(True)

        # Create a QDockWidget and set its features
        dock = QDockWidget("Terminal", self)
        dock.setWidget(self.error_terminal)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        self.show()


        # Function to show error messages
        def error_write(message):
            cursor = self.error_terminal.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.insertText(message)
            cursor.insertBlock()
            char_format = QTextCursor().charFormat()
            char_format.setForeground(QColor("red"))
            cursor.mergeCharFormat(char_format)
            # print(message, file=sys.stderr)

        # Test the error message function
        error_write("Sample error message.")

        # Function to write text to the terminal
        def terminal_write(text):
            cursor = self.error_terminal.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.insertText(text)
            cursor.insertBlock()

        # Example of writing text to the terminal
        terminal_write("This text is written to the terminal.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = operator()
    sys.exit(app.exec())
