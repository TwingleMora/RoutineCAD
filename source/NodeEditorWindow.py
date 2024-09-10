from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from source.config import CONFIG


class NodeEditorWindow(QtWidgets.QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        """
        Initializes the NodeWidget object.
    
        Args:
            parent (QWidget): The parentItem widget.
        """
        super().__init__(parent)

        self.setMinimumSize(400, 400)
        self.setWindowTitle("Modify Node")
        # self.setFont(QtGui.QFont("Lucida Sans Unicode", pointSize=8))
        # self.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont("Lucida Sans Unicode", pointSize=8)

        label_name = QtWidgets.QLabel("Name:        ")
        self.edit_name = QtWidgets.QLineEdit()
        label_description = QtWidgets.QLabel("Description: ")
        self.edit_description = QtWidgets.QLineEdit()
        label_text = QtWidgets.QLabel("Text:        ")

        label_target = QtWidgets.QLabel("Target:        ")
        self.edit_target = QtWidgets.QLineEdit()

        self.edit_text = QtWidgets.QPlainTextEdit()
        self.edit_name.setFont(font)
        self.edit_description.setFont(font)
        self.edit_target.setFont(font)

        self.edit_name.setText(node.title_text)
        self.edit_description.setText(node.type_text)
        # edit_text.setText()
        self.edit_text.setMaximumHeight(self.height() // 5)
        self.edit_text.setPlainText(node.text)
        label_name.setFont(font)
        label_description.setFont(font)
        label_text.setFont(font)
        label_target.setFont(font)

        self.upgrade_btn = QtWidgets.QPushButton("Upgrade")
        self.upgrade_btn.setCheckable(True)

        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()
        h_layout4 = QHBoxLayout()
        h_layout5 = QHBoxLayout()

        h_layout1.addWidget(label_name)
        h_layout1.addWidget(self.edit_name)

        h_layout2.addWidget(label_description)
        h_layout2.addWidget(self.edit_description)

        h_layout3.addWidget(label_text)
        h_layout3.addWidget(self.edit_text)

        h_layout4.addWidget(label_target)
        h_layout4.addWidget(self.edit_target)
        #h_layout4.addWidget(self.upgrade_btn)

        btn_cancel = QPushButton("Cancel")
        btn_apply = QPushButton("Apply")
        btn_cancel.clicked.connect(lambda: self.close())

        self.target_upgrade_number = self.node.target_iteration
        self.current_upgrade_number = self.node.current_iteration

        btn_apply.clicked.connect(self.apply_modifications_nested_func)

        h_layout5.addWidget(btn_cancel)
        h_layout5.addWidget(btn_apply)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(h_layout3)
        v_layout.addLayout(h_layout4)
        v_layout.addLayout(h_layout5)
        self.setLayout(v_layout)


    def apply_modifications_nested_func(self):
        self.current_upgrade_number = self.node.current_iteration
        self.target_upgrade_number = self.node.target_iteration
        if CONFIG.is_number(self.edit_target.text()):
            self.target_iteration_number = int(self.edit_target.text())
        else:
            self.target_iteration_number = self.node.target_iteration

        #if self.upgrade_btn.isChecked():
        if self.target_iteration_number > self.node.target_iteration:
            self.target_upgrade_number = self.target_iteration_number
            self.current_upgrade_number=0
        else:
            self.target_upgrade_number = self.node.target_iteration
        # else:
        #     self.target_upgrade_number = self.node.target_iteration
        self.node.modify(self.edit_name.text(), self.edit_description.text(), self.edit_text.toPlainText(),current_iteration=self.current_upgrade_number,target_iteration=self.target_upgrade_number)
        self.close()

