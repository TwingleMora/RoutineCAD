from PySide6 import QtCore, QtWidgets
from source.threading_widgets.progress_worker import ProgressWorker
from source.config import CONFIG
from source.threading_widgets.time_worker import TimeWorker
from source.threading_widgets.notification_worker import NotificationWorker

class NotifierThread(QtWidgets.QWidget):

    def __init__(self, routine=None):
        super(NotifierThread, self).__init__()
        self.thread = None
        self.worker = None
        self.nthreads = 1
        # self.threads = []
        # self.workers = []
        self.works = [0 for i in range(self.nthreads)]
        #self.ztime = ztime
        self.routine = routine
        #self.routine_in_progress = routine_in_progress
        #self.handle = handle
        if not CONFIG.debug_mode:
            self.setupWorkers()
            self.runThreads()


    def setupWorkers(self):
        self.buildWorker(1)


    # for progress bar
    def buildWorker(self, index):
        """a generic function to build multiple workers;
        workers will run on separate threads and emit signals
        to the ProgressWidget, which lives in the main thread
        """

        self.thread: QtCore.QThread = QtCore.QThread()
        self.worker = NotificationWorker(index, self.routine)
        #self.worker.updateProgress.connect(self.handle)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.notification_work)
        self.worker.finished.connect(self.thread.quit())
        QtCore.QMetaObject.connectSlotsByName(self)
        print("Build Worker")
        # retain a reference in the main thread

        #self.threads.append(self.thread)
        #self.workers.append(self.worker)



#for progress bar
    def runThreads(self):
        self.thread.start()

    def delete(self):
        self.worker.Alive = False
        #self.worker.updateProgress.disconnect(self.handle)
        self.thread.quit()
        self.thread.terminate()  #x.quit() #x.exit()
        del self.thread

    def stop(self):
        self.worker.Alive = False
        #self.worker.updateProgress.disconnect(self.handle)

    def play(self, start, end):
        self.worker.start_time = start
        self.worker.end_time = end
        self.worker.Alive = True
        #self.worker.updateProgress.connect(self.handle)

        #self.deleteLater()
        # self.removeItemWidget(parentItem)
        # self.takeItem(self.row(parentItem))
        # self.rsql.delete_record_by_id(id)
        # self.workers.clear()

        # self.deleteRoutine.emit(self.parentItem, self.routine.routine_id)
        # self.deleteLater()
