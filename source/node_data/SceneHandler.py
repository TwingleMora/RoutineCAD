from source.custom_nodes.Custom_node import Custom_Node
from source.node_editor.connection import Connection
from source.node_editor.pin import Pin


class SceneHandler:
    def __init__(self, scene):
        self.scene = scene
        self.node_lookup = {}
        pass

    def load_scene(self, json_data, imports=None):
        # load the scene json file
        data = None
        # with open(json_path) as f:
        #     data = json.load(f)

        # clear out the node lookup
        node_item = None
        self.node_lookup = {}
        data = json_data
        # Add the nodes
        if data:
            for node in data["nodes"]:
                #info = imports[node["type"]]
                #info = None
                if (node["type"]) == "Custom_Node":
                    node_item = Custom_Node(node["title_text"], node["description_text"], node["text"], node["id"],int(node["current"]),int(node["target"]))

                #node_item = info["class"]()
                if node_item:
                    node_item.uuid = node["uuid"]
                    self.scene.addItem(node_item)
                    node_item.setPos(node["x"], node["y"])

                    self.node_lookup[node["uuid"]] = node_item
                    #node_lookup is array of Scaler_Node, Add_Node, Output_Node, Button_Node
                    #they all have things in common like: get_pin
        # Add the connections
        for c in data["connections"]:
            connection = Connection(None)
            self.scene.addItem(connection)

            start_pin = self.node_lookup[c["start_id"]].get_pin(c["start_pin"])
            end_pin = self.node_lookup[c["end_id"]].get_pin(c["end_pin"])

            print("start_pin", start_pin)

            if start_pin:
                connection.set_start_pin(start_pin)

            if end_pin:
                connection.set_end_pin(end_pin)
            connection.update_start_and_end_pos()

    def convert_to_json(self,save_iterations=False):
        scene = {"nodes": [], "connections": []}

        # Need the nodes, and connections of ports to nodes
        _mItems = self.scene.items()
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
            #if isinstance(item, Custom_Node):
            if isinstance(item, Custom_Node): #or isinstance(item, Custom_Node):
                id = item.Id
                text = item.text
                title_text = item.title_text
                description_text = item.type_text
                if(save_iterations):
                    current_iteration = item.current_iteration
                else:
                    current_iteration = item.last_iteration
                target_iteration = item.target_iteration


                current_score = item
                # print("found node")
                pos = item.pos().toPoint()
                x, y = pos.x(), pos.y()
                # print(f"pos: {x, y}")

                obj_type = type(item).__name__
                # print(f"node type: {obj_type}")

                node_id = str(item.uuid)

                node = {"type": obj_type, "x": x, "y": y, "id": id, "uuid": node_id, "title_text": title_text,
                        "description_text": description_text, "text": text, "current": current_iteration, "target": target_iteration}
                scene["nodes"].append(node)

        return scene
