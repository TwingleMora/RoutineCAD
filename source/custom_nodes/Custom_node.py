from PySide6 import QtWidgets, QtCore

from source.node_editor.node import Node
from source.custom_nodes.common_widgets import FloatLabel
from source.config import CONFIG


class Custom_Node(Node):
    def __init__(self, Name, Description="", text="", Id=None, current_iteration=0, target_iteration=10):
        super().__init__()
        self.label_current_iteration = QtWidgets.QLabel()
        self.label_target_iteration =  QtWidgets.QLabel()
        self.progress_bar = QtWidgets.QProgressBar()
        self.scaler_label = FloatLabel("")
        self.finished = QtWidgets.QCheckBox()
        self.Id = Id
        self.title_text = Name
        self.type_text = Description
        self.text = text

        self.current_iteration:int = current_iteration
        self.last_iteration:int = current_iteration
        self.target_iteration:int = target_iteration



        self.set_color(title_color=(128, 0, 0))
        self.add_pin(name="I1", is_output=False)
        self.add_pin(name="I2", is_output=False)
        self.add_pin(name="I3", is_output=False)

        self.add_pin(name="O1", is_output=True)
        self.add_pin(name="O2", is_output=True)
        self.add_pin(name="O3", is_output=True)


        self.build()

        percent = (self.current_iteration / self.target_iteration) * 100.0
        self.progress_bar.setValue(percent)

    def modify(self, Name, Description, text="", current_iteration=0, target_iteration=10):
        # self.delete()
        # self = Custom_Node()
        #self.minimum_width = self._width

        self.title_text = Name
        self.type_text = Description
        self.text = text
        self.current_iteration = current_iteration
        if target_iteration > 0:
            self.target_iteration = target_iteration
        else:
            self.target_iteration = self.current_iteration
        self.last_iteration = current_iteration
        self.finished.setChecked(False)
        #self.set_color(title_color=(255, 165, 0))
        #self.add_pin(name="i", is_output=False)
        #self.add_pin(name="o", is_output=True)
        self.build()

        percent = (self.current_iteration / self.target_iteration) * 100.0
        self.progress_bar.setValue(percent)

    def init_widget(self):
        #maximum iterations
        if self.widget:
            self.widget.deleteLater()
        self.widget = QtWidgets.QWidget()
        self.widget.setMinimumWidth(450)
        #self.widget.setContentsMargins(10,0,10,0)
        layout = QtWidgets.QVBoxLayout()

        #layout.setContentsMargins(3, 0, 3, 0)
        #self.scaler_line = FloatLineEdit()
        font1 = CONFIG.node_text_font
        font2 = CONFIG.node_labels_font
        font3 = CONFIG.node_checkbox_font
        self.scaler_label = FloatLabel(self.text)
        self.scaler_label.setFont(font1)
        self.progress_bar = QtWidgets.QProgressBar()
        hBoxLayout = QtWidgets.QGridLayout()
        self.label_current_iteration = QtWidgets.QLabel(str(int(self.current_iteration)))
        self.label_current_iteration.setAlignment(QtCore.Qt.AlignCenter)

        seperation = QtWidgets.QLabel("/")
        seperation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_target_iteration = QtWidgets.QLabel(str(int(self.target_iteration)))
        self.label_target_iteration.setAlignment(QtCore.Qt.AlignCenter)

        self.finished = QtWidgets.QCheckBox("Finished")
        self.finished.checkStateChanged.connect(self.finished_changed)

        self.label_current_iteration.setFont(font2)
        self.label_target_iteration.setFont(font2)
        self.finished.setFont(font2)
        self.finished.setStyleSheet(CONFIG.check_box_style)
        seperation.setFont(font2)

        self.finished.setFont(font3)

        hprogresslayout = QtWidgets.QGridLayout()

        hBoxLayout.addWidget(self.label_current_iteration, 0, 0, 1, 1)
        hBoxLayout.addWidget(seperation, 0, 1, 1, 1)
        hBoxLayout.addWidget(self.label_target_iteration, 0, 2, 1, 1)
        hBoxLayout.addWidget(self.finished, 1, 0, 1, 3)
        hprogresslayout.addWidget(self.scaler_label, 0, 1, 1, 4)
        hprogresslayout.addWidget(self.progress_bar, 2, 1, 1, 4)
        hprogresslayout.setSpacing(100)

        self.progress_bar.setMaximumHeight(20)
        self.progress_bar.setStyleSheet(CONFIG.progress_bar_style)
        self.progress_bar.setFormat("")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout.addLayout(hprogresslayout)
        layout.addLayout(hBoxLayout)
        self.widget.setLayout(layout)
        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)



        super().init_widget()

    def finished_changed(self, state):

        if state == QtCore.Qt.Checked:
            if self.current_iteration < self.target_iteration:
                self.label_current_iteration.setText(str(self.last_iteration + 1))

        else:
            self.label_current_iteration.setText(str(self.last_iteration))

        self.current_iteration = float(self.label_current_iteration.text())
        self.target_iteration = float(self.label_target_iteration.text())
        percent:float = (self.current_iteration / self.target_iteration) * 100.0


        self.progress_bar.setValue(percent)
        print("finished clicked")
