from PySide6 import QtCore

import time
from datetime import datetime
from source.database.routine_db import RoutineDB

class TimeWorker(QtCore.QObject):
    """the worker for a threaded process;
    (this is created in the main thread and
    then moved to a QThread, before starting it)
    """

    end_time: datetime = None
    updateProgress = QtCore.Signal(tuple)
    #SQLFetch = QtCore.Signal(tuple)

    finished = QtCore.Signal(int)
    Alive = True
    Finished = False

    break_loop = False;
    def __init__(self, index, routine):
        super(TimeWorker, self).__init__()
        self.rsql = RoutineDB()
        self.routine = routine
        self.fetchingTimer = 0
        self.end_time = self.routine.end_time
        self.start_time = self.routine.start_time
        # store the Worker index (for thread tracking
        # and to compute the overall progress)
        self.id = index
        self.progress = 0

    def update(self, start_time, end_time):

        self.progress = 0
        self.end_time = end_time
        self.start_time = start_time

    def time_work(self):
        sent=False
        while (True):
            if self.break_loop:
                break
            time.sleep(1)
            if self.Alive:
                sent = True

                now = datetime.now()
                self.updateProgress.emit((self.id,now))
            else:
                if not sent:
                    self.updateProgress.emit((self.id, -1))
                    sent=True
                time.sleep(5)
                continue
        self.Alive = True
        self.finished.emit(1)
