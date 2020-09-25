from PyQt5 import QtWidgets
import pickle

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

