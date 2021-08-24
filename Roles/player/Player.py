import time

from PyQt5 import QtCore, QtWidgets
from sys import exit
from threading import Thread
from PyQt5.QtWidgets import QMessageBox
import sys
from datetime import datetime

from Roles.player.design_player import Ui_interface_player
from Server_Client.Sockets import Client
from Test_app.Test_app import TestApp
import pickle
from PyQt5.QtWidgets import QFileDialog
from gui_lib.Arc import Arc
from gui_lib.Canvas import Custom_line, Custom_label, Canvas, CANVAS_WORKING_MODE
from gui_lib.Net import Net
from gui_lib.Nodes import Node, Computer


class Player(QtWidgets.QMainWindow, Ui_interface_player):

    def __init__(self, username, token, points, group):
        super().__init__()
        self.setupUi(self)
        self.client = Client(username, token, points, group)
        self.setup_connect()
        self.flag_correct = None
        self.functions = [self.client_code0, self.client_code1, self.client_code2, self.client_code3,
                          self.client_code4, self.client_code5, self.client_code6]

        # Настройка карты
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 300)
        self.canvas = Canvas(self.centralwidget, self, CANVAS_WORKING_MODE.GAME)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.net = Net({}, {}, {}, {}, {})
        self.canvas.setGeometry(QtCore.QRect(90, 79, 750, 250))
        self.canvas.setScene(self.scene)
        #
        self.horizontal_med_layout.addWidget(self.canvas)

        self.centralwidget.setLayout(self.main_layout)
        # Привязка событий нажатия
        self.send_msg_btn.clicked.connect(self.send_msg_btn_click)
        self.download_btn.clicked.connect(self.download_btn_click)

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
    def client_code0(self, args):
        # args = [username, room, role]
        username = args[0]
        room = args[1]
        role = args[2]
        self.client.role = role
        self.client.room = 'room_' + str(room)
        data = 'Комната: {}. '.format(room)
        if role == 'attack':
            data += '{}, Ваша задача: атаковать локальную сеть.'.format(username)
        else:
            data += '{}, Ваша задача: защитить локальную сеть.'.format(username)
        return data

    # Верная атака
    def client_code1(self, args):
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

    def client_code3(self, args):
        # args = [username]
        username = args[0]
        data = '{}, нельзя использовать данную команду.'.format(username)
        return data

    def client_code4(self, args):
        # args = [username]
        username = args[0]
        data = '{}, на данную сеть не совершенно никаких атак.'.format(username)
        return data

    def client_code5(self, args):
        # args = [username, result]
        username = args[0]
        result = args[1]
        data = '{} предпринял защиту ({}) и воздействовал вопросом.'.format(username, result)
        defend = result.split(')')[0]
        self.defend_node(int(defend.split(' ')[2]), Computer)
        return data

    def client_code6(self, args):
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
            # Если сервер настроен на общение
            #else:
                #data_decode = f"{str(datetime.now().time()).split('.')[0]}:  {data_decode}"

            # Добавление сообщения на экран
            # FIXME добавить получение карты передавать data (чистую) в restore_map()
            # FIXME Незаконно менять объекты основного потока не в основном потоке
            self.textBrowser.append('>>> ' + data_show)

            '''# Если защита корректна, то происходит обработка сообщения в зависимости от объекта и типа защиты
            elif data_decode.split(self.client.separator)[0] == 'defend_correct1':
                data_decode = data_decode.split(self.client.separator)[1]
                # defend представляет из себя одну из строк из списка ('защитить комп 1 ddos',
                # 'защитить комп 1 пароль')
                # Пример вызова функции защиты. Вместо 2 нужен id,
                # вместо Computer - Router или Commutator (в зависимости от команды)
                defend = data_decode.split(' предпринял защиту (')[1].split(')')[0]
                self.defend_node(int(defend.split(' ')[2]), Computer)

            elif data_decode.split(self.client.separator)[0] == 'defend_correct2':
                question = data_decode.split(self.client.separator)[1]
                self.flag_correct = data_decode.split(self.client.separator)[2]
                self.textBrowser.append(question)
                continue'''

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

    def send_msg_btn_click(self):
        listen_thread = Thread(target=self.text_on_textBox)
        listen_thread.start()
        self.plainTextEdit.setPlaceholderText('Введите команду')

        if self.client.first_message:
            data = {'key': 0, 'info': [self.client.token, self.client.username, self.client.points]}
            self.client.first_message = False
        else:
            user_answer = self.plainTextEdit.toPlainText()
            if self.flag_correct is not None:
                if user_answer != self.flag_correct:
                    result = 0
                else:
                    result = 1
                self.flag_correct = None
            else:
                result = user_answer
            if self.client.role == 'attack':
                data = {'key': 1, 'info': [self.client.username, self.client.room, result]}
            else:
                data = {'key': 2, 'info': [self.client.username, self.client.room, result]}

        data_pickle = pickle.dumps(data)
        self.client.socket.send(data_pickle)
        self.plainTextEdit.clear()

    def setup_connect(self):
        try:
             self.client.socket.connect(
                 ("127.0.0.1", 1234)
             )
            # self.client.socket.connect(
            #    ("172.18.7.101", 1234)
            #)
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
        player = Player(username, token, points, group)
        player.show()
        sys.exit(app1.exec_())
