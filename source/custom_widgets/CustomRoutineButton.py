from PySide6 import QtWidgets


class CustomRoutineButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

