from PySide6 import QtCore, QtWidgets
import datetime

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from source.threading_widgets.threadx import Threadx
from source.config import CONFIG


class WeightWindow(QtWidgets.QWidget):
    ModifyTimeSignal = QtCore.Signal(object)

    def __init__(self, routine, routine_in_progress=False, parent=None):
        super(WeightWindow, self).__init__()
        self.time_difference = 0
        self.routine = routine
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Routine Weight Window")
        self.routine_finished = routine_in_progress
        self.Time_Current_Label = QLabel("Current Time: ")
        self.Time_Current_Display = QLabel("")
        self.routine_in_progress = routine_in_progress
        if not self.routine_in_progress:
            self.Time_Current_Display = QLabel(datetime.datetime.now().strftime(CONFIG.dt_format))
        else:
            if self.routine.end_time is not None:
                self.Time_Current_Display = QLabel(self.routine.end_time.strftime(CONFIG.dt_format))

        self.Time_End_Label = QLabel("End Time: ")
        self.Time_End_Display = QLabel("")
        #if not self.routine_in_progress:
        if self.routine.end_time is not None:
            self.Time_End_Display = QLabel(self.routine.end_time.strftime(CONFIG.dt_format))

        self.DueTimeLabel = QLabel("Finish It In: ")
        self.DueTimeDisplay = QLabel("")

        self.Weight_Label = QLabel("Weight: ")
        self.Weight_Edit = QtWidgets.QLineEdit()
        self.Weight_Edit.textChanged.connect(self.onWeightChanged)
        #self.Weight_Edit.textEdited

        self.applyButton = QtWidgets.QPushButton("Apply")
        self.applyButton.clicked.connect(self.apply)

        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        Horizontal_Layout1 = QHBoxLayout()
        Horizontal_Layout2 = QHBoxLayout()
        Horizontal_Layout3 = QHBoxLayout()

        Date_Start_Horizontal_Layout4 = QHBoxLayout()
        Date_End_Horizontal_Layout4 = QHBoxLayout()
        Vertical_Layout = QVBoxLayout()

        Date_Start_Horizontal_Layout4.addWidget(self.Time_Current_Label)
        Date_Start_Horizontal_Layout4.addWidget(self.Time_Current_Display)

        Date_End_Horizontal_Layout4.addWidget(self.Time_End_Label)
        Date_End_Horizontal_Layout4.addWidget(self.Time_End_Display)

        Horizontal_Layout1.addWidget(self.Weight_Label)
        Horizontal_Layout1.addWidget(self.Weight_Edit)

        Horizontal_Layout2.addWidget(self.DueTimeLabel)
        Horizontal_Layout2.addWidget(self.DueTimeDisplay)

        Horizontal_Layout3.addWidget(cancelButton)
        Horizontal_Layout3.addWidget(self.applyButton)

        Vertical_Layout.addLayout(Date_Start_Horizontal_Layout4)
        Vertical_Layout.addLayout(Date_End_Horizontal_Layout4)
        Vertical_Layout.addLayout(Horizontal_Layout1)
        Vertical_Layout.addLayout(Horizontal_Layout2)
        Vertical_Layout.addLayout(Horizontal_Layout3)

        #Vertical_Layout.addWidget(self.modify_weight)

        self.setLayout(Vertical_Layout)
        self.thread = Threadx(routine=self.routine, handle=self.TimeProgressHandler, ztime=True, nthreads=2,
                              routine_in_progress=routine_in_progress)

    def calculate_without_assigning(self):
        if CONFIG.is_number(self.Weight_Edit.text()):
            weight = float(self.Weight_Edit.text())

            self.time_difference = CONFIG.calculated_time(weight)
            if not self.routine_finished:
                current = datetime.datetime.now()
                end = current + self.time_difference
            else:
                current = self.routine.end_time
                end = self.routine.end_time + self.time_difference

            str = CONFIG.ConvertDeltaToRemainingTimeStr(self.time_difference)
            self.DueTimeDisplay.setText(str)
            self.Time_End_Display.setText(end.strftime(CONFIG.dt_format))

    def calculate(self):
        if CONFIG.is_number(self.Weight_Edit.text()):
            weight = float(self.Weight_Edit.text())

            self.time_difference = CONFIG.calculated_time(weight)
            if not self.routine_in_progress:
                current = datetime.datetime.now()
                end = current + self.time_difference
            else:
                current = self.routine.end_time
                end = self.routine.end_time + self.time_difference

            str = CONFIG.ConvertDeltaToRemainingTimeStr(self.time_difference)
            self.DueTimeDisplay.setText(str)
            self.Time_End_Display.setText(end.strftime(CONFIG.dt_format))
            self.routine.start_time = current
            self.routine.end_time = end
            self.routine.weight = weight
            return True
        return False

    def apply(self):
        if self.calculate():
            if self.routine.start_time and self.routine.end_time:
                if self.routine.end_time > self.routine.start_time:
                    #temp = Routine(start_time=self.routine.start_time,
                    #              end_time=self.routine.end_time,
                    #             weight=self.routine.weight)
                    temp = self.routine
                    self.ModifyTimeSignal.emit(temp)
                    self.close()
        pass



    def onWeightChanged(self):
        self.routine.weight = 0
        self.time_difference = 0
        self.calculate_without_assigning()
        pass

    def TimeProgressHandler(self, signal):
        id, dt = signal
        if isinstance(dt, datetime.datetime):
            self.Time_Current_Display.setText(dt.strftime(CONFIG.dt_format))
        else:
            self.Time_Current_Display.setText("Stoped")
        pass

    def closeEvent(self, event):
        #self.thread.delete()
        if not CONFIG.debug_mode:
            if self.thread.thread:
                self.thread.thread.quit()
                self.thread.worker.break_loop = True
                self.thread.worker.deleteLater()
        #del self.thread
        self.deleteLater()
        print("weight clossssssssssssse")
