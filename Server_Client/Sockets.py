import pickle
import socket
from datetime import datetime
from enum import Enum
from functools import partial

from PyQt5.QtCore import Qt

from gui_lib.Net import Net
from PyQt5 import QtCore

from Test_app.Dictionary import Questions
import pandas as pd
import numpy as np
from random import shuffle
from gui_lib.Nodes import Computer


# Слушатель сообщений, получаемых с сервера
class ClientMessageHandler(QtCore.QObject):

    terminal_signal = QtCore.pyqtSignal(str)
    download_net_signal = QtCore.pyqtSignal(Net, int)
    display_net_signal = QtCore.pyqtSignal(int)
    header_room_signal = QtCore.pyqtSignal(str)
    correct_attack_signal = QtCore.pyqtSignal(int, type)
    correct_defend_signal = QtCore.pyqtSignal(int, type)

    def __init__(self, client):
        super().__init__()
        self.client = client

    # Слушаем сообщения, получаемые с сервера
    def run(self):
        # TODO Обработка исключений
        while True:
            data = self.client.socket.recv(4096)
            data_decode = pickle.loads(data)
            data_show = self.client.msg_handler_funcs[data_decode['key']](data_decode['info'])
            # Посылаем сигнал из второго потока в GUI поток
            # Добавление сообщения на экран
            self.terminal_signal.emit(data_show)


class Client:
    def __init__(self, username, platoon, test_scores, player):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.PORT = 1234
        self.socket.settimeout(5)
        self.username = username
        self.test_scores = str(test_scores)
        self.room = None
        self.role = None
        self.msg_handler = ClientMessageHandler(self)
        self.listening_thread = None
        self.is_reconnect = None
        self.player = player
        # FIXME Refactor
        self.msg_handler_funcs = [self.initial_data_handler, self.client_correct_attack, self.client_code2,
                                  self.client_wrong_attack_or_defend, self.client_net_is_safe,
                                  self.client_correct_defend, self.client_correct_defend_question]

    # Обработчик первого сообщения от сервера.
    # Сообщение содержит назначенную комнату, роль и топологию сети.
    def initial_data_handler(self, args):
        # args = [room, role, net]
        self.room = args[0]
        self.role = args[1]
        net = args[2]
        # Создание сети
        self.msg_handler.download_net_signal.emit(net, 0)
        # Отрисовка сети
        self.msg_handler.display_net_signal.emit(0)
        # Смена надписи комнаты
        self.msg_handler.header_room_signal.emit(f"Комната № {self.room + 1}")

        if not self.is_reconnect:
            # Отправляем серверу имя и количество очков за тест
            data = {'key': 0, 'info': [self.username, self.test_scores]}
            data_encode = pickle.dumps(data)
            self.socket.send(data_encode)

        # Строка, которая будет напечатана в консоль
        data_show = 'Комната: {}. '.format(self.room + 1)
        if self.role == PLAYER_ROLE.ATTACKER:
            data_show += '{}, ваша задача: атаковать локальную сеть.'.format(self.username)
        elif self.role == PLAYER_ROLE.DEFENDER:
            data_show += '{}, ваша задача: защитить локальную сеть.'.format(self.username)
        else:
            print("Неверная роль игрока")
        return data_show

    # Верная атака
    def client_correct_attack(self, args):
        # args = [username, result]
        username = args[0]
        result = str(args[1])
        attack = result.split(')')[0]
        data = '{} предпринял атаку: {}.'.format(username, result)
        self.msg_handler.correct_attack_signal.emit(int(attack.split(' ')[1].split('.')[3][1]), Computer)
        return data

    def client_code2(self, args):
        # args = [result]
        result = str(args[0])
        data = result
        return data

    def client_wrong_attack_or_defend(self, args):
        # args = [username, ips]
        username = args[0]
        try:
            ips = args[1]
            data = ips
        except:
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
        self.msg_handler.correct_defend_signal.emit(int(defend.split(' ')[7].split('.')[3][1]), Computer)
        return data

    def client_correct_defend_question(self, args):
        # args = [question, correct]
        question = args[0]
        correct = args[1]
        self.player.flag_correct = correct
        return question


class PLAYER_ROLE(Enum):
    ATTACKER = 0
    DEFENDER = 1


