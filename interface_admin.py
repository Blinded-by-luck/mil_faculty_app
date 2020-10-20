from PyQt5 import QtWidgets
import pickle

from PyQt5.QtCore import Qt

import design_admin  # Это наш конвертированный файл дизайна
from gui_lib.Arc import Arc
from gui_lib.Canvas import set_mouse_btn_mode, get_mouse_btn_mode,MOUSE_BTN_MODE
from gui_lib.Nodes import Node


class Interface_admin(QtWidgets.QMainWindow, design_admin.Ui_interface_admin):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

    def add_computer_btn_click(self):
        self.canvas.reset_temp_data()
        set_mouse_btn_mode(MOUSE_BTN_MODE.ADD_COMPUTER)
        self.enable_buttons()
        self.add_computer_btn.setEnabled(False)

    def add_router_btn_click(self):
        self.canvas.reset_temp_data()
        set_mouse_btn_mode(MOUSE_BTN_MODE.ADD_ROUTER)
        self.enable_buttons()
        self.add_router_btn.setEnabled(False)

    def add_commutator_btn_click(self):
        self.canvas.reset_temp_data()
        set_mouse_btn_mode(MOUSE_BTN_MODE.ADD_COMMUTATOR)
        self.enable_buttons()
        self.add_commutator_btn.setEnabled(False)

    def add_arc_btn_click(self):
        self.canvas.reset_temp_data()
        set_mouse_btn_mode(MOUSE_BTN_MODE.ADD_ARC)
        self.enable_buttons()
        self.add_arc_btn.setEnabled(False)

    def enable_buttons(self):
        self.add_computer_btn.setEnabled(True)
        self.add_router_btn.setEnabled(True)
        self.add_commutator_btn.setEnabled(True)
        self.add_arc_btn.setEnabled(True)

    def send_btn_click(self):
        with open('data.pickle', 'wb') as file:
            pickle.dump(self.canvas.net, file)

    def download_btn_click(self):
        self.canvas.reset_temp_data()
        # сделать диалоговое окно
        with open('data.pickle', 'rb') as file:
            Node.reset_counter()
            Arc.reset_counter()
            self.canvas.net = pickle.load(file)
            self.scene.clear()
            for key_node in self.canvas.net.nodes:
                node = self.canvas.net.nodes[key_node]
                pixmap = self.canvas.get_appropriate_pixmap(node)
                custom_label = self.canvas.place_node(pixmap, node.x, node.y)
                node.custom_widget = custom_label
                custom_label.model_item = node
            # отображение ребер

