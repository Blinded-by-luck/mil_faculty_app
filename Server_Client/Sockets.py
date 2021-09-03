import asyncio
import pickle
import socket
from datetime import datetime
from threading import Thread

from Test_app.Dictionary import Questions
import pandas as pd
import numpy as np
from random import shuffle

class Client:
    def __init__(self, username, token, points, group):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.socket.settimeout(5)
        self.username = username
        self.token = token
        self.points = str(points)
        self.group = group
        self.room = 'none'
        self.role = 'none'
        self.first_message = True


class Server:
    def __init__(self, admin):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.admin = admin
        self.main_loop = asyncio.new_event_loop()
        self.dictionary = {'ip': [], 'token': [], 'ФИО': [], 'Баллы за тест': [], 'Баллы за практику': []}
        self.dict = Questions()
        self.defend_questions = self.random_questions()
        self.users = []
        self.question_index = 0
        self.available_rooms = []
        for i in range(12):
            self.available_rooms.append(i)
            self.available_rooms.append(i)

        self.attack_defend = {}
        self.ip_list = []
        for i in range(5):
            ip = "10.10.10.0" + str(i + 1)
            self.ip_list.append(ip)
            self.attack_defend["sudo "+ ip + " bruteforce"] = "sudo " +\
                               "add rule name=BLOCK IP ADDRESS - " + ip + " dir=in action=block"
        print(self.attack_defend)
        self.points_practice = 0
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

        self.functions = [self.server_first_connection, self.server_message_from_attacker,
                          self.server_message_from_defender]

    async def server_first_connection(self, args):
        # args = [token, username, points, ip, listened_socket]
        print('Enter')
        token = args[0]
        username = args[1]
        score = args[2]
        ip = args[3]
        listened_socket = args[4]
        # Создаем эксель файл с полученными данными
        self.create_dict(ip, token, username, score)
        # Выбираем комнату и роль для игрока и далее отправляем эти данные пользователю
        room = self.available_rooms[0]
        self.info[room]['ip'].append(ip)
        self.info[room]['socket'].append(listened_socket)
        print(listened_socket, self.info[room])
        role = self.info[room]['role'][0]

        self.available_rooms.remove(room)
        self.info[room]['role'].remove(role)

        data = {'key': 0, 'info': [username, room, role, self.admin.canvas.net]}

        data_encode = pickle.dumps(data)
        await self.send_data(room, data_encode, socket=listened_socket)

    async def server_message_from_attacker(self, args):
        # args = [username, room, result, ip, listened_socket]
        username = args[0]
        room = args[1]
        result = args[2]
        listened_socket = args[4]
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
            socket_to_send = listened_socket

        # Обновление значений в эксель таблице
        self.create_dict(username=username, score_practice=self.info[room]['points'][0])

        data_encode = pickle.dumps(data)
        await self.send_data(room, data_encode, socket=socket_to_send)

    async def server_message_from_defender(self, args):
        # args = [username, room, result, ip, listened_socket]
        username = args[0]
        room = args[1]
        result = args[2]
        listened_socket = args[4]
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

        if type(data) == list:
            data_encode = pickle.dumps(data[0])
            await self.send_data(room, data_encode)
            data_encode = pickle.dumps(data[1])
            await self.send_data(room, data_encode, socket=socket_to_send)
        else:
            data_encode = pickle.dumps(data)
            await self.send_data(room, data_encode, socket=socket_to_send)

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
    async def send_data(self, room, data=None, socket=None):
        # Если socket is None, то сервер отправляет всем клиентам в комнате, иначе конкретному клиенту по адресу сокета
        if socket is None:
            for user in self.info[room]['socket']:
                await self.main_loop.sock_sendall(user, data)
        else:
            await self.main_loop.sock_sendall(socket, data)

    # Просмотр сообщений от клиентов
    async def listen_socket(self, ip, listened_socket=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 4096)
                data_decode = pickle.loads(data)
                data_decode['info'].extend([ip, listened_socket])

                await self.functions[data_decode['key']](data_decode['info'])

            except ConnectionResetError:
                print('Пользователь вышел')
                for room in range(12):
                    if listened_socket in self.info[room]['socket']:
                        self.create_txt(room, self.info[room]['text'])

                        self.info[room]['ip'].remove(ip)
                        self.info[room]['socket'].remove(listened_socket)
                        self.users.remove(listened_socket)
                return

    # Создание эксель таблицы
    def create_dict(self, address=None, token=None, username=None, score=None, score_practice=None):
        if address is not None:
            self.dictionary['ip'].append(address)
            self.dictionary['token'].append(token)
            self.dictionary['ФИО'].append(username)
            self.dictionary['Баллы за тест'].append(str(score))
        if score_practice is None:
            self.dictionary['Баллы за практику'].append('0')
        else:
            for i in range(len(self.dictionary['ФИО'])):
                if username == self.dictionary['ФИО'][i]:
                    self.dictionary['Баллы за практику'][i] = str(score_practice)
        data_m = pd.DataFrame(self.dictionary)
        writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
        data_m.to_excel(writer, 'Sheet1')
        writer.save()

    # Подключаем пользователей
    async def accept_sockets(self):
        i = 0
        while True:
            i += 1
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"Пользователь <{address[0]}> подключился!")
            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(address[0], user_socket))

    # Создание текстового файла, когда один из игроков в комнате закрывает приложение
    def create_txt(self, room, message):
        text = open(self.info[room]['txt_file'], 'w')
        text.write(message)
        text.close()

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

    def start(self):
        self.main_loop.run_until_complete(self.main())
