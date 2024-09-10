from PySide6 import QtWidgets, QtCore


class TripleButtonX(QtWidgets.QWidget):
    onChangeSignal = QtCore.Signal(object)

    def Value(self):
        if not self.LeftBtn.isEnabled():
            return -1
        elif not self.RightBtn.isEnabled():
            return 1
        elif not self.MiddleBtn.isEnabled():
            return 0


    def IniUI(self):
        self.LeftBtn.setEnabled(True)
        self.MiddleBtn.setEnabled(True)
        self.RightBtn.setEnabled(False)
    def CancelMiddleButton(self):
        self.MiddleBtn.setEnabled(True)
        self.MiddleBtn.setVisible(False)


    def __init__(self, left, middle, right, parent=None):
        super().__init__(parent)
        self.LeftBtn = QtWidgets.QPushButton(left)
        self.LeftBtn.setStyleSheet("""color: #c7183b;""")
        self.MiddleBtn = QtWidgets.QPushButton(middle)
        self.RightBtn = QtWidgets.QPushButton(right)

        self.IniUI()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.LeftBtn)
        self.layout.addWidget(self.MiddleBtn)
        self.layout.addWidget(self.RightBtn)
        self.setLayout(self.layout)

        self.LeftBtn.clicked.connect(self.LeftClicked)
        self.MiddleBtn.clicked.connect(self.MiddleClicked)
        self.RightBtn.clicked.connect(self.RightClicked)

    def LeftClicked(self):
        self.LeftBtn.setEnabled(False)
        self.LeftBtn.setStyleSheet("""color: #700d21;""")
        self.MiddleBtn.setEnabled(True)
        self.RightBtn.setEnabled(True)
        print("left clicked")

    def MiddleClicked(self):
        self.RightBtn.setEnabled(True)
        self.MiddleBtn.setEnabled(False)
        self.LeftBtn.setEnabled(True)
        self.LeftBtn.setStyleSheet("""color: #c7183b;""")
        print("middle clicked")

    def RightClicked(self):
        self.RightBtn.setEnabled(False)
        self.MiddleBtn.setEnabled(True)
        self.LeftBtn.setEnabled(True)
        self.LeftBtn.setStyleSheet("""color: #c7183b;""")
