from PyQt5 import QtWidgets
import pickle

import design_admin  # Это наш конвертированный файл дизайна
from gui_lib.Canvas import set_left_mouse_btn_mode, get_left_mouse_btn_mode,LEFT_MOUSE_BTN_MODE
from gui_lib.Nodes import get_appropriate_pixmap


class Interface_admin(QtWidgets.QMainWindow, design_admin.Ui_interface_admin):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

    def add_computer_btn_click(self):
        set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.ADD_COMPUTER)
        self.enable_buttons()
        print("Add_computer_click() mode=", get_left_mouse_btn_mode())
        self.add_computer_btn.setEnabled(False)

    def add_router_btn_click(self):
        set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.ADD_ROUTER)
        self.enable_buttons()
        print("Add_router_click() mode=", get_left_mouse_btn_mode())
        self.add_router_btn.setEnabled(False)

    def add_commutator_btn_click(self):
        set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.ADD_COMMUTATOR)
        self.enable_buttons()
        print("Add_commutator_click() mode=", get_left_mouse_btn_mode())
        self.add_commutator_btn.setEnabled(False)

    def enable_buttons(self):
        self.add_computer_btn.setEnabled(True)
        self.add_router_btn.setEnabled(True)
        self.add_commutator_btn.setEnabled(True)

    def send_btn_click(self):
        with open('data.pickle', 'wb') as file:
            pickle.dump(self.net, file)

    def download_btn_click(self):
        # даилоговое окно
        with open('data.pickle', 'rb') as file:
            self.net = pickle.load(file)
            self.scene.clear()
            # добавить отображение компов, потом ребер
            for key_node in self.net.nodes:
                node = self.net.nodes[key_node]
                pixmap = get_appropriate_pixmap(node)
                if pixmap.isNull():
                    print("not load")
                    return
                pixmap_item = self.canvas.place_node(pixmap, node.x, node.y)
                node.pixmap_item = pixmap_item

