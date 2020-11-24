import pickle
from threading import Thread

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

from Roles.admin.design_admin import Ui_interface_admin
from Server_Client.Sockets import Client, Server
import asyncio
import pandas as pd
from datetime import datetime
import xlsxwriter

from gui_lib.Arc import Arc
from gui_lib.Canvas import Canvas, CANVAS_WORKING_MODE, MOUSE_BTN_MODE, Custom_label, Custom_line
from gui_lib.Net import Net
from gui_lib.Nodes import Node


class Admin(QtWidgets.QMainWindow, Ui_interface_admin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # инициализация сервера
        self.server = Server()
        self.setup_server()

        # Настройка карты
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 450)
        self.canvas = Canvas(self.centralwidget, self, CANVAS_WORKING_MODE.EDIT)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.net = Net({}, {}, {}, {}, {})
        self.canvas.setGeometry(QtCore.QRect(90, 79, 751, 291))
        self.canvas.setScene(self.scene)
        # Привязка событий нажатия
        self.add_computer_btn.clicked.connect(self.add_computer_btn_click)
        self.add_router_btn.clicked.connect(self.add_router_btn_click)
        self.add_commutator_btn.clicked.connect(self.add_commutator_btn_click)
        self.add_arc_btn.clicked.connect(self.add_arc_btn_click)
        self.save_btn.clicked.connect(self.save_btn_click)
        self.download_btn.clicked.connect(self.download_btn_click)
        self.send_btn.clicked.connect(self.send_btn_click)
        # сообщение
        self.pushButton_2.clicked.connect(self.send_btn_click)

    def add_computer_btn_click(self):
        self.canvas.reset_temp_data()
        self.canvas.mouse_btn_mode = MOUSE_BTN_MODE.ADD_COMPUTER
        self.enable_buttons()
        self.add_computer_btn.setEnabled(False)

    def add_router_btn_click(self):
        self.canvas.reset_temp_data()
        self.canvas.mouse_btn_mode = MOUSE_BTN_MODE.ADD_ROUTER
        self.enable_buttons()
        self.add_router_btn.setEnabled(False)

    def add_commutator_btn_click(self):
        self.canvas.reset_temp_data()
        self.canvas.mouse_btn_mode = MOUSE_BTN_MODE.ADD_COMMUTATOR
        self.enable_buttons()
        self.add_commutator_btn.setEnabled(False)

    def add_arc_btn_click(self):
        self.canvas.reset_temp_data()
        self.canvas.mouse_btn_mode = MOUSE_BTN_MODE.ADD_ARC
        self.enable_buttons()
        self.add_arc_btn.setEnabled(False)

    def enable_buttons(self):
        self.add_computer_btn.setEnabled(True)
        self.add_router_btn.setEnabled(True)
        self.add_commutator_btn.setEnabled(True)
        self.add_arc_btn.setEnabled(True)

    def save_btn_click(self):
        # отлов исключений
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Special Files (*.mlbin)",
                                                   options=options)
        if file_name:
            with open(file_name, 'wb') as file:
                pickle.dump(self.canvas.net, file)

    def download_btn_click(self):
        # отлов исключений
        self.canvas.reset_temp_data()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Special Files (*.mlbin)", options=options)
        if file_name:
            with open(file_name, 'rb') as file:
                Node.reset_counter()
                Arc.reset_counter()
                self.canvas.net = pickle.load(file)
                self.scene.clear()
                for key_node in self.canvas.net.nodes:
                    node = self.canvas.net.nodes[key_node]
                    pixmap = self.canvas.get_appropriate_pixmap(node.__class__)
                    custom_label = Custom_label(pixmap=pixmap, canvas=self.canvas, model_item=node)
                    self.canvas.scene().addWidget(custom_label)
                    self.canvas.scene().addWidget(custom_label.title)

                for key_arc in self.canvas.net.arcs:
                    arc = self.canvas.net.arcs[key_arc]
                    custom_line = Custom_line(canvas=self.canvas, model_item=arc,
                                              x1=arc.node_from.x, y1=arc.node_from.y,
                                              x2=arc.node_to.x, y2=arc.node_to.y)
                    self.canvas.scene().addItem(custom_line)

    # отправка карты и переход в не редактируемый режим
    def send_btn_click(self):
        self.hide_buttons()
        self.canvas.working_mode = CANVAS_WORKING_MODE.GAME
        net = pickle.dumps(self.canvas.net)
        # FIXME передать net всем игрокам в комнате


    # чатик
    def send_message(self):
        pass


    def hide_buttons(self):
        self.add_computer_btn.hide()
        self.add_router_btn.hide()
        self.add_commutator_btn.hide()
        self.add_arc_btn.hide()
        self.save_btn.hide()
        self.download_btn.hide()
        self.send_btn.hide()

    # Настройка сервера
    def setup_server(self):
        self.server.socket.bind(('127.0.0.1', 1234))
        self.server.socket.listen(3)
        self.server.socket.setblocking(False)
        print('Сервер запущен')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    admin = Admin()
    admin.show()
    server_thread = Thread(target=admin.server.start)
    server_thread.start()
    app.exec()


