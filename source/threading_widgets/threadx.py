from PySide6 import QtCore, QtWidgets
from source.threading_widgets.progress_worker import ProgressWorker
from source.config import CONFIG
from source.threading_widgets.time_worker import TimeWorker


class Threadx(QtWidgets.QWidget):

    def __init__(self, routine=None, handle=None, ztime=False, nthreads=3, routine_in_progress=False, parent=None):
        super(Threadx, self).__init__()
        self.thread = None
        self.worker = None
        self.nthreads = nthreads
        self.threads = []
        self.workers = []
        self.works = [0 for i in range(self.nthreads)]
        self.ztime = ztime
        self.routine = routine
        self.routine_in_progress = routine_in_progress
        self.handle = handle
        if not CONFIG.debug_mode:
            self.setupWorkers()
            self.runThreads()


    def setupWorkers(self):
        if self.ztime:
            if not self.routine_in_progress:
                self.thread: QtCore.QThread = QtCore.QThread()
                self.worker = TimeWorker(0, self.routine)
                self.worker.updateProgress.connect(self.handle)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.time_work)
                self.worker.finished.connect(self.thread.quit())
                QtCore.QMetaObject.connectSlotsByName(self)
                self.thread.start()
            pass
        else:
            # for progress bar
            for i in range(self.nthreads):
                self.buildWorker(i)


    # for progress bar
    def buildWorker(self, index):
        """a generic function to build multiple workers;
        workers will run on separate threads and emit signals
        to the ProgressWidget, which lives in the main thread
        """

        self.thread: QtCore.QThread = QtCore.QThread()
        self.worker = ProgressWorker(index, self.routine)
        self.worker.updateProgress.connect(self.handle)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.progressbar_work)
        self.worker.finished.connect(self.thread.quit())
        QtCore.QMetaObject.connectSlotsByName(self)
        # retain a reference in the main thread

        self.threads.append(self.thread)
        self.workers.append(self.worker)



#for progress bar
    def runThreads(self):
        for thread in self.threads:
            thread.start()

    def delete(self):
        for x in self.workers:
            x.Alive = False
            x.updateProgress.disconnect(self.handle)
        self.workers.clear()
        for x in self.threads:
            x.quit()
            x.terminate()  #x.quit() #x.exit()
            del x

    def stop(self):
        for x in self.workers:
            x.Alive = False
            x.updateProgress.disconnect(self.handle)

    def play(self, start, end):
        for x in self.workers:
            x.start_time = start
            x.end_time = end
            x.Alive = True
            x.updateProgress.connect(self.handle)

        #self.deleteLater()
        # self.removeItemWidget(parentItem)
        # self.takeItem(self.row(parentItem))
        # self.rsql.delete_record_by_id(id)
        # self.workers.clear()

        # self.deleteRoutine.emit(self.parentItem, self.routine.routine_id)
        # self.deleteLater()
