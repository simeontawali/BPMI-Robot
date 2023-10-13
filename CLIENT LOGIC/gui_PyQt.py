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
# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

# 2. Create an instance of QApplication
app = QApplication([])

# 3. Create your application's GUI
window = QWidget()
window.setWindowTitle("BPMI Robot")
# window.setGeometry(100, 100, 280, 80)


# 4. Show your application's GUI
window.show()

# 5. Run your application's event loop
sys.exit(app.exec())