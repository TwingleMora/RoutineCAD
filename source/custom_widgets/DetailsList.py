import datetime

from PySide6 import QtWidgets

from source.config import CONFIG
from source.custom_widgets.DetailsListItem import DetailsListItem
class DetailsList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def create_list(self,routine):
        for name, value in routine.__dict__.items():
            if name not in ["data", "routine_name", "routine_id"]:
                abstract_item = QtWidgets.QListWidgetItem()

                if isinstance(value, datetime.datetime):
                    value = value.strftime(CONFIG.dt_format)
                elif isinstance(value, int) or isinstance(value, float):
                    value = str(value)
                name = str.replace(name,"_"," ")

                list_item = DetailsListItem(name, value)
                abstract_item.setSizeHint(list_item.size())
                self.addItem(abstract_item)
                self.setItemWidget(abstract_item, list_item)
        pass

    def update_list(self, routine):
        self.clear()
        self.create_list(routine)
        pass