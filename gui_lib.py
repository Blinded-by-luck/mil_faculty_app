from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView
from enum import Enum

# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    NOTHING = 0
    ADD = 1

left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING

class Canvas(QGraphicsView):
    def __init__(self, parent=None, root=None):
        QGraphicsView.__init__(self, parent=parent)
        self.interface_admin = root

    def mousePressEvent(self, event):
        global left_mouse_btn_mode
        if event.button() == Qt.LeftButton & (left_mouse_btn_mode == LEFT_MOUSE_BTN_MODE.ADD):
            pen = QtGui.QPen(QtCore.Qt.green)
            # Добавить запоминание и все в отдельный метод
            rect = QtCore.QRectF(self.mapToScene(event.pos()), QtCore.QSizeF(20, 20))
            self.scene().addRect(rect, pen)
            print("An event occurred")
            return
        if event.button() == Qt.RightButton:
            self.interface_admin.enable_buttons()
            left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.NOTHING



