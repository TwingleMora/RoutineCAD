from datetime import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from source.config import CONFIG

from source.database.routine_db import RoutineDB

from source.threading_widgets.threadx import Threadx
from source.threading_widgets.notifierThread import NotifierThread


class ProgressWidget(QtWidgets.QWidget):
    # just for the purpose of this example,
    # define a fixed number of threads to run
    nthreads = 10
    routine = None
    TheRoutineTimeIsUpSignal = QtCore.Signal(object)

    UpdateMainRoutineListSignal = QtCore.Signal(object)

    deleteRoutine = QtCore.Signal(object, object)

    def RoutineActiveText(self):
        #convert True to "Active" and False to "Inactive"
        state = "Inactive" if self.routine.active_state == 0 else "Active"
        return state

    def special_update(self, routine):
        #self.routine_id = routine_id
        self.routine.copy(routine)
        self.routine.routine_name = routine.routine_name
        self.routine.active_state = routine.active_state
        #self.routine = routine this makes ot harder as i must pass id also to special update
        #self.display_routine_id.setText(self.routine_id)
        self.display_routine_name.setText(self.routine.routine_name)
        self.display_active_state.setText(self.RoutineActiveText())

        if (routine.start_time is not None) and (routine.end_time is not None):
            # if ((routine.start_time != self.routine.start_time) or (routine.end_time != self.routine.end_time)):
            #     #self.reset(routine.start_time,routine.end_time)
            #     pass
            self.routine.start_time = routine.start_time
            self.routine.end_time = routine.end_time

        self.display_iterations.setText(str(self.routine.iterations))
        finished_str = "Finished" if self.routine.finished else "Not Finished"
        self.display_Finished.setText(finished_str)
        weight_str = str(self.routine.weight) + ", Every " + CONFIG.ConvertDeltaToRemainingTimeStr(
            CONFIG.calculated_time(self.routine.weight))

        self.display_weight.setText(weight_str)

    def delete_btn_func(self):
        # for( self.threads.clear())

        if not CONFIG.debug_mode:
            self.notify.worker.break_loop = True
            self.notify.thread.terminate()
            #del self.notify.thread

            for y in self.t.workers:
                y.break_loop = True
            for x in self.t.threads:
                #x.quit
                x.terminate()
                #x.deleteLater()
                del x  # I don't know whether to keep it or not
            self.t.workers.clear()
            self.deleteLater()
            #self.threads.clear()

        self.deleteRoutine.emit(self.parentItem, self.routine.routine_id)
        self.deleteLater()

        # Draw grey background
        #brush = QBrush(QColor(128, 128, 128))
        #if self.hover:
        #    brush = QBrush(QColor(255, 255, 255))
        #painter.fillRect(event.rect(), brush)
        #painter.fillPath(event.rect(), brush)
        # The main path

    """
    def leaveEvent(self, event):
        self.hover = False
        self.setStyleSheet("background-color: rgb(128, 128, 128);")
        super().leaveEvent(event)
    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.hover=True
        super().enterEvent(event)
    """

    # Draw text
    #       painter.setPen(QtCore.Qt.black)
    #        painter.drawText(10, 20, self.text)
    def enterEvent(self, event):
        self.hover = True
        #print("HOVER")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover = False
        #print("NO HOVER")
        super().leaveEvent(event)

    def paintEvent(self, event):
        #        QtWidgets.QWidget.underMouse()
        painter = QPainter(self)
        #painter.setRenderHint(painter.Antialiasing)

        painter.setPen(self.node_color.lighter())
        qPenColor = CONFIG.pin_border_color_being_connected_color
        painter.setPen(QtGui.QPen(qPenColor, 20))
        painter.setBrush(self.node_color)
        #painter.drawPath(self.path)
        #painter.fillPath(self.path, self.node_color)

        if self.hover:
            painter.fillRect(event.rect(), self.node_color.lighter())
        else:
            painter.fillRect(event.rect(), self.node_color)

    def __init__(self, routine, parentItem: QtWidgets.QListWidgetItem):
        super(ProgressWidget, self).__init__()
        self.rsql = RoutineDB()
        self.hover = self.underMouse()
        #self.setAutoFillBackground(True)
        self.node_color = QtGui.QColor(10, 10, 10)
        self.path = QtGui.QPainterPath()

        self.works = [0 for i in range(self.nthreads)]
        #self.setStyleSheet("""background-color: rgb(0, 0, 0);""")
        self.parentItem = parentItem
        self.routine = routine
        self.finish_string = "What to do Now, BOSS?!"
        self.fetchingTimer = 0
        self.ThisRoutineFinished = self.routine.finished

        ############################################################################
        #Layouts
        self.layout = QVBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout2 = QHBoxLayout()
        hLayout3 = QHBoxLayout()
        hLayout4 = QHBoxLayout()

        ############################################################################
        #Fonts
        #"Lucida Sans Unicode" | pointSize=15
        #"Lucida Sans Unicode" | pointSize=12
        #"Lucida Sans Unicode" | pointSize=10
        #
        #QtGui.QFont(family: str, pointSize: int = -1, weight: int = -1, italic: bool = False)
        font = QtGui.QFont("Lucida Sans Unicode", 12)
        font.setBold(True)
        font.setPointSize(8)

        ############################################################################
        #routine id label
        label_routine_id = QtWidgets.QLabel("Routine ID:")

        #routine id display label
        self.display_routine_id = QtWidgets.QLabel(str(self.routine.routine_id))

        #font
        label_routine_id.setFont(font)
        self.display_routine_id.setFont(font)

        #layout1 widgets
        hLayout1.addWidget(label_routine_id)
        hLayout1.addWidget(self.display_routine_id)

        ############################################################################
        #routine name label
        label_routine_name = QtWidgets.QLabel("Routine Name:")

        #routine name display label
        self.display_routine_name = QtWidgets.QLabel(self.routine.routine_name)

        #font
        label_routine_name.setFont(font)
        self.display_routine_name.setFont(font)

        #layout2 widgets
        hLayout2.addWidget(label_routine_name)
        hLayout2.addWidget(self.display_routine_name)

        ############################################################################
        #progress bar widget
        self.setupUi()

        # delete button
        self.btn_delete = QtWidgets.QPushButton("X")
        self.btn_delete.setMinimumSize(QtCore.QSize(self.progressBar.width() // 10, self.progressBar.height()))
        self.btn_delete.clicked.connect(self.delete_btn_func)

        #font
        self.btn_delete.setFont(font)
        self.progressBar.setFont(font)

        #layout3 widgets
        hLayout3.addWidget(self.progressBar)
        hLayout3.addWidget(self.btn_delete)

        ############################################################################
        # active state label
        label_active_state = QtWidgets.QLabel("Active State:")
        active = "Active" if self.routine.active_state else "Inactive"
        self.display_active_state = QtWidgets.QLabel(active)

        label_weight = QtWidgets.QLabel("Weight:")
        label_weight.setFont(font)
        weight_str = str(self.routine.weight) + ", Every " + CONFIG.ConvertDeltaToRemainingTimeStr(CONFIG.calculated_time(self.routine.weight))
        self.display_weight = QtWidgets.QLabel(weight_str)
        self.display_weight.setFont(font)

        label_iterations = QtWidgets.QLabel("Iterations:")
        label_iterations.setFont(font)
        iterations_str = str(self.routine.iterations)
        self.display_iterations = QtWidgets.QLabel(iterations_str)
        self.display_iterations.setFont(font)

        label_Finished = QtWidgets.QLabel("Finished: ")
        label_Finished.setFont(font)
        finished_str = "Finished" if self.routine.finished else "Not Finished"
        self.display_Finished = QtWidgets.QLabel(finished_str)
        self.display_Finished.setFont(font)

        #font
        label_active_state.setFont(font)
        self.display_active_state.setFont(font)
        hLayoutX = QGridLayout()
        #layout4 widgets
        hLayoutX.addWidget(label_active_state, 0, 0, 1, 1)
        hLayoutX.addWidget(self.display_active_state, 0, 1, 1, 1)

        hLayoutX.addWidget(label_iterations, 2, 0, 1, 1)
        hLayoutX.addWidget(self.display_iterations, 2, 1, 1, 1)

        #hLayoutX = QHBoxLayout()
        hLayoutX.addWidget(label_weight, 1, 0, 1, 1)
        hLayoutX.addWidget(self.display_weight, 1, 1, 1, 1)

        #hLayoutX = QHBoxLayout()
        hLayoutX.addWidget(label_Finished, 0, 2, 1, 1)
        hLayoutX.addWidget(self.display_Finished, 0, 3, 1, 1)
        ############################################################################
        # "self.layout" layout
        self.layout.addLayout(hLayout1)
        self.layout.addLayout(hLayout2)
        self.layout.addLayout(hLayout3)
        self.layout.addLayout(hLayoutX)
        # self.layout.addLayout(hLayout5)
        # self.layout.addLayout(hLayout6)

        ###########################################

        self.setLayout(self.layout)

        self.t = Threadx(self.routine, self.handleProgress)
        self.notify = NotifierThread(routine=self.routine)
        #self.setupWorkers()
        #self.runThreads()

    def drawProgessBar(self):
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 582, 24))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(60000)
        self.progressBar.setValue(60000)

        self.progressBar.setStyleSheet(
            "QProgressBar { border: 2px solid #000; border-radius: 5px; } QProgressBar::chunk { background-color: #a61133; }")

        self.progressBar.setFormat("")

    def setupUi(self):
        #self.setWindowTitle("Threaded Progress")
        #self.resize(600, 60)
        self.setMaximumHeight(200)
        self.setContentsMargins(20, 20, 20, 20)
        #self.setStyleSheet("padding: 20px;")
        self.drawProgessBar()

    def end(self):
        for worker in self.t.workers:
            worker.break_loop = True

    def stop(self):
        for worker in self.t.workers:
            worker.Alive = False

    def start(self):
        for worker in self.t.workers:
            worker.Alive = True

    def reset(self, start_time, end_time):
        for worker in self.t.workers:
            worker.update(start_time, end_time)
            worker.Alive = True
        self.progressBar.setValue(self.progressBar.maximum())
        self.progressBar.setFormat("")
        print(f"routine {self.routine.routine_id} was updated with weight of {self.routine.weight}")
        # self.routine.start_time = start_time
        # self.routine.end_time = end_time
        # start = self.routine.start_time
        # end = self.routine.end_time
        #
        # #self.t.delete()
        #
        # self.progressBar.setValue(self.progressBar.maximum())
        # self.progressBar.setFormat("")
        # #self.t = Threadx(self.routine,self.handle)
        # self.t.stop()
        # self.t.play(start_time, end_time)
        # #worker.updateProgress.connect(self.handle)

        pass

    def calculate(self):
        self.routine.weight = float(self.rsql.get_weight(self.routine.routine_id))
        time_difference = CONFIG.calculated_time(self.routine.weight)
        # if not self.modify_routine:
        #     current = datetime.datetime.now()
        #     end = current + self.time_difference
        # else:
        #     current = self.routine.end_time
        #     end = self.routine.end_time + self.time_difference
        current = datetime.now()
        end = current + time_difference
        # str = CONFIG.ConvertDeltaToSeconds(self.time_difference)
        # self.DueTimeDisplay.setText(str)
        # self.Time_End_Display.setText(end.strftime(CONFIG.dt_format))
        self.routine.start_time = current
        self.routine.end_time = end

    def reset_all_workers(self):
        for worker in self.t.workers:
            worker.end_time = datetime.now()

    Finished = False
    fixX = False

    def handleProgress(self, signal):
        #(,,signal)
        index, progress = signal  #tuple
        self.works[index] = progress
        self.fixX = self.rsql.get_finished_state(self.routine.routine_id)
        self.et = self.rsql.get_end_time(self.routine.routine_id)
        self.display_Finished.setText("Finished" if self.fixX else "Not Finished")
        value = 0
        nonzero_items = 0

        if progress >= 0:
            for work in self.works:
                if work != 0:
                    value += work
                    nonzero_items += 1
            value /= float(nonzero_items)
            #timeleft = self.routine.end_time - datetime.now()
            timeleft = self.routine.end_time - datetime.now()
            # if value < 0:
            #     self.progressBar.setFormat(self.finish_string)
            #     self.progressBar.setValue(0)
            #     #return
            # else:
            #print(f"routine {self.routine.routine_id} no flags")
            if not self.fixX:
                #self.changeToRed()
                #print(f"routine {self.routine.routine_id} in progress after reset and finished = false")
                self.progressBar.setFormat("%d days and %.2d:%.2d:%.2d" % (
                    timeleft.days, timeleft.seconds // 3600, (timeleft.seconds % 3600) // 60,
                    (timeleft.seconds % 3600) % 60))
            else:
                #self.changeToRed()
                #self.changeToBlue()
                value = self.progressBar.maximum() - value
                #print(f"routine {self.routine.routine_id} in progress after reset and routine is finished ")
                self.progressBar.setStyleSheet(
                    "QProgressBar { border: 2px solid #000; border-radius: 5px; } QProgressBar::chunk { background-color: #2e56ab; }")
                self.progressBar.setFormat("Break:  %d days and %.2d:%.2d:%.2d" % (
                    timeleft.days, timeleft.seconds // 3600, (timeleft.seconds % 3600) // 60,
                    (timeleft.seconds % 3600) % 60))

                #print(f"routine {self.routine.routine_id} finished flag")
            self.progressBar.setValue(value)
            if (self.et < datetime.now()):
                #print("TerminateeeeeeXX")
                self.reset_all_workers()

        elif progress == -1:  #Routine Time Is Up

            #print(f"routine {self.routine.routine_id} flag -1")
            self.progressBar.setFormat(self.finish_string)
            self.progressBar.setValue(0)
            #print(f"send time is up to routine {self.routine.routine_id} ")
            self.TheRoutineTimeIsUpSignal.emit(progress)
            self.progressBar.setStyleSheet(
                "QProgressBar { border: 2px solid #000; border-radius: 5px; } QProgressBar::chunk { background-color: #a61133; }")
            if (self.fixX == True):
                self.fixX = False
                ##### CALCULATE NEW TIME #######
                self.calculate()
                ################## IMPORTANT ################
                self.routine.finished = False
                self.rsql.update_time(self.routine)
                self.reset(self.routine.start_time, self.routine.end_time)

            #print("Unfinished Routine's Time Is Up!")
        elif progress == -2:
            #self.Finished = True
            #self.changeToBlue()
            #self.routine.finished = True
            #self.progressBar.setStyleSheet(
            #    "QProgressBar { border: 2px solid #000; border-radius: 5px; } QProgressBar::chunk { background-color: #2e56ab; }")
            ##### Now Let's Decide Whether To Continue Or No ######
            #print(f"routine {self.routine.routine_id} flag -2")
            pass
        else:
            #print(f"routine {self.routine.routine_id} super negative")
            pass

    def changeToBlue(self):
        for worker in self.t.workers:
            worker.blue = True

    def changeToRed(self):
        for worker in self.t.workers:
            worker.blue = False
