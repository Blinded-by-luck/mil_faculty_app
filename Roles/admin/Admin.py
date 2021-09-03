import pickle
from functools import partial
from threading import Thread

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFileDialog, QApplication, QTableView, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QSizePolicy
from PyQt5.QtCore import Qt, QSize

#from Roles.admin.design_admin import Ui_interface_admin
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
        # Отрисовка
        self.setObjectName("interface_admin")
        desktop_rect = QApplication.desktop().availableGeometry()
        self.resize(desktop_rect.width(), desktop_rect.height())
        self.move(desktop_rect.left(), desktop_rect.top())
        self.setMinimumSize(1320, 800)
        self.setStyleSheet("background: #fffdf5;")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.current_room = -1

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")
        self.setCentralWidget(self.stacked_widget)

        # stacked_widget content
        self.hall_widget = QtWidgets.QWidget()
        self.hall_widget.setObjectName("hall_widget")
        self.hall_widget.setStyleSheet("border: 0px")

        self.room_widget = QtWidgets.QWidget()
        self.room_widget.setObjectName("room_widget")
        self.room_widget.setStyleSheet("border: 0px")

        self.stacked_widget.addWidget(self.hall_widget)
        self.stacked_widget.addWidget(self.room_widget)
        # end stacked_widget content

        # hall_widget content
        self.main_layout_hall = QtWidgets.QVBoxLayout()
        self.main_layout_hall.setObjectName("main_layout_hall")
        self.main_layout_hall.setContentsMargins(0, 0, 0, 0)

        self.hall_widget.setLayout(self.main_layout_hall)
        # end hall_widget content

        # main_layout_hall content
        self.horizontal_up_layout_hall = QtWidgets.QHBoxLayout()
        self.horizontal_up_layout_hall.setObjectName("horizontal_up_layout_hall")

        self.grid_layout_hall = QtWidgets.QGridLayout()
        self.grid_layout_hall.setObjectName("grid_layout_hall")

        self.main_layout_hall.addLayout(self.horizontal_up_layout_hall)
        self.main_layout_hall.addLayout(self.grid_layout_hall)
        # end main_layout_hall content

        # horizontal_up_layout_hall content
        self.header_hall = QtWidgets.QTextEdit()
        self.header_hall.setObjectName("header_hall")
        self.header_hall.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.header_hall.setText("Холл")
        self.header_hall.setAlignment(Qt.AlignCenter)
        self.header_hall.setReadOnly(True)
        self.header_hall.setStyleSheet("font-size: 32pt;"
                                       "color: green;")
        self.horizontal_up_layout_hall.addWidget(self.header_hall)
        # end horizontal_up_layout_hall content

        # grid_layout_hall content
        self.room_tables = np.empty(12, dtype=QTableWidget)
        font = QFont("Helvetica", 18)

        for i in range(self.room_tables.size):
            table = QTableWidget()
            table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QAbstractItemView.NoSelection)
            table.setShowGrid(False)
            table.setRowCount(3)
            table.setColumnCount(1)
            table.verticalHeader().hide()
            table.horizontalHeader().hide()
            table.setStyleSheet(":item { border: 2px solid grey; }")
            table.cellClicked.connect(partial(self.cell_clicked, i))

            item = QTableWidgetItem("Комната № " + str(i + 1))
            item.setToolTip("Перейти в комнату")
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)

            item = QTableWidgetItem("Проскурин Валерий Геннадьевич")
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(1, 0, item)

            item = QTableWidgetItem("ФИО 2 игрока")
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(2, 0, item)

            table.resizeColumnsToContents()
            table.resizeRowsToContents()

            self.grid_layout_hall.addWidget(table, i // 3, i % 3, alignment=Qt.AlignCenter)
            self.room_tables[i] = table
        # end grid_layout_hall content

        # room_widget content
        self.main_layout_room = QtWidgets.QVBoxLayout()
        self.main_layout_room.setObjectName("main_layout_room")
        self.main_layout_room.setContentsMargins(0, 0, 0, 0)

        self.room_widget.setLayout(self.main_layout_room)
        # end room_widget content

        # main_layout_room content
        self.vertical_up_layout_room = QtWidgets.QVBoxLayout()
        self.vertical_up_layout_room.setObjectName("vertical_up_layout_room")
        self.vertical_up_layout_room.setContentsMargins(20, 20, 20, 10)

        self.horizontal_med_layout_room = QtWidgets.QHBoxLayout()
        self.horizontal_med_layout_room.setObjectName("horizontal_med_layout_room")
        self.horizontal_med_layout_room.setContentsMargins(0, 0, 20, 0)

        self.vertical_down_layout_room = QtWidgets.QVBoxLayout()
        self.vertical_down_layout_room.setObjectName("vertical_down_layout_room")
        self.vertical_down_layout_room .setContentsMargins(20, 0, 20, 0)

        self.main_layout_room.addLayout(self.vertical_up_layout_room)
        self.main_layout_room.addLayout(self.horizontal_med_layout_room)
        self.main_layout_room.addLayout(self.vertical_down_layout_room)
        # end main_layout_room content

        # vertical_up_layout content
        self.horizontal_up_header_layout_room = QtWidgets.QHBoxLayout()
        self.horizontal_up_header_layout_room.setObjectName("horizontal_up_header_layout_room")

        self.horizontal_up_layout_room = QtWidgets.QHBoxLayout()
        self.horizontal_up_layout_room.setObjectName("horizontal_up_layout_room")

        self.vertical_up_layout_room.addLayout(self.horizontal_up_header_layout_room)
        self.vertical_up_layout_room.addLayout(self.horizontal_up_layout_room)
        # end vertical_up_layout content

        # horizontal_up_header_layout_room content
        self.return_btn = QtWidgets.QPushButton()
        self.return_btn.setObjectName("return_btn")
        self.return_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.return_btn.clicked.connect(self.return_btn_click)
        self.return_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.return_btn.setStyleSheet("QPushButton {background: #03a9f4;                \
                                    color: #fff; border-radius: 15px;                   \
                                    font-size: 12pt;                                    \
                                    font-family: Century Gothic, sans-serif;}           \
                                    QPushButton:hover {background-color:#64bee8;}       \
                                    QPushButton:pressed {background-color:#03a9f4;}")

        self.header_room_table = QTableWidget()
        self.header_room_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.header_room_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.header_room_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.header_room_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.header_room_table.setShowGrid(False)
        self.header_room_table.setRowCount(2)
        self.header_room_table.setColumnCount(2)
        self.header_room_table.verticalHeader().hide()
        self.header_room_table.horizontalHeader().hide()
        self.header_room_table.setStyleSheet(":item { border: 1px solid grey; }")

        self.header_room_table.setSpan(0, 0, 1, 2)
        font = QFont("Helvetica", 14)
        item = QTableWidgetItem("Комната №")
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        self.header_room_table.setItem(0, 0, item)

        item = QTableWidgetItem("ФИО 1 игрока")
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        self.header_room_table.setItem(1, 0, item)

        item = QTableWidgetItem("ФИО 2 игрока")
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        self.header_room_table.setItem(1, 1, item)

        self.header_room_table.resizeColumnsToContents()
        self.header_room_table.resizeRowsToContents()

        self.up_spacer_room = QtWidgets.QSpacerItem(desktop_rect.width() // 16, desktop_rect.height(),
                                                    QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Ignored)

        self.horizontal_up_header_layout_room.addWidget(self.return_btn)
        self.horizontal_up_header_layout_room.addSpacerItem(self.up_spacer_room)
        self.horizontal_up_header_layout_room.addWidget(self.header_room_table)
        self.horizontal_up_header_layout_room.addSpacerItem(self.up_spacer_room)
        # end horizontal_up_header_layout_room content

        # horizontal_up_layout_room content
        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.save_btn.clicked.connect(self.save_btn_click)
        self.save_btn.setStyleSheet("QPushButton {background: #03a9f4;                  \
                                    color: #fff; border-radius: 15px;                   \
                                    font-size: 12pt;                                    \
                                    font-family: Century Gothic, sans-serif;}           \
                                    QPushButton:hover {background-color:#64bee8;}       \
                                    QPushButton:pressed {background-color:#03a9f4;}")

        self.download_btn = QtWidgets.QPushButton()
        self.download_btn.setObjectName("download_btn")
        self.download_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.download_btn.clicked.connect(self.download_btn_click)
        self.download_btn.setStyleSheet("QPushButton {background: #03a9f4;                  \
                                        color: #fff; border-radius: 15px;                   \
                                        font-size: 12pt;                                    \
                                        font-family: Century Gothic, sans-serif;}           \
                                        QPushButton:hover {background-color:#64bee8;}       \
                                        QPushButton:pressed {background-color:#03a9f4;}")

        self.send_btn = QtWidgets.QPushButton()
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setMinimumSize(QtCore.QSize(200, 40))
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
        # end horizontal_up_layout_room content

        # horizontal_med_layout_room content
        self.vertical_med_layout_room = QtWidgets.QVBoxLayout()
        self.vertical_med_layout_room.setObjectName("vertical_med_layout_room")
        self.vertical_med_layout_room.setContentsMargins(0, 0, 10, 0)
        self.vertical_med_layout_room.addStretch()

        self.scene = QtWidgets.QGraphicsScene()
        # self.scene.setSceneRect(0, 0, 800, 300)
        self.canvas = Canvas(self.stacked_widget, self, CANVAS_WORKING_MODE.EDIT)
        self.canvas.setStyleSheet("border: 1px solid grey;"
                                  "background-color: rgb(255, 255, 255);")
        # self.canvas.setGeometry(QtCore.QRect(90, 79, 750, 250))
        self.canvas.setScene(self.scene)

        self.horizontal_med_layout_room.addLayout(self.vertical_med_layout_room)
        self.horizontal_med_layout_room.addWidget(self.canvas)
        # end horizontal_med_layout_room content

        # vertical_med_layout_room content
        self.lower_spacer_room = QtWidgets.QSpacerItem(10, desktop_rect.height(),
                                                       QtWidgets.QSizePolicy.Preferred,
                                                       QtWidgets.QSizePolicy.MinimumExpanding)

        self.add_computer_btn = QtWidgets.QPushButton()
        self.add_computer_btn.setObjectName("add_computer_btn")
        self.add_computer_btn.setMaximumSize(QtCore.QSize(40, 50))
        self.add_computer_btn.setStyleSheet("border: 1px solid grey;")
        icon = QIcon()
        icon.addPixmap(self.canvas.computer_pixmap, QIcon.Normal, QIcon.Off)
        self.add_computer_btn.setIcon(icon)
        self.add_computer_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_computer_btn.clicked.connect(self.add_computer_btn_click)

        self.add_router_btn = QtWidgets.QPushButton()
        self.add_router_btn.setObjectName("add_router_btn")
        self.add_router_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_router_btn.setStyleSheet("border: 1px solid grey;")
        icon = QIcon()
        icon.addPixmap(self.canvas.router_pixmap, QIcon.Normal, QIcon.Off)
        self.add_router_btn.setIcon(icon)
        self.add_router_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_router_btn.clicked.connect(self.add_router_btn_click)

        self.add_commutator_btn = QtWidgets.QPushButton()
        self.add_commutator_btn.setObjectName("add_commutator_btn")
        self.add_commutator_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_commutator_btn.setStyleSheet("border: 1px solid grey;")
        icon = QIcon()
        icon.addPixmap(self.canvas.commutator_pixmap, QIcon.Normal, QIcon.Off)
        self.add_commutator_btn.setIcon(icon)
        self.add_commutator_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_commutator_btn.clicked.connect(self.add_commutator_btn_click)

        self.add_arc_btn = QtWidgets.QPushButton()
        self.add_arc_btn.setObjectName("add_arc_btn")
        self.add_arc_btn.setMinimumSize(QtCore.QSize(40, 50))
        self.add_arc_btn.setStyleSheet("border: 1px solid grey;")
        icon = QIcon()
        icon.addPixmap(self.canvas.arc_pixmap, QIcon.Normal, QIcon.Off)
        self.add_arc_btn.setIcon(icon)
        self.add_arc_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_arc_btn.clicked.connect(self.add_arc_btn_click)

        self.vertical_med_layout_room.addWidget(self.add_computer_btn)
        self.vertical_med_layout_room.addWidget(self.add_router_btn)
        self.vertical_med_layout_room.addWidget(self.add_commutator_btn)
        self.vertical_med_layout_room.addWidget(self.add_arc_btn)
        self.vertical_med_layout_room.addSpacerItem(self.lower_spacer_room)
        # end vertical_med_layout_room content

        # vertical_down_layout content
        self.log_widget = QtWidgets.QTextBrowser()
        self.log_widget.setObjectName("log_widget")
        self.log_widget.setMinimumSize(QtCore.QSize(500, 200))
        self.log_widget.setMaximumSize(QtCore.QSize(self.width(), 200))
        self.log_widget.setStyleSheet("border: 1px solid grey;"
                                      "background: #edfcff; font-size: 12pt;"
                                      "font-family: Century Gothic, sans-serif;")

        self.vertical_down_layout_room.addWidget(self.log_widget)
        # end vertical_down_layout content

        # инициализация сервера
        self.server = Server(self)
        self.setup_server()

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("interface_admin", "Проект"))
        self.save_btn.setText(_translate("interface_admin", "Сохранить карту"))
        self.return_btn.setText(_translate("interface_admin", "В холл"))
        self.download_btn.setText(_translate("interface_admin", "Загрузить карту"))
        self.send_btn.setText(_translate("interface_admin", "Отправить карту игрокам"))

    def cell_clicked(self, i):
        sender = self.sender()
        if sender.currentRow() == 0 & sender.currentColumn() == 0:
            # TODO отрисовка i карты на канвасе
            # TODO Показать или скрыть кнопки в зависимости от того, отправлена ли была карта

            self.current_room = i
            self.header_room_table.item(0, 0).setText("Комната №" + str(i + 1))
            # TODO Установка имен игроков соответствующей комнаты (где-то хранятся)
            self.header_room_table.item(1, 0).setText("Проскурин Валерий")
            self.header_room_table.item(1, 1).setText("Проскурин Валерий")
            self.header_room_table.resizeColumnsToContents()
            self.stacked_widget.setCurrentIndex(1)

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

    def return_btn_click(self):
        self.current_room = -1
        self.stacked_widget.setCurrentIndex(0)

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
        # TODO Вызвать функцию передачи карты игрокам соответствующей комнаты (из массива функций)
        self.hide_buttons()
        self.canvas.working_mode = CANVAS_WORKING_MODE.GAME
        net = pickle.dumps(self.canvas.net)
        for user in self.server.users:
            user.sendall(net)

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
        # self.server.socket.bind(('127.0.0.1', 1234))
        self.server.socket.bind(('172.18.7.101', 1234))
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


