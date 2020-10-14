from PyQt5 import QtWidgets
import pickle

import gui_lib.Node
import design_admin  # Это наш конвертированный файл дизайна
from gui_lib.Canvas import set_left_mouse_btn_mode, get_left_mouse_btn_mode,LEFT_MOUSE_BTN_MODE


class Interface_admin(QtWidgets.QMainWindow, design_admin.Ui_interface_admin):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.canvas = None

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

    def add_concentrator_btn_click(self):
        set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.ADD_CONCENTRATOR)
        self.enable_buttons()
        print("Add_concentrator_click() mode=", get_left_mouse_btn_mode())
        self.add_concentrator_btn.setEnabled(False)

    def enable_buttons(self):
        self.add_computer_btn.setEnabled(True)
        self.add_router_btn.setEnabled(True)
        self.add_commutator_btn.setEnabled(True)
        self.add_concentrator_btn.setEnabled(True)

    def send_btn_click(self):
        # TODO Сериализация и отправка
        with open('data.pickle', 'wb') as file:
            pickle.dump(gui_lib.nodes, file)

    def download_btn_click(self):
        with open('data.pickle', 'rb') as file:
            gui_lib.nodes = pickle.load(file)
            self.scene.clear()
            for node in gui_lib.nodes:
                self.scene.addEllipse(node.rect_ellipse)

