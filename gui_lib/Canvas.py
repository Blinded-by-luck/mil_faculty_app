from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView
from enum import Enum

from gui_lib.Nodes import Computer
from gui_lib.Nodes import Router
from gui_lib.Nodes import Commutator
from gui_lib.Nodes import Node

# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    NOTHING = 0
    ADD_COMPUTER = 1
    ADD_ROUTER = 2
    ADD_COMMUTATOR = 3


left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING


def get_left_mouse_btn_mode():
    return left_mouse_btn_mode


def set_left_mouse_btn_mode(value):
    global left_mouse_btn_mode
    left_mouse_btn_mode = value


class Canvas(QGraphicsView):
    def __init__(self, parent=None, root=None):
        QGraphicsView.__init__(self, parent=parent)

        self.interface_admin = root

    def place_node(self, pixmap, x, y):
        pixmap_item = self.scene().addPixmap(pixmap)
        size = pixmap_item.pixmap().size()
        pixmap_item.setPos(
            x - size.width() / 2,
            y - size.height() / 2
        )
        return pixmap_item

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('count nodes before =', len(self.interface_admin.net.nodes))
            print('Node.Counter before =', Node.Counter)
            point = self.mapToScene(event.pos())
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMPUTER:
                pixmap = QPixmap('Models\\Computer.png')
                if pixmap.isNull():
                    print("not load")
                    return
                pixmap_item = self.place_node(pixmap, point.x(), point.y())
                node = Computer(pixmap_item.x(), pixmap_item.y(), [], [], pixmap_item)
                self.interface_admin.net.add_node(node)
                return

            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_ROUTER:
                pixmap = QPixmap('Models\\Router.png')
                if pixmap.isNull():
                    print("not load")
                    return
                pixmap_item = self.place_node(pixmap, point.x(), point.y())
                node = Router(pixmap_item.x(), pixmap_item.y(), [], [], pixmap_item)
                self.interface_admin.net.add_node(node)
                return

            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMMUTATOR:
                pixmap = QPixmap('Models\\Commutator.png')
                if pixmap.isNull():
                    print("not load")
                    return
                pixmap_item = self.place_node(pixmap, point.x(), point.y())
                node = Commutator(pixmap_item.x(), pixmap_item.y(), [], [], pixmap_item)
                self.interface_admin.net.add_node(node)
                return

        if event.button() == Qt.RightButton:
            self.interface_admin.enable_buttons()
            set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.NOTHING)
