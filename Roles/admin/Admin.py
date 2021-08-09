import pickle
from threading import Thread

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication

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


class Admin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # инициализация сервера
        self.server = Server()
        self.setup_server()

        # Отрисовка
        self.setObjectName("interface_admin")
        desktop_rect = QApplication.desktop().availableGeometry()
        self.resize(desktop_rect.width(), desktop_rect.height())
        self.move(desktop_rect.left(), desktop_rect.top())
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background: #fffdf5;")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setObjectName("stackedWidget")
        # self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1020, 723))
        self.setCentralWidget(self.stackedWidget)

        self.room_widget = QtWidgets.QWidget()
        self.room_widget.setObjectName("room_widget")
        self.stackedWidget.addWidget(self.room_widget)

        self.main_layout_room = QtWidgets.QVBoxLayout()
        self.main_layout_room.setContentsMargins(0, 0, 0, 0)
        self.main_layout_room.setObjectName("main_layout_room")

        self.room_widget.setLayout(self.main_layout_room)

        self.horizontal_up_layout_room = QtWidgets.QHBoxLayout()
        self.horizontal_up_layout_room.setContentsMargins(20, 20, 20, 10)
        self.horizontal_up_layout_room.setObjectName("horizontal_up_layout_room")

        self.horizontal_med_layout_room = QtWidgets.QHBoxLayout()
        self.horizontal_med_layout_room.setContentsMargins(-1, -1, 20, -1)
        self.horizontal_med_layout_room.setObjectName("horizontal_med_layout_room")

        self.vertical_down_layout_room = QtWidgets.QVBoxLayout()
        self.vertical_down_layout_room .setContentsMargins(20, -1, 20, -1)
        self.vertical_down_layout_room.setObjectName("vertical_down_layout_room")

        self.main_layout_room.addLayout(self.horizontal_up_layout_room)
        self.main_layout_room.addLayout(self.horizontal_med_layout_room)
        self.main_layout_room.addLayout(self.vertical_down_layout_room)

        # horizontal_up_layout_room content
        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_btn_click)
        self.save_btn.setStyleSheet("QPushButton {background: #03a9f4;                  \
                                    color: #fff; border-radius: 15px;                   \
                                    font-size: 12pt;                                    \
                                    font-family: Century Gothic, sans-serif;}           \
                                    QPushButton:hover {background-color:#64bee8;}       \
                                    QPushButton:pressed {background-color:#03a9f4;}")

        self.download_btn = QtWidgets.QPushButton()
        self.download_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.download_btn.setObjectName("download_btn")
        self.download_btn.clicked.connect(self.download_btn_click)
        self.download_btn.setStyleSheet("QPushButton {background: #03a9f4;                  \
                                        color: #fff; border-radius: 15px;                   \
                                        font-size: 12pt;                                    \
                                        font-family: Century Gothic, sans-serif;}           \
                                        QPushButton:hover {background-color:#64bee8;}       \
                                        QPushButton:pressed {background-color:#03a9f4;}")

        self.send_btn = QtWidgets.QPushButton()
        self.send_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.send_btn.setObjectName("send_btn")
        self.send_btn.clicked.connect(self.send_btn_click)
        self.send_btn.setStyleSheet("QPushButton {background: #03a9f4;                  \
                                    color: #fff; border-radius: 15px;                   \
                                    font-size: 12pt;                                    \
                                    font-family: Century Gothic, sans-serif;}           \
                                    QPushButton:hover {background-color:#64bee8;}       \
                                    QPushButton:pressed {background-color:#03a9f4;}")

        self.horizontal_up_layout_room.addWidget(self.save_btn)
        self.horizontal_up_layout_room.addWidget(self.download_btn)
        self.horizontal_up_layout_room.addWidget(self.send_btn)

        # horizontal_med_layout_room content
        self.vertical_med_layout_room = QtWidgets.QVBoxLayout()
        self.vertical_med_layout_room.setContentsMargins(0, 0, 10, 0)
        self.vertical_med_layout_room.setObjectName("vertical_med_layout_room")
        self.vertical_med_layout_room.addStretch()

        self.scene = QtWidgets.QGraphicsScene()
        # self.scene.setSceneRect(0, 0, 800, 300)
        self.canvas = Canvas(self.stackedWidget, self, CANVAS_WORKING_MODE.EDIT)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.canvas.setGeometry(QtCore.QRect(90, 79, 750, 250))
        self.canvas.setScene(self.scene)

        self.horizontal_med_layout_room.addLayout(self.vertical_med_layout_room)
        self.horizontal_med_layout_room.addWidget(self.canvas)

        # vertical_med_layout_room content
        self.lower_spacer_room = QtWidgets.QSpacerItem(10, desktop_rect.height(),
                                                       QtWidgets.QSizePolicy.Preferred,
                                                       QtWidgets.QSizePolicy.MinimumExpanding)

        self.add_computer_btn = QtWidgets.QPushButton()
        self.add_computer_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_computer_btn.setMaximumSize(QtCore.QSize(40, 50))
        self.add_computer_btn.setStyleSheet("")
        self.add_computer_btn.setText("")
        icon = QIcon()
        icon.addPixmap(self.canvas.computer_pixmap, QIcon.Normal, QIcon.Off)
        self.add_computer_btn.setIcon(icon)
        self.add_computer_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_computer_btn.setObjectName("add_computer_btn")
        self.add_computer_btn.clicked.connect(self.add_computer_btn_click)

        self.add_router_btn = QtWidgets.QPushButton()
        self.add_router_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_router_btn.setMaximumSize(QtCore.QSize(40, 50))
        self.add_router_btn.setStyleSheet("")
        self.add_router_btn.setText("")
        icon = QIcon()
        icon.addPixmap(self.canvas.router_pixmap, QIcon.Normal, QIcon.Off)
        self.add_router_btn.setIcon(icon)
        self.add_router_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_router_btn.setObjectName("add_router_btn")
        self.add_router_btn.clicked.connect(self.add_router_btn_click)

        self.add_commutator_btn = QtWidgets.QPushButton()
        self.add_commutator_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_commutator_btn.setMaximumSize(QtCore.QSize(40, 50))
        self.add_commutator_btn.setStyleSheet("")
        self.add_commutator_btn.setText("")
        icon = QIcon()
        icon.addPixmap(self.canvas.commutator_pixmap, QIcon.Normal, QIcon.Off)
        self.add_commutator_btn.setIcon(icon)
        self.add_commutator_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_commutator_btn.setObjectName("add_commutator_btn")
        self.add_commutator_btn.clicked.connect(self.add_commutator_btn_click)

        self.add_arc_btn = QtWidgets.QPushButton()
        self.add_arc_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_arc_btn.setMaximumSize(QtCore.QSize(40, 50))
        self.add_arc_btn.setStyleSheet("")
        self.add_arc_btn.setText("")
        icon = QIcon()
        icon.addPixmap(self.canvas.arc_pixmap, QIcon.Normal, QIcon.Off)
        self.add_arc_btn.setIcon(icon)
        self.add_arc_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_arc_btn.setObjectName("add_arc_btn")
        self.add_arc_btn.clicked.connect(self.add_arc_btn_click)

        self.vertical_med_layout_room.addWidget(self.add_computer_btn)
        self.vertical_med_layout_room.addWidget(self.add_router_btn)
        self.vertical_med_layout_room.addWidget(self.add_commutator_btn)
        self.vertical_med_layout_room.addWidget(self.add_arc_btn)
        self.vertical_med_layout_room.addSpacerItem(self.lower_spacer_room)

        # vertical_down_layout content
        self.log_widget = QtWidgets.QTextBrowser()
        self.log_widget.setMinimumSize(QtCore.QSize(500, 200))
        self.log_widget.setMaximumSize(QtCore.QSize(self.width(), 200))
        self.log_widget.setObjectName("log_widget")
        self.log_widget.setStyleSheet("background: #edfcff; font-size: 12pt;"
                                      "font-family: Century Gothic, sans-serif;")

        self.vertical_down_layout_room.addWidget(self.log_widget)

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("interface_admin", "Проект"))
        self.save_btn.setText(_translate("interface_admin", "Сохранить карту"))
        self.download_btn.setText(_translate("interface_admin", "Загрузить карту"))
        self.send_btn.setText(_translate("interface_admin", "Отправить карту"))

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
                                              x1=arc.node_from.x + self.canvas.computer_pixmap.width() / 2,
                                              y1=arc.node_from.y + self.canvas.computer_pixmap.height() / 2,
                                              x2=arc.node_to.x + self.canvas.computer_pixmap.width() / 2,
                                              y2=arc.node_to.y + self.canvas.computer_pixmap.height() / 2)
                    self.canvas.scene().addItem(custom_line)

    # отправка карты и переход в не редактируемый режим
    def send_btn_click(self):
        self.hide_buttons()
        self.canvas.working_mode = CANVAS_WORKING_MODE.GAME
        net = pickle.dumps(self.canvas.net)
        for user in self.server.users:
            user.sendall(net)
        # FIXME передать net всем игрокам в комнате

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
        # self.server.socket.bind(('172.18.7.101', 1234))
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


