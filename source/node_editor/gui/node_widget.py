import json
import uuid
import random

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGraphicsView, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QToolBar

from source.node_editor.gui.node_editor import NodeEditor
from source.node_editor.gui.view import View

from source.node_editor.connection import Connection
from source.node_editor.node import Node
from source.node_editor.pin import Pin
from source.config import CONFIG

class NodeScene(QtWidgets.QGraphicsScene):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos())
        if item.setAcceptDrops:
            # pass on event to item at the coordinates
            item.dropEvent(e)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()
        print("dragMoveEvent")


class NodeWidget(QtWidgets.QWidget):
    """
    Widget for creating and displaying a node editor.

    Attributes:
        node_editor (NodeEditor): The node editor object.
        scene (NodeScene): The scene object for the node editor.
        view (View): The view object for the node editor.
    """

    def __init__(self, parent):
        """
        Initializes the NodeWidget object.

        Args:
            parent (QWidget): The parentItem widget.
        """
        view = None
        super().__init__(parent)

        self.node_lookup = {}  # A dictionary of nodes, by uuids for faster looking up. Refactor this in the future
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.scene = NodeScene()  # scene = NodeScene(self)
        self.scene.setSceneRect(0, 0, 99999, 99999)  # scene.setSceneRect(0, 0, 9999, 9999)
        #self.sceneHandler = SceneHandler(self.scene)

        self.view = View(self)
        self.view.setScene(self.scene)
        self.node_editor = NodeEditor(self)
        self.node_editor.install(self.scene)
        self.view.scale(CONFIG.intial_scale_factor, CONFIG.intial_scale_factor)
        self.view.horizontalScrollBar().setMaximum(99999)
        self.view.verticalScrollBar().setMaximum(99999)
        self.view.horizontalScrollBar().setValue(5593)
        self.view.verticalScrollBar().setValue(5786)
        #H: 5844
        #V: 5504
        #self.view.scale(0.25,0.25)





        ###################################
        ####################################

        # Create a floating toolbar
        self.toolbar = QToolBar("Floating Toolbar")
        self.toolbar.setFloatable(True)  # Allows the toolbar to be movable
        self.toolbar.setMovable(True)

        # Add actions (buttons) to the toolbar
        action_select = QAction("Select", self)
        action_pan = QAction("Pan", self)
        self.toolbar.addAction(action_select)
        self.toolbar.addAction(action_pan)

        # Connect actions to functionality
        action_select.triggered.connect(lambda: self.view.setDragMode(QGraphicsView.RubberBandDrag))
        action_pan.triggered.connect(lambda: self.view.setDragMode(QGraphicsView.ScrollHandDrag))

        # Layout for the window
        #layout = QVBoxLayout()
        #layout.addWidget(self.view)
        #layout.addWidget(self.toolbar)

        # Set layout for the main window
        #self.setLayout(layout)

        # Set the initial drag mode to RubberBandDrag
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        ####################################
        ####################################

        self.view.centerOn(self.scene.sceneRect().center())

        main_layout.addWidget(self.view)
        main_layout.addWidget(self.toolbar)
        #### REQUEST NODE
        #################################
        ############# 3 #################
        #################################
        self.view.request_node.connect(self.create_node)

    def create_node(self, node):
        node.uuid = uuid.uuid4()
        self.scene.addItem(node)  #add item to scene
        pos = self.view.mapFromGlobal(QtGui.QCursor.pos())
        node.setPos(self.view.mapToScene(pos))

    def create_custom_node(self, node):
        node.uuid = uuid.uuid4()
        self.scene.addItem(node)  #add item to scene
        pos = self.view.rect().center()
        pos = QtCore.QPoint(pos.x() + random.randrange(-100, 100), pos.y() + random.randrange(-100, 100))  #pos = QtCore.QPoint(pos.x() + random.random() * 100, pos.y() + random.random() * 100)
        node.setPos(self.view.mapToScene(pos))

    # def load_scene(self, json_data, imports=None):
    #     # load the scene json file
    #     data = None
    #     # with open(json_path) as f:
    #     #     data = json.load(f)
    #
    #     # clear out the node lookup
    #     node_item = None
    #     self.node_lookup = {}
    #     data = json_data
    #     # Add the nodes
    #     if data:
    #         for node in data["nodes"]:
    #             #info = imports[node["type"]]
    #             #info = None
    #             if (node["type"]) == "Scaler_Node":
    #                 node_item = Scaler_Node()
    #             elif (node["type"]) == "Add_Node":
    #                 node_item = Add_Node()
    #             elif (node["type"]) == "Print_Node":
    #                 node_item = Print_Node()
    #             elif (node["type"]) == "Button_Node":
    #                 node_item = Button_Node()
    #             elif (node["type"]) == "Custom_Node":
    #                 node_item = Custom_Node(node["title_text"], node["description_text"], node["text"], node["id"])
    #
    #             #node_item = info["class"]()
    #             if node_item:
    #                 node_item.uuid = node["uuid"]
    #                 self.scene.addItem(node_item)
    #                 node_item.setPos(node["x"], node["y"])
    #
    #                 self.node_lookup[node["uuid"]] = node_item
    #                 #node_lookup is array of Scaler_Node, Add_Node, Output_Node, Button_Node
    #                 #they all have things in common like: get_pin
    #     # Add the connections
    #     for c in data["connections"]:
    #         connection = Connection(None)
    #         self.scene.addItem(connection)
    #
    #         start_pin = self.node_lookup[c["start_id"]].get_pin(c["start_pin"])
    #         end_pin = self.node_lookup[c["end_id"]].get_pin(c["end_pin"])
    #
    #         print("start_pin", start_pin)
    #
    #         if start_pin:
    #             connection.set_start_pin(start_pin)
    #
    #         if end_pin:
    #             connection.set_end_pin(end_pin)
    #         connection.update_start_and_end_pos()
    #
    # def convert_to_json(self):
    #     scene = {"nodes": [], "connections": []}
    #
    #     # Need the nodes, and connections of ports to nodes
    #     _mItems = self.scene.items()
    #     for item in self.scene.items():
    #         # Connections
    #         if isinstance(item, Connection):
    #             # print(f"Name: {item}")
    #             nodes = item.nodes()
    #             start_id = str(nodes[0].uuid)
    #             end_id = str(nodes[1].uuid)
    #             start_pin = item.start_pin.name
    #             end_pin = item.end_pin.name
    #             # print(f"Node ids {start_id, end_id}")
    #             # print(f"connected ports {item.start_pin.name(), item.end_pin.name()}")
    #
    #             connection = {
    #                 "start_id": start_id,
    #                 "end_id": end_id,
    #                 "start_pin": start_pin,
    #                 "end_pin": end_pin,
    #             }
    #             scene["connections"].append(connection)
    #             continue
    #
    #         # Pins
    #         if isinstance(item, Pin):
    #             continue
    #
    #         # Nodes
    #         #if isinstance(item, Custom_Node):
    #         if isinstance(item, Node):
    #             id = item.Id
    #             text = item.text
    #             title_text = item.title_text
    #             description_text = item.type_text
    #             # print("found node")
    #             pos = item.pos().toPoint()
    #             x, y = pos.x(), pos.y()
    #             # print(f"pos: {x, y}")
    #
    #             obj_type = type(item).__name__
    #             # print(f"node type: {obj_type}")
    #
    #             node_id = str(item.uuid)
    #
    #             node = {"type": obj_type, "x": x, "y": y, "id": id, "uuid": node_id, "title_text": title_text,
    #                     "description_text": description_text, "text": text}
    #             scene["nodes"].append(node)
    #
    #     return scene

    def save_project(self, json_path):

        # TODO possibly an ordered dict so things stay in order (better for git changes, and manual editing)
        # Maybe connections will need a uuid for each so they can be sorted and kept in order.
        scene = {"nodes": [], "connections": []}

        # Need the nodes, and connections of ports to nodes
        for item in self.scene.items():
            # Connections
            if isinstance(item, Connection):
                # print(f"Name: {item}")
                nodes = item.nodes()
                start_id = str(nodes[0].uuid)
                end_id = str(nodes[1].uuid)
                start_pin = item.start_pin.name
                end_pin = item.end_pin.name
                # print(f"Node ids {start_id, end_id}")
                # print(f"connected ports {item.start_pin.name(), item.end_pin.name()}")

                connection = {
                    "start_id": start_id,
                    "end_id": end_id,
                    "start_pin": start_pin,
                    "end_pin": end_pin,
                }
                scene["connections"].append(connection)
                continue

            # Pins
            if isinstance(item, Pin):
                continue

            # Nodes
            if isinstance(item, Node):
                id = item.Id
                text = item.text
                title_text = item.title_text
                description_text = item.type_text
                # print("found node")
                pos = item.pos().toPoint()
                x, y = pos.x(), pos.y()
                # print(f"pos: {x, y}")

                obj_type = type(item).__name__
                # print(f"node type: {obj_type}")

                node_id = str(item.uuid)

                node = {"type": obj_type, "x": x, "y": y, "id": id, "uuid": node_id, "title_text": title_text,
                        "description_text": description_text, "text": text}
                scene["nodes"].append(node)

        # Write the items_info dictionary to a JSON file
        with open(json_path, "w") as f:
            json.dump(scene, f, indent=4)
