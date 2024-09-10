from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QHBoxLayout
from source.config import CONFIG


class DetailsListItem(QtWidgets.QWidget):


    # def sizeHint(self):
    #     base_width = self.label2.width()+self.label1.width()
    #     return PySide6.QtCore.QSize(50, 50)
    #     if self.expanded:
    #         pass

    def __init__(self, label_name, display_text, parent=None):
        super().__init__(parent)
        # 2 Lables on Horizontal Layout
        self.label1 = QLabel(label_name)
        self.label2 = QLabel(display_text)
        self.L_Layout = QHBoxLayout()
        self.R_Layout = QHBoxLayout()
        self.M_layout = QHBoxLayout()
        self.setMaximumHeight(50)
        self.setMaximumWidth(400)
        #self.setBaseSize(100, 60)
        font =CONFIG.list_font
        font.setBold(True)

        #self.label1.setAlignment(QtCore.Qt.AlignLeft)
        #self.label2.setAlignment(QtCore.Qt.AlignRight)
        #self.R_Layout.setAlignment(QtCore.Qt.AlignRight)
        #self.L_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.label1.setFont(font)
        self.label2.setFont(font)
        #self.M_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.L_Layout.addWidget(self.label1)
        self.R_Layout.addWidget(self.label2)

        self.M_layout.addLayout(self.L_Layout)
        self.M_layout.addLayout(self.R_Layout)
        self.setLayout(self.M_layout)
        #self.setupUi()
        #self.setContentsMargins(1, 1, 1, 1)

    def setupUi(self):
        # self.setWindowTitle("Threaded Progress")
        # self.resize(600, 60)
        pass
        #self.setContentsMargins(20, 20, 20, 20)
        # self.setStyleSheet("padding: 20px;")
        #self.show()