# Класс, представляющий данные о пользователе.
class UserData:

    def __init__(self, ip, id, role, user_socket, user_thread, name=None):
        self.ip = ip
        # Персональный id игрока (принимает значения от 0 до Server.MAX_USER - 1)
        self.id = id
        self.role = role
        self.name = name
        self.socket = user_socket
        self.thread = user_thread
        # Наличие соединения с пользователем
        self.is_connected = True


# Класс, представляющий строку excel-таблицы. Содержит информацию об одном пользователе.
class RowDataTable:

    def __init__(self, name, test_scores, practice_score=0, final_grade=0):
        self.name = name
        self.test_scores = test_scores
        self.practice_scores = practice_score
        self.final_grade = final_grade


def user_id_to_room_number(id):
    return id // 2


# Слушатель сообщений, получаемых от клиента
class ServerMessageHandler(QtCore.QObject):

    def __init__(self, server, ip):
        super().__init__()
        self.server = server
        self.ip = ip

    # Слушаем сообщения, получаемые от клиента
    def run(self):
        # TODO Обработка исключений
        user_data = self.server.users[self.ip]
        while True:
            try:
                print(user_data.socket)
                print(f"id = {user_data.id}")
                data = user_data.socket.recv(4096)
                data_decode = pickle.loads(data)
            # TODO
            except ConnectionResetError:
                user_data.is_connected = False
                user_data.socket.close()
                return
            except EOFError:
                user_data.is_connected = False
                user_data.socket.close()
                return
            self.server.msg_handlers_funcs[data_decode['key']](data_decode['info'], self.ip)


