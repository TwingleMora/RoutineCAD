from PySide6 import QtWidgets, QtCore


class ToggleButtonX(QtWidgets.QWidget):
    onChangeSignal = QtCore.Signal(object)
    def IsChecked(self):
        return self.LeftBtn.isEnabled()

    def IniUI(self):
        self.RightBtn.setEnabled(False)
        self.LeftBtn.setEnabled(True)
    def __init__(self, left,right, parent=None):
        super().__init__(parent)
        self.LeftBtn  = QtWidgets.QPushButton(left)
        self.LeftBtn.setStyleSheet("""color: #c7183b;""")

        self.RightBtn = QtWidgets.QPushButton(right)

        self.IniUI()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.LeftBtn)
        self.layout.addWidget(self.RightBtn)
        self.setLayout(self.layout)

        self.LeftBtn.clicked.connect(self.LeftClicked)
        self.RightBtn.clicked.connect(self.RightClicked)

    def LeftClicked(self):
        self.LeftBtn.setEnabled(False)
        self.LeftBtn.setStyleSheet("""color: #700d21;""")
        self.RightBtn.setEnabled(True)
        print("left clicked")
        self.onChangeSignal.emit(False)

    def RightClicked(self):
        self.RightBtn.setEnabled(False)
        self.LeftBtn.setEnabled(True)
        self.LeftBtn.setStyleSheet("""color: #c7183b;""")

        print("right clicked")
        self.onChangeSignal.emit(True)