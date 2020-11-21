from PyQt5 import QtCore, QtGui, QtWidgets
from sys import exit
import socket
from threading import Thread
from PyQt5.QtWidgets import QMessageBox
import sys
from datetime import datetime

from Roles.attacker.design_attacker import Ui_interface_attacker
from Test_app.Test_app import TestApp
import pickle
from PyQt5.QtWidgets import QFileDialog
from gui_lib.Arc import Arc
from gui_lib.Canvas import Custom_line, Custom_label, Canvas, CANVAS_WORKING_MODE
from gui_lib.Net import Net
from gui_lib.Nodes import Node


class Client(QtWidgets.QMainWindow, Ui_interface_attacker):

    def __init__(self, username, token, points, group):
        super(Client, self).__init__()
        self.ui = Ui_interface_attacker()
        self.ui.setupUi(self)

        self.username = username
        self.token = token
        self.points = str(points)
        self.group = group
        self.room = 'none'
        # separator используется для стабильности при передаче сообщений. Помимо того, что серверу и клиенту нужно
        # передавать сообщения пользователей, ему еще нужно передавать информацию о комнате, имени игрока и так далее.
        # Поэтому нужно использовать набор символов, который пользователь вряд ли когда-то введет
        # Также separator на сервере и клиенте должен быть одинаковым
        self.separator = '$%6h))/.qyjrgKUTFV^Shc8~~63,c'
        self.role = 'none'
        self.first_message = True

        # Настройка карты
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 450)
        self.canvas = Canvas(self.ui.centralwidget, self, CANVAS_WORKING_MODE.GAME)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.net = Net({}, {}, {}, {}, {})
        self.canvas.setGeometry(QtCore.QRect(90, 79, 751, 291))
        self.canvas.setScene(self.scene)
        self.ui.download_btn.clicked.connect(self.download_btn_click)
        self.ui.pushButton_2.clicked.connect(self.send_server)

    # Кнопка загрузки карты
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
                    pixmap = self.canvas.get_appropriate_pixmap(node)
                    custom_label = Custom_label(pixmap=pixmap, canvas=self.canvas, model_item=node)
                    self.canvas.scene().addWidget(custom_label)

                for key_arc in self.canvas.net.arcs:
                    arc = self.canvas.net.arcs[key_arc]
                    custom_line = Custom_line(canvas=self.canvas, model_item=arc,
                                              x1=arc.node_from.x, y1=arc.node_from.y,
                                              x2=arc.node_to.x, y2=arc.node_to.y)
                    self.canvas.scene().addItem(custom_line)

    # Считывание сообщений с сервера
    def text_on_textBox(self):
        while True:
            data = self.client.recv(2048).decode("utf-8")
            # Если это первое сообщение с сервера, то в нем содержится иформация о комнате и роли игрока
            if data.split(self.separator)[0] == 'first message':
                self.room = 'room_' + data.split(self.separator)[2]
                data = data.split(self.separator)[1] + data.split(self.separator)[2] + data.split(self.separator)[3] + \
                       data.split(self.separator)[4]

            # Здесь содержится информация о роли конкретного игрока
            elif data.split(self.separator)[0] == 'role':
                self.role = data.split(self.separator)[1]
                continue

            # Если сообщение пользователя некорректно, то оно просто выводится
            elif data.split(self.separator)[0] == 'incorrect':
                data = data.split(self.separator)[1]

            # Если атака корректна, то происходит обработка сообщения в зависимости от объекта и типа атаки
            elif data.split(self.separator)[0] == 'attack_correct':
                data = data.split(self.separator)[1]
                # attack представляет из себя одну из строк из списка ('атаковать комп1 ddos', 'атаковать комп1 пароль')
                attack = data.split(' предпринял атаку (')[1].split(')')[0]

            # Если защита корректна, то происходит обработка сообщения в зависимости от объекта и типа защиты
            elif data.split(self.separator)[0] == 'defend_correct':
                data = data.split(self.separator)[1]
                # defend представляет из себя одну из строк из списка ('защитить комп1 ddos', 'защитить комп1 пароль')
                defend = data.split(' предпринял защиту (')[1].split(')')[0]

            # Если сервер настроен на общение
            else:
                data = f"{str(datetime.now().time()).split('.')[0]}:  {data}"

            # Добавление сообщения на экран
            self.ui.textBrowser.append('>>> ' + data)

    def send_server(self):
        listen_thread = Thread(target=self.text_on_textBox)
        listen_thread.start()
        self.ui.plainTextEdit.setPlaceholderText('Введите команду')

        if self.first_message:
            data = 'first message' + self.separator + self.token + self.separator + self.username\
                   + self.separator + self.points
            self.first_message = False
        else:
            data = self.username + self.separator + self.room + self.separator + self.role + self.separator + \
                   self.ui.plainTextEdit.toPlainText()
        self.client.send(data.encode("utf-8"))
        self.ui.plainTextEdit.clear()

    def setupUi(self):
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        try:
            self.client.connect(
                ("127.0.0.1", 1234)
            )
        except:
            alert = QMessageBox()
            alert.setText('Ошибка подключения к серверу!')
            alert.exec_()
            exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    test = TestApp()
    test.show()
    app.exec()

    username = test.get_username()
    token = test.get_token()
    points = test.get_points()
    group = test.get_group()

    if points < 7:
        app1 = QtWidgets.QApplication(sys.argv)
        client = Client(username, token, points, group)
        client.setupUi()
        client.show()
        sys.exit(app1.exec_())
