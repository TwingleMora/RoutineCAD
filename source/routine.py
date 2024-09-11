from datetime import datetime
import dateutil.parser


class Routine:
    routine_id: int = 0  ##[x]##
    routine_name: str = ""  ##[x]##
    start_time: datetime = None  # datetime(2024)  ##[]##
    end_time: datetime = None  # datetime(2025)  ##[]##
    data: str = None
    active_state: int = 1  ##[]##
    iterations: int = 0  ##[]##
    EXP:float =0

    def __init__(self, routine_id=None, routine_name=None, start_time: datetime = None, end_time: datetime = None,
                 data=None, active_state=None, iterations=0, weight=1, finished=False, EXP=0):
        self.routine_id = routine_id
        self.routine_name = routine_name
        self.start_time = start_time
        self.end_time = end_time
        self.data = data
        self.active_state = active_state
        self.iterations = iterations
        self.weight = weight
        self.finished = finished
        self.EXP = EXP
        ############## For Dicts ##############
        if isinstance(start_time, str):
            self.start_time = dateutil.parser.parse(start_time)
        if isinstance(end_time, str):
            self.end_time = dateutil.parser.parse(end_time)

        pass

    def CopyDateTime(self, routine):
        ss = routine.start_time
        self.start_time = datetime(year=ss.year, month=ss.month, day=ss.day, hour=ss.hour, minute=ss.minute,
                                   second=ss.second)
        ee = routine.end_time
        self.end_time = datetime(year=ee.year, month=ee.month, day=ee.day, hour=ee.hour, minute=ee.minute,
                                 second=ee.second)

    def copy(self, routine):
        self.routine_id = routine.routine_id
        self.routine_name = routine.routine_name
        ss = routine.start_time
        self.start_time = datetime(year=ss.year, month=ss.month, day=ss.day, hour=ss.hour, minute=ss.minute,
                                   second=ss.second)
        ee = routine.end_time
        self.end_time = datetime(year=ee.year, month=ee.month, day=ee.day, hour=ee.hour, minute=ee.minute,
                                 second=ee.second)

        self.data = routine.data
        self.active_state = routine.active_state
        self.iterations = routine.iterations
        self.weight = routine.weight
        self.finished = routine.finished
        self.EXP = routine.EXP

    def calculate(self):
        pass