class Server(QtCore.QObject):

    username_connect_signal = QtCore.pyqtSignal(int, PLAYER_ROLE, str)
    header_room_table_signal = QtCore.pyqtSignal(int, PLAYER_ROLE, str)
    canvas_signal = QtCore.pyqtSignal(int)

    def __init__(self, admin):
        super().__init__()
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        # Обратная ссылка на GUI
        self.admin = admin
        # Порт подключения
        self.PORT = 1234
        # Максимальное количество пользователей, подключенных одновременно
        self.MAX_USERS = 24
        # Количество комнат
        self.ROOM_NUMBER = self.MAX_USERS // 2
        # Суммарное количество подключений. Может быть больше self.MAX_USERS при переподключении пользователей
        self.connections_number = 0
        # Id, который будет выдан следующему подключенному пользователю
        self.current_user_id = 0
        # Массив флагов, каждый флаг показывает, была ли отправлена топология сети.
        # Если флаг установлен в True, то редактировать сеть запрещено.
        self.nets_were_sent = np.zeros(self.ROOM_NUMBER, dtype=bool)
        # Данные, из которых будет формироваться excel-таблица
        self.table_data = np.empty(self.MAX_USERS, RowDataTable)
        # Обработчики сообщений для каждого клиента
        self.msg_handlers = np.empty(self.MAX_USERS, ServerMessageHandler)

        # FIXME Refactor
        self.dict = Questions()
        self.defend_questions = self.random_questions()
        self.question_index = 0
        self.points_practice = 0

        # Отображение ip в UserData
        self.users = {}

        # FIXME
        self.attack_defend = {}
        self.ip_list = []
        for i in range(5):
            ip = "10.10.10.0" + str(i + 1)
            self.ip_list.append(ip)
            self.attack_defend["sudo "+ ip + " bruteforce"] = "sudo " +\
                               "add rule name=BLOCK IP ADDRESS - " + ip + " dir=in action=block"
        print(self.attack_defend)

        self.info = [{'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_1.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_2.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_3.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_4.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_5.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_6.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_7.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_8.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_9.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_10.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_11.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                     {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_12.txt',
                      'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]}]
        # FIXME Refactor
        self.msg_handlers_funcs = [self.first_connection_handler, self.server_message_from_attacker,
                                   self.server_message_from_defender]
        self.server_thread = None

    # Запуск сервера
    def run(self):
        # FIXME Автоматический запуск на нужном сокете
        self.socket.bind(('127.0.0.1', self.PORT))
        # self.server.socket.bind(('172.18.7.101', self.PORT))
        self.socket.listen(self.MAX_USERS)
        print('Сервер запущен')
        # TODO Try catch?
        while True:
            user_socket, address = self.socket.accept()
            ip = address[0]
            is_reconnect = False
            if ip in self.users:
                if self.users[ip].is_connected:
                    user_socket.close()
                    continue
                else:
                    is_reconnect = True
            self.connections_number += 1
            print(f"Пользователь <{ip}> подключился!")
            room = self.get_room_number(ip, is_reconnect)
            role = self.get_role(ip, is_reconnect)
            if not self.nets_were_sent[room]:
                self.canvas_signal.emit(room)
                self.nets_were_sent[room] = True
            self.msg_listener_start(ip, self.current_user_id, role, user_socket, is_reconnect)
            if not is_reconnect:
                self.current_user_id += 1
            self.send_initial_data(user_socket, room, role)

    # Отправляет игроку комнату, роль и топологию сети
    def send_initial_data(self, user_socket, room, role):
        data = {"key": 0, "info": [room, role, self.admin.canvas.nets[room]]}
        data_encode = pickle.dumps(data)
        user_socket.send(data_encode)

    def get_room_number(self, ip, is_reconnect):
        if is_reconnect:
            return user_id_to_room_number(self.users[ip].id)
        return user_id_to_room_number(self.current_user_id)

    def get_role(self, ip, is_reconnect):
        if is_reconnect:
            return self.users[ip].role
        return PLAYER_ROLE(self.current_user_id % 2)

    def get_names_by_room(self, room):
        result = ["Фамилия и имя нападающего", "Фамилия и имя защитника"]
        for user_data in self.users.values():
            if room == user_id_to_room_number(user_data.id):
                if user_data.role == PLAYER_ROLE.ATTACKER:
                    result[0] = user_data.name
                else:
                    result[1] = user_data.name
        return result

    # Обработчик первого сообщения от клиента.
    # Сообщение содержит имя и количество очков за тест
    def first_connection_handler(self, args, ip):
        # args = [username, test_scores]
        name = args[0]
        test_scores = args[1]
        # Запоминаем полученные данные
        self.table_data[self.users[ip].id] = RowDataTable(name, test_scores)
        self.users[ip].name = name

        # Отрисовываем полученные данные
        room = user_id_to_room_number(self.users[ip].id)
        role = self.users[ip].role
        self.username_connect_signal.emit(room, role, name)
        self.header_room_table_signal.emit(room, role, name)
        print("first_connection_handler")

    def server_message_from_attacker(self, args, ip):
        # args = [username, room, result]
        username = args[0]
        room = args[1]
        result = args[2]
        # Записываем все сообщения в переменную text, из которой позже будет сформирован txt файл
        self.info[room]['text'] += str(datetime.now().time()).split('.')[0] + ':' + '(' + username + ')' + result + '\n'
        if username not in self.info[room]['username']:
            self.info[room]['username'].append(username)

        print('Message from attacker: ', result)
        # Если команда верная
        if result in self.attack_defend.keys():
            # Записываем в self.server.info[room]['last_action'] команду, чтобы защищающийся ввел команду, которая
            # защищает конкретно от этого вида атаки
            self.info[room]['last_action'] = result
            data = {'key': 1, 'info': [username, result]}
            socket_to_send = None
            # Добавление одного очка за верно написанную команду по атаке
            self.info[room]['points'][0] += 1
        elif result in ['0', '1']:
            if result == '0':
                result = 'Атакующий не справился с вопросом.'
            else:
                result = 'Атакующий справился с вопросом.'
            data = {'key': 2, 'info': [result]}
            socket_to_send = None
        # Если написал что-то, чего нет в командах для атакующего
        else:
            if result == "ipconfig":
                ips = '\n'.join(self.ip_list)
                data = {'key': 3, 'info': [username, ips]}
            else:
                data = {'key': 3, 'info': [username]}
            socket_to_send = listened_socket

        # Обновление значений в эксель таблице
        self.create_dict(username=username, score_practice=self.info[room]['points'][0])

        data_encode = pickle.dumps(data)
        self.send_data(room, data_encode, socket=socket_to_send)

    def server_message_from_defender(self, args, listened_socket):
        # args = [username, room, result, ip]
        username = args[0]
        room = args[1]
        result = args[2]
        print('Message from defender:', result)
        # Если атакующий еще не совершил атаку
        if self.info[room]['last_action'] == '':
            data = {'key': 4, 'info': [username]}
            socket_to_send = listened_socket

        # Если атакующий уже совершил атаку
        else:
            # Если команда защитника защищает от типа нападения атакующего
            if self.attack_defend[self.info[room]['last_action']] == result:
                self.info[room]['last_action'] = ''
                # Добавление одного очка за верно написанную команду по защите
                self.info[room]['points'][1] += 1
                # Отправка верной защиты всем в комнате
                data = [{'key': 5, 'info': [username, result]}]

                # Отправка вопроса нападающему
                question = self.defend_questions[self.question_index]
                answer1 = '\n1) ' + self.dict.quest[question][0][1]
                answer2 = '\n2) ' + self.dict.quest[question][1][1]
                answer3 = '\n3) ' + self.dict.quest[question][2][1] + '\n'
                correct = None
                for i in range(3):
                    if self.dict.quest[question][i][2] == 1:
                        correct = str(i + 1)
                self.question_index += 1

                question = '\n' + question[1] + answer1 + answer2 + answer3
                data.append({'key': 6, 'info': [question, correct]})
                socket_to_send = self.info[room]['socket'][0]

            # Если написана неверная команда или команда не соответствует типу нападения
            else:
                data = {'key': 3, 'info': [username]}
                socket_to_send = listened_socket

        # Обновление значений в эксель таблице
        self.create_dict(username=username, score_practice=self.info[room]['points'][1])

        # if type(data) == list:
        #     data_encode = pickle.dumps(data[0])
        #     await self.send_data(room, data_encode)
        #     data_encode = pickle.dumps(data[1])
        #     await self.send_data(room, data_encode, socket=socket_to_send)
        # else:
        #     data_encode = pickle.dumps(data)
        #     await self.send_data(room, data_encode, socket=socket_to_send)

    def random_questions(self):
        all_questions_keys = list(self.dict.quest.keys())
        one_answer = []

        # Поиск всех вопросов всех типов и добавление в соответствующие списки
        for question_key in all_questions_keys:
            if question_key[0] == 1:
                one_answer.append(question_key)

        shuffle(one_answer)

        return one_answer

    # Отправка сообщений клиентам
    def send_data(self, room, data=None, socket=None):
        # Если socket is None, то сервер отправляет всем клиентам в комнате, иначе конкретному клиенту по адресу сокета
        # if socket is None:
        #     for user in self.info[room]['socket']:
        #         await self.main_loop.sock_sendall(user, data)
        # else:
        #     await self.main_loop.sock_sendall(socket, data)
        pass

    # Создание эксель таблицы
    def create_dict(self, address=None, token=None, username=None, score=None, score_practice=None):
        if address is not None:
            self.table_data['ip'].append(address)
            self.table_data['token'].append(token)
            self.table_data['ФИО'].append(username)
            self.table_data['Баллы за тест'].append(str(score))
        if score_practice is None:
            self.table_data['Баллы за практику'].append('0')
        else:
            for i in range(len(self.table_data['ФИО'])):
                if username == self.table_data['ФИО'][i]:
                    self.table_data['Баллы за практику'][i] = str(score_practice)
        data_m = pd.DataFrame(self.table_data)
        writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
        data_m.to_excel(writer, 'Sheet1')
        writer.save()

    def msg_listener_start(self, ip, user_id, role, user_socket, is_reconnect):
        thread = QtCore.QThread(parent=self)
        if is_reconnect:
            self.users[ip].user_socket = user_socket
            self.users[ip].thread = thread
            user_id = self.users[ip].id
            self.users[ip].is_connected = True
        else:
            self.users[ip] = UserData(ip, user_id, role, user_socket, thread)
        self.msg_handlers[user_id] = ServerMessageHandler(self, ip)
        self.msg_handlers[user_id].moveToThread(thread)
        thread.started.connect(self.msg_handlers[user_id].run)
        thread.start()

    # Создание текстового файла, когда один из игроков в комнате закрывает приложение
    def create_txt(self, room, message):
        text = open(self.info[room]['txt_file'], 'w')
        text.write(message)
        text.close()
