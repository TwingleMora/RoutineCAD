from PySide6 import QtCore

import time
from datetime import datetime

from PySide6.QtGui import QIcon

from source.config import CONFIG
from source.database.routine_db import RoutineDB
from win10toast import ToastNotifier
from plyer import notification
from winotify import Notification, audio
from source.routine import Routine
import icons
import winsound


class NotificationWorker(QtCore.QObject):
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
        super(NotificationWorker, self).__init__()
        self.toast = None
        self.rsql = RoutineDB()
        self.routine = Routine()
        self.routine.copy(routine)
        self.fetchingTimer = 0
        self.end_time = self.routine.end_time
        self.start_time = self.routine.start_time
        # store the ProgressWorker index (for thread tracking
        # and to compute the overall progress)
        self.id = index
        self.progress = 0
        self.blue = False
        print("notification worker created")
        self.break_notification = False

    def update(self, start_time, end_time):
        self.progress = 0
        self.end_time = end_time
        self.start_time = start_time
        #print(f"routine {self.routine.routine_id} was upadted in worker")
        #self.routine.finished = False

    def notification_work(self):

        end = self.end_time
        start = self.start_time

        now = datetime.now()
        delta1 = end - now
        delta2 = end - start

        self.progress = (delta1 / delta2) * 60000
        self.percent = (self.progress / 60000) * 100
        self.last_percent = 100
        while (True):
            if self.break_loop:
                break
            self.routine.active_state = self.rsql.get_active_state(self.routine.routine_id)

            if self.fetchingTimer > 5:
                self.routine.finished = self.rsql.get_finished_state(self.routine.routine_id)
                self.start_time = self.rsql.get_start_time(self.routine.routine_id)
                self.end_time = self.rsql.get_end_time(self.routine.routine_id)
                self.fetchingTimer = 0
            self.fetchingTimer += 1
            print("in worker loop")
            if self.break_loop:
                break

            if self.routine.active_state:
                self.Alive = True
                print(f"routine {self.routine.routine_name} is activee agaaain")



            if datetime.now() > self.end_time:
                self.Alive = False
                print("dead in worker loop")
                time.sleep(1)
                self.last_percent = 100
                self.break_notification = False
            else:
                self.Alive = True
                print("data now is less than data end")

            if self.break_loop:
                break

            if not self.routine.active_state:
                self.Alive = False
                print(f"routine {self.routine.routine_name} is noooot activee")


            if self.break_loop:
                break

            if self.Alive:
                print("live in worker loop")
                sent = True
                time.sleep(1)
                end = self.end_time
                start = self.start_time
                now = datetime.now()
                delta1 = end - now
                delta2 = end - start
                self.progress = ((delta1 / delta2) * 60000)
                self.percent = (self.progress / 60000) * 100
                self.toast = ToastNotifier()
                # try:
                if not self.routine.finished:

                    # self.toast.show_toast("Routines",
                    #                       f"Routine {self.routine.routine_name} is {self.percent:.2f}% now\n"
                    #                       f"{CONFIG.ConvertDeltaToRemainingTimeStr(delta1)} remaining", duration=5,
                    #                           icon_path=r"E:\optz\bk\spec\app.ico")
                    #winsound.Beep(37, 5000)
                    if self.percent < self.last_percent - 20:
                        self.last_percent = self.percent
                        notification.notify(title="Routines",
                                            message=f"Routine {self.routine.routine_name} is {self.percent:.2f}% now\n"
                                                    f"{CONFIG.ConvertDeltaToRemainingTimeStr(delta1)} remaining",
                                            app_icon=CONFIG.icon_file,
                                            timeout=5)

                    pass
                else:
                    if self.percent < 10:
                        self.break_notification = True
                    if self.break_notification:
                        if self.percent < self.last_percent - 3:
                            self.last_percent = self.percent
                            notification.notify(title="Routines",
                                                message=f"Routine {self.routine.routine_name} break mode is finishing soon\n"
                                                        f"{CONFIG.ConvertDeltaToRemainingTimeStr(delta1)} remaining",
                                                app_icon=CONFIG.icon_file,
                                                timeout=5)

                    pass

                if self.progress < 0:
                    continue
            else:
                time.sleep(1)
                continue
