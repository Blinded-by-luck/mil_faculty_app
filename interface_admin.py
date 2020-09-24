from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

import gui_lib
import design_admin  # Это наш конвертированный файл дизайна


class Interface_admin(QtWidgets.QMainWindow, design_admin.Ui_interface_admin):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.canvas = None


    def add_node_btn_click(self):
        gui_lib.left_mouse_btn_mode = gui_lib.LEFT_MOUSE_BTN_MODE.ADD
        self.enable_buttons()
        print("Add node click")
        self.add_node_btn.setEnabled(False)

    def enable_buttons(self):
        self.add_node_btn.setEnabled(True)

