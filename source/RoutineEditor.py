import datetime
import json
import logging
from pathlib import Path

import shiboken6.Shiboken
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QMessageBox
from shiboken6 import Shiboken

from source.custom_widgets.CustomRoutineButton import CustomRoutineButton
from source.custom_widgets.ToggleButtonX import ToggleButtonX
from source.custom_widgets.TripleButtonX import TripleButtonX
from source.database.routine_db import RoutineDB
from source.node_data.SceneHandler import SceneHandler
from source.node_editor.gui.node_list import NodeList
from source.node_editor.gui.node_widget import NodeWidget
from source.node_editor.node import Node
from source.routine import Routine
from source.custom_nodes.Custom_node import Custom_Node
from source.NodeEditorWindow import NodeEditorWindow
from enum import Enum

logging.basicConfig(level=logging.DEBUG)
from source.modify_weight_window import WeightWindow
from shiboken6.Shiboken import isValid

from source.custom_widgets.DetailsList import DetailsList


class NodeEditorMode(Enum):
    New = 0
    Edit = 1


class RoutineEditor(QtWidgets.QMainWindow):
    clicked_on_finished = False

    #########################################
    ########### MAIN MENU SIGNALS ###########
    ###########                   ###########
    #########################################
    ################# FOR EXAMPLE IF USER REMOVED A ROUTINE ##############

    ################ TO UPDATE NO OF ACTIVE ROUTINES ################

    ######## UPDATE PROJECT
    ###############################
    ############## 1 ##############
    ###############################

    Update_Signal = QtCore.Signal(Path)
    New_Signal = QtCore.Signal(Path)

    ######## UPDATE PROJECT
    #################################
    ############# 2 #################
    #################################
    #print("Drop Okay!")
    # node = e.mimeData().item.class_name  #object has attribute called 'item'
    # self.request_node.emit(node())
    routine: Routine = None

    Checked = False

    def OnTimeUp(self, value):
        if not self.Checked:
            self.Checked = True
            print("time is up in editooooooor")
            self.UpdateTerMFinished()
            self.UpdateToggleButton(self.InitialFinishedState)
            self.routine.finished = True

    ToggleButtonXValue = False

    def UpdateToggleButton(self, finished=None):
        self.MissedMadeBtn.setVisible(False)
        self.MissedMadeBtn.setEnabled(False)
        if not self.InProgress():
            if not self.routine.finished:
                self.MissedMadeBtn.setVisible(True)
                self.MissedMadeBtn.setEnabled(True)

    def UpdateTerMFinished(self):
        if not self.routine.active_state:
            self.TerMFinshedBtn.setEnabled(False)
            self.TerMFinshedBtn.setVisible(False)
        else:
            if self.routine.finished:
                self.TerMFinshedBtn.setEnabled(True)
                self.TerMFinshedBtn.setVisible(True)
                self.TerMFinshedBtn.CancelMiddleButton()
            else:
                if (self.InProgress()):
                    self.TerMFinshedBtn.setEnabled(True)
                    self.TerMFinshedBtn.setVisible(True)
                else:
                    self.TerMFinshedBtn.setEnabled(False)
                    self.TerMFinshedBtn.setVisible(False)

    def SetUpMenuBar(self):
        #icon = QtGui.QIcon("resources/app.ico")
        #self.setWindowIcon(icon)

        self.setWindowTitle("Routine Editor")
        self.settings = QtCore.QSettings("node-editor", "RoutineEditor")

        # create a "File" menu and add an "Export CSV" action to it
        file_menu = QtWidgets.QMenu("File", self)
        self.menuBar().addMenu(file_menu)

        load_action = QtGui.QAction("Load Project", self)
        load_action.triggered.connect(self.get_project_path)
        file_menu.addAction(load_action)

        save_action = QtGui.QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

    def SetupTopUI(self):
        self.Routine_Id_Label = QLabel("Routine ID: ")
        self.Routine_Id_Display = QtWidgets.QLabel(str(self.routine.routine_id))

        self.Routine_Name_Label = QLabel("Routine Name: ")
        self.Routine_Name_Edit = QtWidgets.QLineEdit()
        self.Routine_Name_Edit.setText(self.routine.routine_name)
        self.Routine_State_Label = QLabel("Routine State: ")

    def __init__(self, routine: Routine = None, JSONData=None, EditorMode: NodeEditorMode = NodeEditorMode.Edit,
                 parent=None):

        super().__init__(parent)
        self.routine = Routine()
        self.routine.copy(routine)
        self.editorMode = EditorMode
        self.json_data = JSONData
        self.InitialFinishedState = self.routine.finished
        ### New Windows Handler
        self.new_window: QtWidgets.QWidget = None

        ### SQL
        self.rsql = RoutineDB()

        ### I Dont know what this is
        self.settings = None

        #self.project_path = None
        #self.imports = None

        ####XXXX
        self.SetupTopUI()
        ####XXXX
        self.SetUpMenuBar()

        # Layouts
        main_layout = QtWidgets.QHBoxLayout()
        left_layout = QtWidgets.QVBoxLayout()

        #layout settings
        ## main

        ## left
        left_layout.setContentsMargins(0, 0, 0, 0)

        #widgets
        ### main
        main_widget = QtWidgets.QWidget()

        ### left
        left_widget = QtWidgets.QWidget()

        ### spliter
        self.splitter = QtWidgets.QSplitter()

        #widgets settings
        ### main
        main_widget.setLayout(main_layout)

        ###left
        left_widget.setLayout(left_layout)

        ###splitter

        ### Main Window Settings
        self.setCentralWidget(main_widget)

        ### main widgets definitions settings
        ###main
        #########NodeWidget
        self.node_widget = NodeWidget(self)
        self.node_widget.node_editor.modify_node.connect(self.OpenNodeEditor)

        ####XXXX
        self.sceneHandler = SceneHandler(self.node_widget.scene)
        ####XXXX
        ########splitter
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(self.node_widget)

        ### other widgets definitions

        #left
        self.node_list = NodeList(self)  # NodeList(parentItem)
        self.details_list = DetailsList()
        self.Routine_State_CheckBox = QtWidgets.QCheckBox()
        self.modify_weight = QPushButton("Modify Weight")
        self.add_point = QPushButton("Add Point")
        self.finish_routine = CustomRoutineButton("Finish Routine")
        self.create_apply = QPushButton("")
        self.MissedMadeBtn = ToggleButtonX("Missed", "Made", self)
        self.TerminateBtn = QtWidgets.QPushButton("Terminate")
        self.TerMFinshedBtn = TripleButtonX("Terminated", "Finished", "None", self)
        self.CancelButton = QPushButton("Cancel")
        #Terminate => -1
        #Finish => 0
        #Cancel
        self.CancelButton.clicked.connect(self.close)

        #node list
        self.node_list.modify_node.connect(self.OpenNodeEditor)

        #TerminateBtn
        self.TerminateBtn.setCheckable(True)

        self.TerminateBtn.clicked.connect(self.clicked_terminate_func)

        #routine state checkbox
        active = QtCore.Qt.CheckState.Checked if self.routine.active_state else QtCore.Qt.CheckState.Unchecked
        self.Routine_State_CheckBox.setCheckState(active)
        self.Routine_State_CheckBox.setEnabled(not self.routine.finished)
        self.Routine_State_CheckBox.checkStateChanged.connect(self.toggle_active)
        #add point button
        self.add_point.clicked.connect(self.clicked_add_point)

        ####################################################
        ####################################################
        #TerMFinshedBtn
        if (self.editorMode == NodeEditorMode.New):
            self.TerMFinshedBtn.setEnabled(False)
            self.TerMFinshedBtn.setVisible(False)
        elif (self.editorMode == NodeEditorMode.Edit):
            self.UpdateTerMFinished()

        #MissedMadeBtn
        self.MissedMadeBtn.onChangeSignal.connect(self.pressedOnToggleButton)
        self.ToggleButtonXValue = False
        if (self.editorMode == NodeEditorMode.New):
            self.MissedMadeBtn.setEnabled(False)
            self.MissedMadeBtn.setVisible(False)
        elif (self.editorMode == NodeEditorMode.Edit):
            self.UpdateToggleButton()

        ####################################################
        ####################################################

        #create / modify routine button
        if (self.editorMode == NodeEditorMode.New):
            self.create_apply.setText("Create")
        elif (self.editorMode == NodeEditorMode.Edit):
            self.create_apply.setText("Modify")
        self.create_apply.clicked.connect(self.clicked_create_modifiy_func)

        #modify weight button
        self.modify_weight.clicked.connect(self.clicked_modify_weight)

        #Left Layouts Settings
        Left_Top_LayoutH1 = QHBoxLayout()
        Left_Top_LayoutH2 = QHBoxLayout()
        Left_Top_LayoutH3 = QHBoxLayout()
        Left_Bottom_LayoutH1 = QHBoxLayout()

        Left_Top_LayoutH1.addWidget(self.Routine_Id_Label)
        Left_Top_LayoutH1.addWidget(self.Routine_Id_Display)

        Left_Top_LayoutH2.addWidget(self.Routine_Name_Label)
        Left_Top_LayoutH2.addWidget(self.Routine_Name_Edit)

        Left_Top_LayoutH3.addWidget(self.Routine_State_Label)
        Left_Top_LayoutH3.addWidget(self.Routine_State_CheckBox)
        # Add widgets to left layout

        Left_Bottom_LayoutH1.addWidget(self.CancelButton)
        Left_Bottom_LayoutH1.addWidget(self.create_apply)

        left_layout.addLayout(Left_Top_LayoutH1)
        left_layout.addLayout(Left_Top_LayoutH2)
        left_layout.addLayout(Left_Top_LayoutH3)

        left_layout.addWidget(self.modify_weight)
        left_layout.addWidget(self.details_list)
        left_layout.addWidget(self.node_list)
        left_layout.addWidget(self.add_point)
        left_layout.addWidget(self.MissedMadeBtn)
        left_layout.addWidget(self.TerMFinshedBtn)
        left_layout.addLayout(Left_Bottom_LayoutH1)
        main_layout.addWidget(self.splitter)

        ###################################################
        ##################  LOAD THE JSON  ###############
        self.load_project(self.json_data)

        ########################################################################
        # Restore GUI from last state                                          #
        if self.settings.contains("geometry"):  #
            self.restoreGeometry(self.settings.value("geometry"))  #
            #                                                                      #
            s = self.settings.value("splitterSize")  #
            self.splitter.restoreState(s)  #
        #                                                                      #
        ########################################################################

    def clicked_terminate_func(self):
        if self.TerminateBtn.checkStateSet() == QtCore.Qt.CheckState.Checked:
            pass
        else:
            pass
        pass

    def pressedOnToggleButton(self, win):
        ToggleButtonXValue = True
        if win:
            print("Made It")
        else:
            print("Missed It")

        pass

    def toggle_active(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.routine.active_state = True
            msgBox = QMessageBox()
            msgBox.setText("Reminder Modify Routine Time.")
            msgBox.setIcon(QMessageBox.Information)
            #msgBox.exec_()

            if not self.clicked_on_finished:
                self.finish_routine.setEnabled(True)
        else:
            self.routine.active_state = False
            self.finish_routine.setEnabled(False)

    def update_widgets(self):
        # self.Date_Start_Display.setText(self.routine.start_time.strftime(CONFIG.dt_format))
        # self.Date_End_Display.setText(self.routine.end_time.strftime(CONFIG.dt_format))
        self.details_list.update_list(self.routine)

    def InProgress(self):
        stored_end_time = self.rsql.get_end_time(self.routine.routine_id)
        return stored_end_time > datetime.datetime.now()

    def clicked_modify_weight(self):
        if self.new_window and isValid(self.new_window):
            self.new_window.close()
        #pass by reference
        #self.new_window = WeightWindow(self.routine,self.routine.finished)

        #pass datetime by value
        if self.editorMode == NodeEditorMode.Edit:
            mRoutine = Routine()
            mRoutine.copy(self.routine)
            #mRoutine.end_time = self.rsql.get_end_time(self.routine.routine_id)
            self.new_window = WeightWindow(mRoutine, self.InProgress())
            self.new_window.show()
            self.new_window.ModifyTimeSignal.connect(self.OnApplyTimeModify)
        elif self.editorMode == NodeEditorMode.New:
            self.new_window = WeightWindow(self.routine, False)
            self.new_window.show()
            self.new_window.ModifyTimeSignal.connect(self.OnApplyTimeModify)

    def OnApplyTimeModify(self, routine):
        if self.editorMode == NodeEditorMode.Edit:
            ss = self.routine.start_time
            start_time = datetime.datetime(ss.year, ss.month, ss.day, ss.hour, ss.minute, ss.second)
            ee = self.routine.end_time
            end_time = datetime.datetime(ee.year, ee.month, ee.day, ee.hour, ee.minute, ee.second)
            self.routine = routine
            if self.InProgress():
                self.routine.start_time = start_time
                self.routine.end_time = end_time
            self.update_widgets()
        elif self.editorMode == NodeEditorMode.New:
            self.routine.CopyDateTime(routine)
            self.update_widgets()

        # def clicked_finish_routine_func(self):
        #     if self.routine.active_state:
        #         #self.routine.start_time = datetime.datetime.now()
        #         #delta_time = CONFIG.calculated_time(self.routine.weight)
        #         #self.routine.end_time = self.routine.start_time + delta_time
        #         self.routine.iterations += 1
        #         self.routine.finished = True
        #         delta_time = (self.routine.end_time - datetime.datetime.now())
        #         self.routine.EXP = delta_time.total_seconds() / 3600
        #         self.update_widgets()
        #         self.clicked_on_finished = True
        #         self.finish_routine.setEnabled(False)
        #         self.Routine_State_CheckBox.setEnabled(False)

        pass

    def clicked_create_modifiy_func(self):
        #### IMPORTANT #####
        routine = self.routine

        if self.editorMode == NodeEditorMode.Edit:
            routine.routine_name = self.Routine_Name_Edit.text()
            save_node_iteration = True # always save node iteration
            #routine.finished = self.routine.finished
            if self.MissedMadeBtn.isVisible():
                self.routine.finished = True
                if self.MissedMadeBtn.IsChecked() == True:
                    save_node_iteration = True
            if self.TerMFinshedBtn.isVisible():
                if self.TerMFinshedBtn.Value() == -1:
                    print("Termination")
                    current = datetime.datetime.now()
                    routine.end_time = current - datetime.timedelta(hours=5)
                elif self.TerMFinshedBtn.Value() == 0:
                    if self.routine.active_state:
                        # self.routine.start_time = datetime.datetime.now()
                        # delta_time = CONFIG.calculated_time(self.routine.weight)
                        # self.routine.end_time = self.routine.start_time + delta_time
                        routine.iterations = self.routine.iterations + 1
                        routine.finished = True
                        save_node_iteration = True
                        delta_time = (self.routine.end_time - datetime.datetime.now())
                        routine.EXP = delta_time.total_seconds() / 3600
                        self.update_widgets()
                        self.clicked_on_finished = True
                        self.finish_routine.setEnabled(False)
                        self.Routine_State_CheckBox.setChecked(True)
                        self.Routine_State_CheckBox.setEnabled(False)

            routine.data = json.dumps(self.sceneHandler.convert_to_json(save_node_iteration))
            routine.active_state = 1 if self.Routine_State_CheckBox.checkState() == QtCore.Qt.CheckState.Checked else 0
            self.Update_Signal.emit(routine)
            self.close()


        elif self.editorMode == NodeEditorMode.New:
            test_time = self.routine.end_time > datetime.datetime.now()
            if test_time == True:
                routine.routine_name = self.Routine_Name_Edit.text()
                routine.data = json.dumps(self.sceneHandler.convert_to_json())
                routine.active_state = 1 if self.Routine_State_CheckBox.checkState() == QtCore.Qt.CheckState.Checked else 0
                routine.finished = False

                self.New_Signal.emit(routine)
                self.close()

    ###################################################
    #############                 ###########
    ############### Modify Node #############
    #############                ############
    #################        ################
    ############### Open  Node ##############
    #############     Editor     ############
    ###################################################
    #add set target
    ## QEditLine and UpgradeButton
    def OpenNodeEditor(self, node):
        if self.new_window and Shiboken.isValid(self.new_window):
            self.new_window.close()
        self.new_window = NodeEditorWindow(node)
        self.new_window.show()

    def clicked_add_point(self):
        node = Custom_Node("point", "describe it")
        self.node_widget.create_custom_node(node)

    def save_project(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("JSON files (*.json)")
        file_path, _ = file_dialog.getSaveFileName()
        self.node_widget.save_project(file_path)

    def load_project(self, json_data=None):
        """
        # self.imports = {}

        # for file in project_path.glob("*.py"):
        #
        #     if not file.stem.endswith('_node'):
        #         print('file:', file.stem)
        #         continue
        #     spec = importlib.util.spec_from_file_location(file.stem, file)
        #     module = importlib.util.module_from_spec(spec)
        #     spec.loader.exec_module(module)
        #
        #     for name, obj in inspect.getmembers(module):
        #         if not name.endswith('_Node'):
        #             continue
        #         if inspect.isclass(obj):
        #             self.imports[obj.__name__] = {"class": obj, "module": module}
        #break

        # self.imports["Add_Node"] = {"class": Add_Node, "module": Add_Node.__module__}
        # self.imports["Button_Node"] = {"class": Button_Node, "module": Button_Node.__module__}
        # self.imports["Print_Node"] = {"class": Print_Node, "module": Print_Node.__module__}
        # self.imports["Scaler_Node"] = {"class": Scaler_Node, "module": Scaler_Node.__module__}
        # self.node_list.update_project(self.imports)

        # work on just the first json file. add the ablitity to work on multiple json files later
        # for json_path in project_path.glob("*.json"):
        #     self.node_widget.load_scene(json_path)
        #     break
        """
        items = []
        if json_data:
            self.sceneHandler.load_scene(json_data)

            for item in self.node_widget.scene.items():
                if isinstance(item, Node):
                    items.append(item)
        if items:
            if len(items) > 0:
                self.node_list.list_all_objects(items)
        ##################################
        #Load Routine Details
        self.details_list.create_list(self.routine)

    def get_project_path(self):
        project_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Project Folder", "")
        if not project_path:
            return

        self.load_project(project_path)

    def closeEvent(self, event):
        """
        Handles the close event by saving the GUI state and closing the application.

        Args:
            event: Close event.

        Returns:
            None.
        """

        # debugging lets save the scene:
        # self.node_widget.save_project("C:/Users/Howard/simple-node-editor/Example_Project/test.json")

        self.settings = QtCore.QSettings("node-editor", "RoutineEditor")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterSize", self.splitter.saveState())
        QtWidgets.QWidget.closeEvent(self, event)
        print("Cloooooosed!")
