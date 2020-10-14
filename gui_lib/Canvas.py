from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView
from enum import Enum


# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    NOTHING = 0
    ADD_COMPUTER = 1
    ADD_ROUTER = 2
    ADD_COMMUTATOR = 3
    ADD_CONCENTRATOR = 4


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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMPUTER:
                # Добавить запоминание и все в отдельный метод
                point = self.mapToScene(event.pos())
                place = QtCore.QRectF(QtCore.QPointF(point.x(), point.y()), QtCore.QSizeF(15, 15))
                self.scene().addEllipse(place)
                return
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_ROUTER:
                pen = QtGui.QPen(QtCore.Qt.green)
                point = self.mapToScene(event.pos())
                place = QtCore.QRectF(QtCore.QPointF(point.x(), point.y()), QtCore.QSizeF(15, 15))
                self.scene().addEllipse(place, pen)
                return
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMMUTATOR:
                point = self.mapToScene(event.pos())
                place = QtCore.QRectF(QtCore.QPointF(point.x(), point.y()), QtCore.QSizeF(15, 15))
                self.scene().addRect(place)
                return
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_CONCENTRATOR:
                pen = QtGui.QPen(QtCore.Qt.green)
                point = self.mapToScene(event.pos())
                place = QtCore.QRectF(QtCore.QPointF(point.x(), point.y()), QtCore.QSizeF(15, 15))
                self.scene().addRect(place, pen)
                return

        if event.button() == Qt.RightButton:
            self.interface_admin.enable_buttons()
            set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.NOTHING)







