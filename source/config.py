from PySide6 import QtGui
import datetime

from PySide6.QtGui import QIcon


class CONFIG:
    icon_file = "internal_icon.ico"
    @staticmethod
    def load_notification_icon():
        icon = QIcon(':/Portfolio_X/Apps/UnderDevelopment/Course/Point1/Point1/app.ico')
        icon.pixmap(64, 64).save(CONFIG.icon_file)

    maxSceneRect = 99999
    intial_scale_factor = 0.25 / 2

    debug_mode = False
    list_font = QtGui.QFont("Comic Sans MS", 8)

    @staticmethod
    def is_number(s: str):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def ConvertDeltaToRemainingTimeStr(timeleft):
        return ("%d days and %.2d:%.2d:%.2d" % (
            timeleft.days, timeleft.seconds // 3600, (timeleft.seconds % 3600) // 60,
            (timeleft.seconds % 3600) % 60))

    @staticmethod
    def calculated_time(weight):
        if weight:
            if weight != 0:
                equation = 96 * (1 / weight)
                return datetime.timedelta(hours=equation)
        return datetime.timedelta(seconds=0)

    ## View ##
    grid_size_course = 600
    grid_size_fine = 30

    connection_thickness = 7
    pin_radius = 20
    pin_margin = 5
    pin_thickness = 5

    db_name = "RDB"
    routine_table_name = "routines"
    node_table_name = ""
    #default_dt_format = "YYYY-MM-DDTHH:MM:SS.mmmmmm"
    default_dt_format = "%Y-%m-%d %H:%M:%S.%f"
    #dt_format = "%Y/%m/%d, %H:%M:%S a"
    dt_format = "%m/%d, %I:%M:%S %p"
    font_factor = 2
    title_font = QtGui.QFont("Comic Sans MS", pointSize=25 * font_factor)
    title_type_font = QtGui.QFont("Comic Sans MS", pointSize=18 * font_factor)
    pin_font = QtGui.QFont("Comic Sans MS", 14 * font_factor)

    node_text_font = QtGui.QFont("Comic Sans MS", pointSize=20 * font_factor)
    node_checkbox_font = QtGui.QFont("Comic Sans MS", pointSize=15 * font_factor)
    node_labels_font = QtGui.QFont("Comic Sans MS", pointSize=15 * font_factor)

    title_font.setBold(True)
    title_type_font.setBold(True)
    pin_font.setBold(True)
    node_text_font.setBold(True)
    node_checkbox_font.setBold(True)
    node_labels_font.setBold(False)
    NodeMinimumHeaderHeight = 150
    NodeMinimumWidth = 80
    NodeWidthMarginX = 150
    NodeWidthMargin = 40
    NodeVerticalMargin = 20
    NodePinTextMargin = 0

    pin_h_off = 5
    IPinsHOffset = pin_h_off
    OPinsHOffset = -pin_h_off
    middlePinsVOffset = 30
    lastPinsVOffset = -10

    path_color_being_connected = QtGui.QColor(38, 83, 181)
    path_color_connected = QtGui.QColor(166, 27, 78)
    pin_being_connected_color = QtGui.QColor(96, 98, 168)
    pin_border_color_being_connected_color = QtGui.QColor(38, 83, 181)
    pin_connected_color = QtGui.QColor(166, 27, 78)
    pin_border_color = QtGui.QColor(158, 55, 60)

    distance_between_title_and_description = 30

    check_box_style = ("""
            QCheckBox::indicator {
                width: 35px;
                height: 35px;
            }
        """)
    progress_bar_style = ("""
     QProgressBar {
                border: 4px solid white;
                border-radius: 20px;
            }
             QProgressBar::grey {
        background-color: blue;
                }
""")
