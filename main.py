"""
A simple Node Editor application that allows the user to create, modify and connect nodes of various types.

The application consists of a main window that contains a splitter with a Node List and a Node Widget. The Node List
shows a list of available node types, while the Node Widget is where the user can create, edit and connect nodes.

This application uses PySide6 as a GUI toolkit.

Author: Bryan Howard
Repo: https://github.com/bhowiebkr/simple-node-editor
"""
from datetime import datetime
import json
import logging
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from source.RoutineEditor import RoutineEditor
from source.RoutineEditor import NodeEditorMode
from source.config import CONFIG
from source.routine import Routine

from source.routine_list import RoutineList

import icons

logging.basicConfig(level=logging.DEBUG)

from source.database.routine_db import RoutineDB


class MainMenu(QtWidgets.QWidget):
    NoOfActiveRoutines = 0
    NoOfAllRoutines = 0
    TotalEXP = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn = None
        self.cursor = None
        self.setMinimumSize(QtCore.QSize(600, 400))
        self.launcher = None
        self.setWindowTitle("RoutineCAD")

        CONFIG.load_notification_icon()

        self.rsql = RoutineDB()
        ###################################
        ############ WIDGETS ##############
        ###################################
        self.routine_list = RoutineList(self)
        self.routine_list.UpdateMainRoutineListSignal.connect(self.update_widgets)
        #####################################
        ###########  MAIN LIST ##############
        #####################################

        #       self.routine_list.setSpacing(10)
        #        self.routine_list.autoFillBackground(True)
        btn_add_routine = QPushButton("Add Routine")
        btn_cancel = QPushButton("Cancel")

        ###################################
        ############ SIGNALS ##############
        ###################################

        ################################
        ######### CREATE TABLE #########
        ################################
        #self.create_table(self.table_name)
        self.rsql.create_table()
        ###############################
        ######### CLEAR TABLE #########
        ###############################
        #self.rsql.clear()

        # json_files = []
        #
        # json_file1 = (Path(__file__).parent.resolve() / 'Example_project/ee.json')
        # json_file2 = (Path(__file__).parent.resolve() / 'Example_project/xx.json')
        # json_file3 = (Path(__file__).parent.resolve() / 'Example_project/vv.json')
        # json_files.append(json_file1)
        # json_files.append(json_file2)
        # json_files.append(json_file3)
        # self.json_datas = []
        # for json_file in json_files:
        #     if json_file:
        #         json_path = Path(json_file)
        #         if json_path.exists():  # and json_path.is_dir():
        #             # self.json_path = json_path
        #             with open(json_path) as f:
        #                 json_data = json.load(f)
        #                 self.json_datas.append(json_data)

        ### Test Insert
        # datetime is object
        # current = datetime.now()

        # for i in range(3):
        #     final = current + timedelta(seconds=4)
        #     routine = Routine(routine_id=i, routine_name="name" + str(i), data=json.dumps(self.json_datas[i]),
        #                       active_state=True,start_time=current,end_time=final,iterations=0,weight=1)
        #     self.rsql.insert(routine)

        top_layout = QGridLayout()
        #top_layout.setC.setColumnCount(3)  # Set the number of columns to 3

        self.routine_list.create_list()
        self.routine_list.update_list()

        ###########################LEFT SIDE##################################
        LEFT_LAYOUT1 = QHBoxLayout()
        LEFT_LAYOUT2 = QHBoxLayout()
        label_No_Of_Active_Routines = QtWidgets.QLabel("Active Routines:")
        self.display_No_Of_Active_Routines = QtWidgets.QLabel()

        label_EXP = QtWidgets.QLabel("Exp:")
        self.TotalEXP = self.rsql.get_total_exp()
        str_exp = "%0.2f" % self.TotalEXP
        self.display_EXP = QtWidgets.QLabel(str_exp)

        # font
        label_No_Of_Active_Routines.setFont(CONFIG.list_font)
        self.display_No_Of_Active_Routines.setFont(CONFIG.list_font)
        label_EXP.setFont(CONFIG.list_font)
        self.display_EXP.setFont(CONFIG.list_font)

        LEFT_LAYOUT1.addWidget(label_No_Of_Active_Routines)
        LEFT_LAYOUT1.addWidget(self.display_No_Of_Active_Routines)

        LEFT_LAYOUT2.addWidget(label_EXP)
        LEFT_LAYOUT2.addWidget(self.display_EXP)

        ###########################RIGHT SIDE##################################
        RIGHT_LAYOUT1 = QHBoxLayout()
        RIGHT_LAYOUT2 = QHBoxLayout()
        label_No_Of_All_Routines = QtWidgets.QLabel("All Routines:")
        self.display_No_Of_All_Routines = QtWidgets.QLabel()

        label_HR = QtWidgets.QLabel("HR:")
        self.display_HR = QtWidgets.QLabel()

        # font
        label_No_Of_All_Routines.setFont(CONFIG.list_font)
        self.display_No_Of_All_Routines.setFont(CONFIG.list_font)
        label_HR.setFont(CONFIG.list_font)
        self.display_HR.setFont(CONFIG.list_font)

        NoOfActiveRoutines = self.rsql.number_of_active_routines()
        NoOfAllRoutines = self.rsql.number_of_all_routines()
        self.NoOfActiveRoutines = NoOfActiveRoutines
        self.NoOfAllRoutines = NoOfAllRoutines

        self.display_No_Of_All_Routines.setText(str(self.NoOfAllRoutines))
        self.display_No_Of_Active_Routines.setText(str(self.NoOfActiveRoutines))

        RIGHT_LAYOUT1.addWidget(label_No_Of_All_Routines)
        RIGHT_LAYOUT1.addWidget(self.display_No_Of_All_Routines)

        RIGHT_LAYOUT2.addWidget(label_HR)
        RIGHT_LAYOUT2.addWidget(self.display_HR)

        top_layout.addLayout(LEFT_LAYOUT1, 0, 0)
        top_layout.addLayout(LEFT_LAYOUT2, 1, 0)
        top_layout.addLayout(RIGHT_LAYOUT1, 0, 2)

        ###########################################################
        btn_add_routine.clicked.connect(self.add_routine_clicked)
        btn_cancel.clicked.connect(lambda: self.close())

        button_layout = QVBoxLayout()
        button_layout.addLayout(top_layout)
        button_layout.addWidget(self.routine_list)
        button_layout.addWidget(btn_add_routine)
        button_layout.addWidget(btn_cancel)
        self.setLayout(button_layout)

    def add_routine_clicked(self):
        new_id = self.rsql.calculate_new_routine_id()
        self.launcher = RoutineEditor(
            routine=Routine(routine_id=new_id, iterations=0, weight=1, start_time=datetime.now(),
                            end_time=datetime.now()), EditorMode=NodeEditorMode.New)
        self.launcher.show()
        self.launcher.New_Signal.connect(self.NewRoutineClicked)

    #        self.launcher.UpdateMainRoutineListSignal.connect(self.update_widgets)

    def NewRoutineClicked(self, routine):
        self.routine_list.add_item_to_list(routine)
        self.update_widgets()

    def update_widgets(self, x=0):
        self.NoOfActiveRoutines = self.rsql.number_of_active_routines()
        self.NoOfAllRoutines = self.rsql.number_of_all_routines()
        self.TotalEXP = self.rsql.get_total_exp()

        str_exp = "%0.2f" % self.TotalEXP
        self.display_EXP.setText(str_exp)

        self.display_No_Of_All_Routines.setText(str(self.NoOfAllRoutines))
        self.display_No_Of_Active_Routines.setText(str(self.NoOfActiveRoutines))
        self.display_EXP = QtWidgets.QLabel(str_exp)


if __name__ == "__main__":
    import sys
    import qdarktheme

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/Portfolio_X/Apps/UnderDevelopment/Course/Point1/Point1/app.ico'))
    qdarktheme.setup_theme()
    window = MainMenu()
    window.show()

    app.exec()
    sys.exit()
