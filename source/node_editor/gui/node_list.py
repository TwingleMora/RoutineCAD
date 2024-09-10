from PySide6 import QtCore, QtGui, QtWidgets
import sys
import importlib
import inspect

from PySide6.QtWidgets import QScrollBar


class NodeList(QtWidgets.QListWidget):
    #### MODIFY NODE
    #################################
    ############# 1 #################
    #################################
    modify_node = QtCore.Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : lightgreen;")
        self.setVerticalScrollBar(scroll_bar)
        self.setDragEnabled(False)  # enable dragging
        #self.setDragEnabled(True)  # enable dragging
        self.setMaximumHeight(50)

    def list_all_objects(self, nodes):
        for node in nodes:
            """
                self.Id = Id
                self.title_text = Name
                self.type_text = Description
                self.text = text
            """
            name = node.title_text + " [ " + str(node.Id) + " ] "
            item = QtWidgets.QListWidgetItem(name)
            item.module = node
            item.class_name = node.__class__
            self.addItem(item)

    def update_project(self, imports):
        # make an item for each custom  class

        for name, data in imports.items():
            name = name.replace("_Node", "")

            item = QtWidgets.QListWidgetItem(name)
            item.module = data["module"]
            item.class_name = data["class"]
            self.addItem(item)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        #item.__class__.delete()
        if item and item.text():
            name = item.text()

            #drag = QtGui.QDrag(self)
            #mime_data = QtCore.QMimeData()
            #mime_data.setText(name)
            #mime_data.item = item
            #drag.setMimeData(mime_data)
            for i in range(self.count()):
                self.item(i).module.setSelected(False)
            print(item.module.setSelected(True))

            # Drag needs a pixmap or else it'll error due to a null pixmap
            #pixmap = QtGui.QPixmap(16, 16)
            #pixmap.fill(QtGui.QColor("darkgray"))
            #pixmap.fill(QtGui.QColor("red"))
            #drag.setPixmap(pixmap)
            #drag.exec_()

            super().mousePressEvent(event)
    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.text():
            #### REQUEST NODE
            #################################
            ############# 2 #################
            #################################
            self.modify_node.emit(item.module)




