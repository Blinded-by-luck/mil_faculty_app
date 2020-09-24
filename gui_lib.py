from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QWidget
from enum import Enum
#from interface_admin import

# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    NOTHING = 0
    ADD = 1

left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.interface_admin = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.LeftButton & (left_mouse_btn_mode == LEFT_MOUSE_BTN_MODE.ADD):
            print("An event occurred")
            return
        if event.key() == Qt.RightButton:
            self.interface_admin.enable_buttons()
