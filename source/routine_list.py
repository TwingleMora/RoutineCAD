import json

from PySide6 import QtCore, QtWidgets

from source.database.routine_db import RoutineDB
from source.routine import Routine
from source.threading_widgets.progressbar import ProgressWidget
from source.RoutineEditor import RoutineEditor


class RoutineList(QtWidgets.QListWidget):
    #########################################
    ########### MAIN MENU SIGNALS ###########
    ###########                   ###########
    #########################################
    ################# FOR EXAMPLE IF USER REMOVED A ROUTINE ##############
    UpdateMainRoutineListSignal = QtCore.Signal(object)
    ################ TO UPDATE NO OF ACTIVE ROUTINES ################

    #### OPEN ROUTINE
    #################################
    ############# 1 #################
    #################################
    openRoutine = QtCore.Signal(object)
    qListWidgetItem = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rsql = RoutineDB()
        self.setSpacing(10)
        #self.setStyleSheet("background-color: black;")
        #self.setStyleSheet("""foreground-color: rgb(255, 255, 0);""")

    def create_list(self):
        #records = self.rsql.get_records_as_list()
        records = self.rsql.get_routines()
        for i in range(len(records)):
            # I may remove the text in the future
            item = QtWidgets.QListWidgetItem("")
            #item.setBackground(QtGui.QColor(0, 0, 0))
            #item.setForeground(QtGui.QColor(0, 0, 0))
            ##############
            ########## WE DONT INCLUDED JSON DATA HERE WE INCLUDE IT IN
            ########## MODULEX WE GET IT FROM DB
            ##############
            mRoutine = records[i]
            routine_item = ProgressWidget(mRoutine, parentItem=item)

            routine_item.deleteRoutine.connect(self.remove_item_from_list)
            item.progressWidget = routine_item
            item.setSizeHint(routine_item.size())

            self.addItem(item)
            self.setItemWidget(item, routine_item)

    def add_item_to_list(self, routine):
        self.rsql.insert(routine)
        # I may remove the text in the future
        item = QtWidgets.QListWidgetItem("")
        routine_item = ProgressWidget(routine, parentItem=item)
        routine_item.deleteRoutine.connect(self.remove_item_from_list)
        item.setSizeHint(routine_item.size())
        item.progressWidget = routine_item
        self.addItem(item)
        self.setItemWidget(item, routine_item)

    def update_list(self):
        dicts = self.rsql.get_records_as_dicts()
        #records = self.rsql.get_routines()
        for i in range(len(dicts)):
            id = int(self.itemWidget(self.item(i)).routine.routine_id)

            self.itemWidget(self.item(i)).special_update(
                Routine(routine_id=id, routine_name=dicts[id]["name"], active_state=dicts[id]["active_state"],
                        iterations=dicts[id]["iterations"], finished=dicts[id]["finished"], weight=dicts[id]["weight"],
                        start_time=dicts[id]["start_time"], end_time=dicts[id]["end_time"]))
            print("Id: ", id)

    def remove_item_from_list(self, parentItem, id):
        self.removeItemWidget(parentItem)
        self.takeItem(self.row(parentItem))
        self.rsql.delete_record_by_id(id)

        self.UpdateMainRoutineListSignal.emit(-1)

        ################
        ################ IMPORTANT
        ################
        ##########################################
        ##########
        #################### 25dt 2yh mn el database w 25dt 2yh mn el routine_list_item(item.modulex)
        #########
        ###########################################

    def OpenRoutineEditor(self, progressWidgetItem):
        routine_id = progressWidgetItem.routine.routine_id
        #1# routine = routine_list_item.routine
        #1# dict_x = self.export_from_table_by_id(self.table_name, routine.routine_id)
        #3.0# db_routine = self.rsql.get_routine_by_id(routine.routine_id)
        #3.1#
        db_routine = self.rsql.get_routine_by_id(routine_id)
        json_s = db_routine.data
        json_f = json.loads(json_s)
        ############################
        ##########################################################
        #2# routine.start_time = db_routine.start_time
        #2# routine.end_time = db_routine.end_time
        #2# routine.iterations = db_routine.iterations
        #2# routine.weight = db_routine.weight

        #3#
        self.launcher = RoutineEditor(db_routine, json_f)
        progressWidgetItem.TheRoutineTimeIsUpSignal.connect(self.launcher.OnTimeUp)
        self.launcher.show()

        self.launcher.Update_Signal.connect(self.UpdateRoutineClicked)

    def UpdateRoutineClicked(self, routine):
        #self.update_in_table(self.table_name, routine.routine_id, routine.routine_name, routine.data,routine.active_state)
        self.rsql.update(routine)
        #self.update_list()
        self.update_list()
        self.UpdateMainRoutineListSignal.emit(1)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if (event.button() == QtCore.Qt.LeftButton):
            if item:
                #1#self.openRoutine.emit(item.modulex)
                #2#self.OpenRoutineEditor(item.modulex)
                #3#
                #progress_bar = item.progressWidget
                #id = routine.routine_id
                self.OpenRoutineEditor(item.progressWidget)
                #print("IDDDD ",item.modulex.routine_id)

        # elif(event.button()== QtCore.Qt.RightButton):
        #     if item:
        #         end =datetime.datetime.now()+datetime.timedelta(seconds=20*random.random())
        #         start = datetime.datetime.now()
        #         item.modulex.reset(start,end)
        super().mousePressEvent(event)
