from PySide6 import QtCore, QtGui, QtWidgets
from source.config import CONFIG

class Pin_Graphics(QtWidgets.QGraphicsPathItem):
    def __init__(self, parent, scene):
        super().__init__(parent)
        self.being_connected = False
        self.radius_ = CONFIG.pin_radius
        self.margin = CONFIG.pin_margin

        self.execution = False

        path = QtGui.QPainterPath()
        #########################################################
        ##################### ADD THE CIRCUIT ###################
        #########################################################
        path.addEllipse(-self.radius_, -self.radius_, 2 * self.radius_, 2 * self.radius_)

        ##################################################
        ################# What's setPath()? ################
        ##################################################
        #setPath() is used to set the path of the item.

        self.setPath(path)

        self.setFlag(QtWidgets.QGraphicsPathItem.ItemSendsScenePositionChanges)
        font = CONFIG.pin_font

        self.font = QtGui.QFont(font)
        self.font_metrics = QtGui.QFontMetrics(self.font)

        self.pin_text_height = self.font_metrics.height()

        self.is_output = False
        self.margin = 2

        self.text_path = QtGui.QPainterPath()

    def set_execution(self, execution):
        if execution:
            path = QtGui.QPainterPath()

            points = []
            points.append(QtCore.QPointF(-6, -7))
            points.append(QtCore.QPointF(-6, 7))
            points.append(QtCore.QPointF(-2, 7))
            points.append(QtCore.QPointF(6, 0))
            points.append(QtCore.QPointF(-2, -7))
            points.append(QtCore.QPointF(-6, -7))
            path.addPolygon(QtGui.QPolygonF(points))
            self.setPath(path)

    def set_name(self, name):
        nice_name = self.name.replace("_", " ").title()

        self.pin_text_width = self.font_metrics.horizontalAdvance(nice_name)+CONFIG.NodePinTextMargin

        if self.is_output:
            x = -self.radius_ - self.margin - self.pin_text_width
        else:
            x = self.radius_ + self.margin

        y = self.pin_text_height / 4

        self.text_path.addText(x, y, self.font, nice_name)
    def is_connected(self):
        pass
    def is_being_connected(self):
        pass
    def paint(self, painter, option=None, widget=None):

        if self.execution:
            painter.setPen(QtCore.Qt.white)
        elif self.being_connected:
            qPenColor = CONFIG.pin_border_color_being_connected_color
            painter.setPen(QtGui.QPen(qPenColor, CONFIG.pin_thickness))
        else:
            #qPenColor =  QtCore.Qt.green
            qPenColor =  CONFIG.pin_border_color
            painter.setPen(QtGui.QPen(qPenColor, CONFIG.pin_thickness))

        if self.is_connected():
            if self.execution:
                painter.setBrush(QtCore.Qt.white)
            else:
                painter.setBrush(CONFIG.pin_connected_color)
        elif (self.being_connected):
            painter.setBrush(CONFIG.pin_being_connected_color)
        else:
            painter.setBrush(QtCore.Qt.NoBrush)

        painter.drawPath(self.path())

        # Draw text

        if not self.execution:
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtCore.Qt.white)
            painter.drawPath(self.text_path)

    def itemChange(self, change, value):
        """
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged and self.connection:
          self.connection.update_start_and_end_pos()

        """

        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged and self.connection:
            for con in self.connection:
                con.update_start_and_end_pos()
        """
        """
        return value
