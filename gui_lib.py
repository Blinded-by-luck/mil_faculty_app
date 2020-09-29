from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsEllipseItem
from enum import Enum


# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    NOTHING = 0
    ADD = 1

left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING

nodes = []


class Canvas(QGraphicsView):
    def __init__(self, parent=None, root=None):
        QGraphicsView.__init__(self, parent=parent)

        self.interface_admin = root

    def mousePressEvent(self, event):
        global left_mouse_btn_mode, nodes
        if event.button() == Qt.LeftButton & (left_mouse_btn_mode == LEFT_MOUSE_BTN_MODE.ADD):
            # pen = QtGui.QPen(QtCore.Qt.green)
            # Добавить запоминание и все в отдельный метод
            point = self.mapToScene(event.pos())
            node = Node(x=point.x(), y=point.y())
            nodes.append(node)
            self.scene().addEllipse(node.rect_ellipse)
            print("An event occurred")
            return
        if event.button() == Qt.RightButton:
            self.interface_admin.enable_buttons()
            left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING


class Node:
    def __init__(self, x=0, y=0, width=20, height=20):
        self.rect_ellipse = QRectF(x, y, width, height)

    def __getstate__(self):
        data = [self.rect_ellipse.x(), self.rect_ellipse.y()]
        return data

    def __setstate__(self, value):
        self.__init__(x=value[0], y=value[1])




