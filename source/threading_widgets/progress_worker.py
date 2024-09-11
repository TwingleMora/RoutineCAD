from PySide6 import QtCore

import time
from datetime import datetime
from source.database.routine_db import RoutineDB


class ProgressWorker(QtCore.QObject):
    """the worker for a threaded process;
    (this is created in the main thread and
    then moved to a QThread, before starting it)
    """

    end_time: datetime = None
    updateProgress = QtCore.Signal(tuple)
    sendExperiencePoints = QtCore.Signal(object)
    #SQLFetch = QtCore.Signal(tuple)

    finished = QtCore.Signal(int)
    Alive = True
    #Finished = False
    break_loop = False

    def __init__(self, index, routine):
        super(ProgressWorker, self).__init__()
        self.rsql = RoutineDB()
        self.routine = routine
        self.fetchingTimer = 0
        self.end_time = self.routine.end_time
        self.start_time = self.routine.start_time
        # store the ProgressWorker index (for thread tracking
        # and to compute the overall progress)
        self.id = index
        self.progress = 0
        self.blue = False

    def update(self, start_time, end_time,active_state=None):
        self.progress = 0
        self.end_time = end_time
        self.start_time = start_time
        if active_state is not None:
            self.routine.active_state = active_state
        #print(f"routine {self.routine.routine_id} was upadted in worker")
        #self.routine.finished = False

    def progressbar_work(self):

        end = self.end_time
        start = self.start_time

        now = datetime.now()
        delta1 = end - now
        delta2 = end - start

        dd = delta2.total_seconds()

        ratio = (60000 / float(dd))
        #(end - start) *100        1 * 100
        #-------------      -   ---------------
        #end - start               end-start
        self.progress = (delta1 / delta2) * 60000
        sent = False
        while (True):
            if self.break_loop:
                break
            if self.fetchingTimer > 5:
                #self.routine.finished = self.rsql.get_finished_state(self.routine.routine_id)
                self.routine.active_state = self.rsql.get_active_state(self.routine.routine_id)
                # if not self.routine.active_state:
                #     #self.updateProgress.emit((self.id, -3))
                #     self.Alive = False
                #     #print("This is Weirdddd")
                # else:
                #     self.Alive = True
                self.fetchingTimer = 0
            self.fetchingTimer += 1

            if not self.routine.active_state:
                # self.updateProgress.emit((self.id, -3))
                self.Alive = False
                # print("This is Weirdddd")
            else:
                self.Alive = True

            if self.break_loop:
                break

            if datetime.now() > self.end_time:
                #print(f"routine {self.routine.routine_id} is stucked here (not Alive)")
                self.updateProgress.emit((self.id, -1))
                self.Alive = False
                time.sleep(1)

            if self.break_loop:
                break

            if self.Alive:
                sent = True
                time.sleep(1)
                end = self.end_time
                start = self.start_time
                now = datetime.now()
                delta0 = now - start
                delta1 = end - now
                delta2 = end - start

                #self.progress -= ratio/4
                #if not self.blue:
                self.progress = ((delta1 / delta2) * 60000)
                #else:

                #    self.progress = ((delta0 / delta2) * 60000)
                if self.progress < 0:

                    #print("Negativeeeeeeeee")
                    continue
                self.updateProgress.emit((self.id, self.progress))
            else:
                time.sleep(1)
                #print("not alive but now is less than end")
                continue
        #print("brrrrrrreeeeeeeeeeeeeeeek")
        self.Alive = True
        #self.finished.emit(1)
