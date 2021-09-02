import time

from PyQt5 import QtCore, QtWidgets
from sys import exit
from threading import Thread

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, \
    QTextBrowser, QPlainTextEdit, QHBoxLayout
import sys

from Server_Client.Sockets import Client
from Test_app.Test_app import TestApp
import pickle
from gui_lib.Arc import Arc
from gui_lib.Canvas import Custom_line, Custom_label, Canvas, CANVAS_WORKING_MODE
from gui_lib.Nodes import Node, Computer


class Player(QtWidgets.QMainWindow):

    def __init__(self, username, token, points, group):
        super().__init__()
        self.client = Client(username, token, points, group)
        self.flag_correct = None
        self.functions = [self.client_first_connection, self.client_correct_attack, self.client_code2,
                          self.client_wrong_attack_or_defend, self.client_net_is_safe,
                          self.client_correct_defend, self.client_correct_defend_question]

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
        print(self.connection_label.sizeHint())
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
        self.connect_btn.setStyleSheet("QPushButton {background: #03a9f4;                   \
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
        self.canvas = Canvas(self.stacked_widget, self, CANVAS_WORKING_MODE.EDIT)
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
        self.header_room.setText("Комната № 1")
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

    def restore_map(self, data):
        # отлов исключений
        self.canvas.reset_temp_data()
        Node.reset_counter()
        Arc.reset_counter()
        self.canvas.net = pickle.loads(data)
        self.scene.clear()
        for key_node in self.canvas.net.nodes:
            node = self.canvas.net.nodes[key_node]
            pixmap = self.canvas.get_appropriate_pixmap(node)
            custom_label = Custom_label(pixmap=pixmap, canvas=self.canvas, model_item=node)
            self.canvas.scene().addWidget(custom_label)

        for key_arc in self.canvas.net.arcs:
            arc = self.canvas.net.arcs[key_arc]
            custom_line = Custom_line(canvas=self.canvas, model_item=arc,
                                      x1=arc.node_from.x, y1=arc.node_from.y,
                                      x2=arc.node_to.x, y2=arc.node_to.y)
            self.canvas.scene().addItem(custom_line)

    def connect_btn_click(self):
        try:
            self.client.socket.connect(
                (self.connection_line_edit.text().strip(), 1234)
            )
            self.client.socket.settimeout(None)
            self.stacked_widget.setCurrentIndex(1)
        except:
            alert = QMessageBox()
            alert.setText('Ошибка подключения к серверу!')
            alert.exec_()

    def download_btn_click(self):
        # отлов исключений
        self.download_btn.hide()
        self.canvas.reset_temp_data()
        net = self.client.socket.recv(1024)
        self.canvas.net = pickle.loads(net)
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

    # Первое сообщение
    def client_first_connection(self, args):
        # args = [username, room, role]
        username = args[0]
        room = args[1]
        role = args[2]
        self.client.role = role
        self.client.room = room
        data = 'Комната: {}. '.format(room + 1)
        if role == 'attack':
            data += '{}, Ваша задача: атаковать локальную сеть.'.format(username)
        else:
            data += '{}, Ваша задача: защитить локальную сеть.'.format(username)
        return data

    # Верная атака
    def client_correct_attack(self, args):
        # args = [username, result]
        username = args[0]
        result = str(args[1])
        attack = result.split(')')[0]
        data = '{} предпринял атаку: {}.'.format(username, result)
        thread = Thread(target=self.attack_node, args=(int(attack.split(' ')[2]), Computer), daemon=True)
        thread.start()
        return data

    def client_code2(self, args):
        # args = [result]
        result = str(args[0])
        data = result
        return data

    def client_wrong_attack_or_defend(self, args):
        # args = [username]
        username = args[0]
        data = '{}, нельзя использовать данную команду.'.format(username)
        return data

    def client_net_is_safe(self, args):
        # args = [username]
        username = args[0]
        data = '{}, на данную сеть не совершенно никаких атак.'.format(username)
        return data

    def client_correct_defend(self, args):
        # args = [username, result]
        username = args[0]
        result = args[1]
        data = '{} предпринял защиту ({}) и воздействовал вопросом.'.format(username, result)
        defend = result.split(')')[0]
        self.defend_node(int(defend.split(' ')[2]), Computer)
        return data

    def client_correct_defend_question(self, args):
        # args = [question, correct]
        question = args[0]
        correct = args[1]
        self.flag_correct = correct
        return question

    # Считывание сообщений с сервера
    # FIXME переделать структуру сообщений
    def text_on_textBox(self):
        while True:
            data = self.client.socket.recv(2048)
            data_decode = pickle.loads(data)
            data_show = self.functions[data_decode['key']](data_decode['info'])
            # Добавление сообщения на экран
            # FIXME добавить получение карты передавать data (чистую) в restore_map()
            # FIXME Незаконно менять объекты основного потока не в основном потоке
            self.text_browser_room.append('>>> ' + data_show)

    # Помечает соответствующую вершину красным
    # class_type - это тип класса: Computer, Router, Commutator
    # Возвращает true, если атака возможна и false иначе
    def attack_node(self, id, class_type):
        if id in self.canvas.net.nodes:
            node = self.canvas.net.nodes[id]
            pixmap = self.canvas.get_appropriate_pixmap(class_type)
            fired_pixmap = self.canvas.get_appropriate_fired_pixmap(class_type)
            if node.is_active:
                node.is_under_attack = True
                while node.is_under_attack:
                    node.custom_widget.setPixmap(fired_pixmap)
                    time.sleep(1)
                    node.custom_widget.setPixmap(pixmap)
                    time.sleep(1)
                return True
        return False

    # Помечает соответствующую вершину черным
    # class_type - это тип класса: Computer, Router, Commutator
    # Возвращает true, если защита возможна и false иначе
    def defend_node(self, id, class_type):
        if id in self.canvas.net.nodes:
            node = self.canvas.net.nodes[id]
            if node.is_active:
                if node.is_under_attack:
                    pixmap = self.canvas.get_appropriate_pixmap(class_type)
                    node.custom_widget.setPixmap(pixmap)
                    node.is_under_attack = False
                    node.is_active = False
                    return True
        return False

    def display_defender_btn_click(self):
        f = open('defender_cheat_sheet.txt', 'r')
        message_box = QMessageBox()
        message_box.setMinimumSize(800, 600)
        message_box.setText(f.read())
        f.close()
        message_box.exec_()


    def display_attacker_btn_click(self):
        f = open('attacker_cheat_sheet.txt', 'r')
        message_box = QMessageBox()
        message_box.setText(f.read())
        f.close()
        message_box.exec_()

    def send_msg_btn_click(self):
        listen_thread = Thread(target=self.text_on_textBox)
        listen_thread.start()
        self.plain_text_edit_room.setPlaceholderText('Введите команду')

        if self.client.first_message:
            data = {'key': 0, 'info': [self.client.token, self.client.username, self.client.points]}
            self.client.first_message = False
        else:
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
    points = test.get_points()
    group = test.get_group()
    exit_yn = test.get_exit_yn()

    if points < 7 and exit_yn == 0:
        app1 = QtWidgets.QApplication(sys.argv)
        player = Player(username, token, points, group)
        player.show()
        sys.exit(app1.exec_())
