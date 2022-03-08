import socket
from functools import partial

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, \
    QTextBrowser, QPlainTextEdit, QHBoxLayout
import sys
from gui_lib.Net import Net
from Server_Client.Sockets import Client
from Test_app.Test_app import TestApp
import pickle
from gui_lib.Canvas import Canvas, CANVAS_WORKING_MODE


class Player(QtWidgets.QMainWindow):

    def __init__(self, username, platoon, test_scores):
        super().__init__()
        self.client = Client(username, platoon, test_scores, self)
        # FIXME Refactor
        self.flag_correct = None

        # Отрисовка
        self.setObjectName("interface_player")
        desktop_rect = QApplication.desktop().availableGeometry()
        self.resize(desktop_rect.width(), desktop_rect.height())
        self.move(desktop_rect.left(), desktop_rect.top())
        self.setMinimumSize(1320, 800)
        self.setStyleSheet("background: #fffdf5;")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.current_room = 0

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")
        self.setCentralWidget(self.stacked_widget)

        # stacked_widget content
        self.connection_widget = QtWidgets.QWidget()
        self.connection_widget.setObjectName("connection_widget")

        self.room_widget = QtWidgets.QWidget()
        self.room_widget.setObjectName("room_widget")
        self.room_widget.setStyleSheet("border: 0 px;")

        self.stacked_widget.addWidget(self.connection_widget)
        self.stacked_widget.addWidget(self.room_widget)
        # end stacked_widget content

        # connection_widget content
        self.main_layout_connection = QVBoxLayout()
        self.main_layout_connection.addStretch(0)
        self.main_layout_connection.setObjectName("main_layout_connection")

        self.connection_widget.setLayout(self.main_layout_connection)
        # end connection_widget content

        # main_layout_connection content
        self.connection_label = QLabel()
        self.connection_label.setObjectName("connection_label")
        self.connection_label.setText("Введите ip сервера:")
        font = QFont("Helvetica", 14)
        self.connection_label.setFont(font)

        self.connection_line_edit = QLineEdit()
        self.connection_line_edit.setObjectName("connection_line_edit")
        self.connection_line_edit.setFont(font)
        self.connection_line_edit.setStyleSheet("background: white;")

        self.connect_btn = QPushButton()
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.setText("Подключиться")
        self.connect_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.connect_btn.clicked.connect(self.connect_btn_click)
        self.connect_btn.setStyleSheet(
            #language=css
            "QPushButton {background: #03a9f4;                   \
                                        color: #fff; border-radius: 15px;                   \
                                        font-size: 12pt;                                    \
                                        font-family: Century Gothic, sans-serif;}           \
                                        QPushButton:hover {background-color:#64bee8;}       \
                                        QPushButton:pressed {background-color:#03a9f4;}")

        self.reconnect_btn = QPushButton()
        self.reconnect_btn.setObjectName("reconnect_btn")
        self.reconnect_btn.setText("Переподключиться")
        self.reconnect_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.reconnect_btn.clicked.connect(partial(self.connect_btn_click, True))
        self.reconnect_btn.setStyleSheet("QPushButton {background: #03a9f4;                   \
                                                color: #fff; border-radius: 15px;                   \
                                                font-size: 12pt;                                    \
                                                font-family: Century Gothic, sans-serif;}           \
                                                QPushButton:hover {background-color:#64bee8;}       \
                                                QPushButton:pressed {background-color:#03a9f4;}")

        self.vertical_spacer_connection = QtWidgets.QSpacerItem(0, int(desktop_rect.height() / 2.5),
                                                                QSizePolicy.Ignored,
                                                                QSizePolicy.Expanding)

        self.main_layout_connection.addWidget(self.connection_label, alignment=Qt.AlignCenter)
        self.main_layout_connection.addWidget(self.connection_line_edit, alignment=Qt.AlignCenter)
        self.main_layout_connection.addWidget(self.connect_btn, alignment=Qt.AlignCenter)
        self.main_layout_connection.addWidget(self.reconnect_btn, alignment=Qt.AlignCenter)
        self.main_layout_connection.addSpacerItem(self.vertical_spacer_connection)
        # end main_layout_connection content

        # room_widget_content
        self.main_layout_room = QVBoxLayout()
        self.main_layout_room.setObjectName("main_layout_room")

        self.room_widget.setLayout(self.main_layout_room)
        # end room_widget_content

        # main_layout_room content
        self.header_layout_room = QHBoxLayout()
        self.header_layout_room.setObjectName("header_layout_room")

        self.scene = QtWidgets.QGraphicsScene()
        nets = np.zeros(1, Net)
        nets[0] = Net({}, {}, {}, {}, {})
        self.canvas = Canvas(self.stacked_widget, self, nets, CANVAS_WORKING_MODE.GAME)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);"
                                  "border: 1px solid grey")
        self.canvas.setScene(self.scene)

        self.text_browser_room = QTextBrowser()
        self.text_browser_room.setObjectName("text_browser_room")
        self.text_browser_room.setMinimumSize(QtCore.QSize(500, 150))
        self.text_browser_room.setMaximumSize(QtCore.QSize(desktop_rect.width(), 150))
        self.text_browser_room.setStyleSheet("background: #edfcff;"
                                             "border: 1px solid grey;"
                                             "font-size: 12pt;"
                                             "font-family: Century Gothic, sans-serif;")

        self.plain_text_edit_room = QPlainTextEdit()
        self.plain_text_edit_room.setObjectName("plain_text_edit_room")
        self.plain_text_edit_room.setPlaceholderText('Введите команду')
        self.plain_text_edit_room.setMinimumSize(QtCore.QSize(500, 70))
        self.plain_text_edit_room.setMaximumSize(QtCore.QSize(desktop_rect.width(), 70))
        self.plain_text_edit_room.setStyleSheet("background: white;"
                                                "border: 1px solid grey;"
                                                "font-size: 12pt;"
                                                "font-family: Century Gothic, sans-serif;")

        self.send_msg_btn_room = QPushButton()
        self.send_msg_btn_room.setObjectName("send_msg_btn_room")
        self.send_msg_btn_room.setMinimumSize(QtCore.QSize(200, 40))
        self.send_msg_btn_room.setMaximumSize(QtCore.QSize(desktop_rect.width(), 40))
        self.send_msg_btn_room.setText("Отправить")
        self.send_msg_btn_room.clicked.connect(self.send_msg_btn_click)
        self.send_msg_btn_room.setStyleSheet(
            "QPushButton {                                  \
                                        background: #03a9f4;                        \
                                        color: #fff;                                \
                                        border-radius: 15px;                        \
                                        font-size: 12pt;                            \
                                        font-family: Century Gothic, sans-serif;}   \
                                    QPushButton:hover {                             \
                                        background-color:#64bee8;                   \
                                    }                                               \
                                    QPushButton:pressed {                           \
                                        background-color:#03a9f4;                   \
                                    }")

        self.main_layout_room.addLayout(self.header_layout_room)
        self.main_layout_room.addWidget(self.canvas)
        self.main_layout_room.addWidget(self.text_browser_room)
        self.main_layout_room.addWidget(self.plain_text_edit_room)
        self.main_layout_room.addWidget(self.send_msg_btn_room)
        # end main_layout_room content

        # header_layout_room
        self.header_room = QtWidgets.QTextEdit()
        self.header_room.setObjectName("header_room")
        self.header_room.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.header_room.setFixedHeight(50)
        self.header_room.setText("Комната №")
        # self.header_room.setAlignment(Qt.AlignCenter)
        self.header_room.setReadOnly(True)
        self.header_room.setStyleSheet("font-size: 16pt;"
                                       "color: black;")

        self.display_attacker_btn = QPushButton()
        self.display_attacker_btn.setObjectName("display_attacker_btn")
        self.display_attacker_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.display_attacker_btn.setMaximumSize(QtCore.QSize(desktop_rect.width(), 40))
        self.display_attacker_btn.setText("Атакующий")
        self.display_attacker_btn.clicked.connect(self.display_attacker_btn_click)
        self.display_attacker_btn.setStyleSheet(
                                    "QPushButton {                                  \
                                        background: #03a9f4;                        \
                                        color: #fff;                                \
                                        border-radius: 15px;                        \
                                        font-size: 12pt;                            \
                                        font-family: Century Gothic, sans-serif;}   \
                                    QPushButton:hover {                             \
                                        background-color:#64bee8;                   \
                                    }                                               \
                                    QPushButton:pressed {                           \
                                        background-color:#03a9f4;                   \
                                    }")

        self.display_defender_btn = QPushButton()
        self.display_defender_btn.setObjectName("display_defender_btn")
        self.display_defender_btn.setMinimumSize(QtCore.QSize(200, 40))
        self.display_defender_btn.setMaximumSize(QtCore.QSize(desktop_rect.width(), 40))
        self.display_defender_btn.setText("Защитник")
        self.display_defender_btn.clicked.connect(self.display_defender_btn_click)
        self.display_defender_btn.setStyleSheet(
                                    "QPushButton {                                  \
                                        background: #03a9f4;                        \
                                        color: #fff;                                \
                                        border-radius: 15px;                        \
                                        font-size: 12pt;                            \
                                        font-family: Century Gothic, sans-serif;}   \
                                    QPushButton:hover {                             \
                                        background-color:#64bee8;                   \
                                    }                                               \
                                    QPushButton:pressed {                           \
                                        background-color:#03a9f4;                   \
                                    }")

        self.header_layout_room.addWidget(self.header_room)
        self.header_layout_room.addWidget(self.display_attacker_btn)
        self.header_layout_room.addWidget(self.display_defender_btn)
        # end header_layout_room

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("interface_player", "Project"))

    @QtCore.pyqtSlot(str)
    def terminal_set_text(self, data):
        self.text_browser_room.append('>  ' + data)

    def msg_listener_start(self):
        # создадим поток
        self.client.listening_thread = QtCore.QThread()
        # перенесём объект в другой поток
        msg_handler = self.client.msg_handler
        msg_handler.moveToThread(self.client.listening_thread)
        # после чего подключим все сигналы и слоты
        msg_handler.terminal_signal.connect(self.terminal_set_text)
        msg_handler.download_net_signal.connect(self.canvas.download_net)
        msg_handler.display_net_signal.connect(self.canvas.display_net)
        msg_handler.header_room_signal.connect(self.header_room_set_text)
        msg_handler.correct_attack_signal.connect(self.attack_node)
        msg_handler.correct_defend_signal.connect(self.defend_node)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.client.listening_thread.started.connect(msg_handler.run)
        # запустим поток
        self.client.listening_thread.start()

    def connect_btn_click(self, is_reconnect=False):
        try:
            self.client.socket.connect(
                (self.connection_line_edit.text().strip(), self.client.PORT)
            )
            self.client.socket.settimeout(None)
            self.client.is_reconnect = is_reconnect
            # Слушаем сообщения от сервера в отдельном потоке
            self.msg_listener_start()
            self.stacked_widget.setCurrentIndex(1)

        except socket.timeout:
            alert = QMessageBox()
            alert.setText('Превышено время ожидания от сервера!')
            alert.exec_()

        except ConnectionError:
            alert = QMessageBox()
            alert.setText('Ошибка подключения к серверу!')
            alert.exec_()

        except Exception as exc:
            print(exc)

    @QtCore.pyqtSlot(str)
    def header_room_set_text(self, str):
        self.header_room.setText(str)

    # Помечает соответствующую вершину красным
    # class_type - это тип класса: Computer, Router, Commutator
    # Возвращает true, если атака возможна и false иначе
    @QtCore.pyqtSlot(int, type)
    def attack_node(self, id, class_type):
        if id in self.canvas.nets[0].nodes:
            node = self.canvas.nets[0].nodes[id]
            pixmap = self.canvas.get_appropriate_pixmap(class_type)
            fired_pixmap = self.canvas.get_appropriate_fired_pixmap(class_type)
            if node.is_active:
                node.is_under_attack = True
                node.custom_widget.setPixmap(fired_pixmap)
                return True
        return False

    # Помечает соответствующую вершину черным
    # class_type - это тип класса: Computer, Router, Commutator
    # Возвращает true, если защита возможна и false иначе
    @QtCore.pyqtSlot(int, type)
    def defend_node(self, id, class_type):
        if id in self.canvas.nets[0].nodes:
            node = self.canvas.nets[0].nodes[id]
            if node.is_active:
                if node.is_under_attack:
                    pixmap = self.canvas.get_appropriate_pixmap(class_type)
                    node.custom_widget.setPixmap(pixmap)
                    node.is_under_attack = False
                    node.is_active = False
                    return True
        return False

    def display_defender_btn_click(self):
        f = open('defender_cheat_sheet.txt', 'r', encoding="utf-8")
        message_box = QMessageBox()
        message_box.setText(f.read())
        f.close()
        message_box.exec_()

    def display_attacker_btn_click(self):
        f = open('attacker_cheat_sheet.txt', 'r', encoding="utf-8")
        message_box = QMessageBox()
        message_box.setText(f.read())
        f.close()
        message_box.exec_()

    def send_msg_btn_click(self):
        self.plain_text_edit_room.setPlaceholderText('Введите команду')
        user_answer = self.plain_text_edit_room.toPlainText()
        if self.flag_correct is not None:
            if user_answer != self.flag_correct:
                result = '0'
            else:
                result = '1'
            self.flag_correct = None
        else:
            result = user_answer
        if self.client.role == 'attack':
            data = {'key': 1, 'info': [self.client.username, self.client.room, result]}
        else:
            data = {'key': 2, 'info': [self.client.username, self.client.room, result]}

        data_pickle = pickle.dumps(data)
        self.client.socket.send(data_pickle)
        self.plain_text_edit_room.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    test = TestApp()
    test.show()
    app.exec()

    username = test.get_username()
    token = test.get_token()
    test_scores = test.get_points()
    platoon = test.get_group()
    exit_yn = test.get_exit_yn()

    # if points < 7 and exit_yn == 0:
    if test_scores < 7:
        app1 = QtWidgets.QApplication(sys.argv)
        player = Player(username, platoon, test_scores)
        player.show()
        sys.exit(app1.exec_())
