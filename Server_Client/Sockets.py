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
        # separator используется для стабильности при передаче сообщений. Помимо того, что серверу и клиенту нужно
        # передавать сообщения пользователей, ему еще нужно передавать информацию о комнате, имени игрока и так далее.
        # Поэтому нужно использовать набор символов, который пользователь вряд ли когда-то введет
        # Также separator на сервере и клиенте должен быть одинаковым
        self.separator = '$%6h))/.qyjrgKUTFV^Shc8~~63,c'
        self.role = 'none'
        self.first_message = True


class Server:
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.main_loop = asyncio.new_event_loop()
        self.dictionary = {'ip': [], 'token': [], 'ФИО': [], 'Баллы за тест': [], 'Баллы за практику': []}
        self.dict = Questions()
        self.defend_questions = self.random_questions()
        self.users = []
        self.question_index = 0
        # separator используется для стабильности при передаче сообщений. Помимо того, что серверу и клиенту нужно
        # передавать сообщения пользователей, ему еще нужно передавать информацию о комнате, имени игрока и так далее.
        # Поэтому нужно использовать набор символов, который пользователь вряд ли когда-то введет
        self.separator = '$%6h))/.qyjrgKUTFV^Shc8~~63,c'
        self.available_rooms = []
        for i in range(1, 13):
            self.available_rooms.append(i)
            self.available_rooms.append(i)
        # Если используем сервер для практической части, а не для общения
        self.flag_practical = True
        self.attack_defend = {'атаковать комп 1 ddos': 'защитить комп 1 ddos',
                              'атаковать комп 1 пароль': 'защитить комп 1 пароль',
                              'атаковать комп 2 ddos': 'защитить комп 2 ddos',
                              'атаковать комп 2 пароль': 'защитить комп 2 пароль',
                              'атаковать комп 3 ddos': 'защитить комп 3 ddos',
                              'атаковать комп 3 пароль': 'защитить комп 3 пароль',
                              'атаковать комп 4 ddos': 'защитить комп 4 ddos',
                              'атаковать комп 4 пароль': 'защитить комп 4 пароль'}

        self.points_practice = 0
        self.info = {'room_1': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_1.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_2': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_2.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_3': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_3.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_4': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_4.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_5': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_5.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_6': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_6.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_7': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_7.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_8': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_8.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_9': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_9.txt',
                                       'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_10': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_10.txt',
                                        'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_11': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_11.txt',
                                        'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]},
                            'room_12': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_12.txt',
                                        'text': '', 'role': ['attack', 'defend'], 'last_action': '', 'points': [0, 0]}}
        self.functions = [self.server_code0, self.server_code1, self.server_code2]

    # code0 - первое сообщение
    def server_code0(self, args, ip, listened_socket):
        # args = [token, username, points]
        print('Enter')
        token = args[0]
        username = args[1]
        score = args[2]
        # Создаем эксель файл с полученными данными
        self.create_dict(ip, token, username, score)
        # Выбираем комнату и роль для игрока и далее отправляем эти данные пользователю
        room = self.available_rooms[0]
        self.info['room_' + str(room)]['ip'].append(ip)
        self.info['room_' + str(room)]['socket'].append(listened_socket)
        print(listened_socket, self.info['room_' + str(room)])
        role = self.info['room_' + str(room)]['role'][0]

        self.available_rooms.remove(room)
        self.info['room_' + str(room)]['role'].remove(role)

        data = {'key': 0, 'info': [username, room, role]}
        return data, 'room_' + str(room)

    # code1 - сообщение от атакующего
    def server_code1(self, args, listened_socket):
        # args = [username, room, role, result]
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
        elif result in [0, 1]:
            data = {'key': 2, 'info': [result]}
            socket_to_send = None
        # Если написал что-то, чего нет в командах для атакующего
        else:
            data = {'key': 3, 'info': [username]}
            socket_to_send = listened_socket

        # Обновление значений в эксель таблице
        self.create_dict(username=username, score_practice=self.info[room]['points'][0])
        return data, socket_to_send, room

    # code2 - сообщение от защитника
    def server_code2(self, args, listened_socket):
        # args = [username, room, role, result]
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
        return data, socket_to_send, room

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
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                data_decode = pickle.loads(data)

                # Если это первое сообщение, то получаем информацию о токене, фио и количество очков за тест
                if data_decode['key'] == 0:
                    data, room = self.functions[data_decode['key']](data_decode['info'], ip, listened_socket)
                    data_encode = pickle.dumps(data)
                    await self.send_data(room, data_encode, socket=listened_socket)
                elif data_decode['key'] == 1:
                    data, socket_to_send, room = self.functions[data_decode['key']](data_decode['info'], listened_socket)
                    data_encode = pickle.dumps(data)
                    await self.send_data(room, data_encode, socket=socket_to_send)
                elif data_decode['key'] == 2:
                    data, socket_to_send, room = self.functions[data_decode['key']](data_decode['info'], listened_socket)
                    if type(data) == list:
                        data_encode = pickle.dumps(data[0])
                        await self.send_data(room, data_encode)
                        data_encode = pickle.dumps(data[1])
                        await self.send_data(room, data_encode, socket=socket_to_send)
                    else:
                        data_encode = pickle.dumps(data)
                        await self.send_data(room, data_encode, socket=socket_to_send)

                '''else:
                    # Если выбираем режим сервера для практической части
                    if self.flag_practical:
                        await self.practical_part(data_decode, listened_socket)

                    # Если сервер настроен на простое общение в комнатах
                    else:
                        username = data_decode.split(self.separator)[0]
                        room = data_decode.split(self.separator)[1]
                        role = data_decode.split(self.separator)[2]
                        message = data_decode.split(self.separator)[3]
                        if username not in self.info[room]['username']:
                            self.info[room]['username'].append(username)

                        message_to_send = '(' + username + ') ' + message
                        print(username + '(' + room + ')' + ':', message)
                        self.info[room]['text'] += str(datetime.now().time()).split('.')[
                                                              0] + ':' + message_to_send

                        await self.send_data(room, message_to_send.encode('utf-8'))'''

            except ConnectionResetError:
                print('Пользователь вышел')
                for room in self.info.keys():
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

    # Практическая часть
    async def practical_part(self, data_decode, socket):
        username = data_decode.split(self.separator)[0]
        room = data_decode.split(self.separator)[1]
        role = data_decode.split(self.separator)[2]
        message = data_decode.split(self.separator)[3].lower()
        # Записываем все сообщения в переменную text, из которой позже будет сформирован txt файл
        self.info[room]['text'] += str(datetime.now().time()).split('.')[0] + ':' + '(' + username + ')' + message + '\n'

        if username not in self.info[room]['username']:
            self.info[room]['username'].append(username)

        # Если пришло сообщение от атакующего
        if role == 'attack':
            print('Message from attacker: ', message)
            # Если команда верная
            if message in self.attack_defend.keys():
                # Записываем в self.server.info[room]['last_action'] команду, чтобы защищающийся ввел команду, которая
                # защищает конкретно от этого вида атаки
                self.info[room]['last_action'] = message
                message_to_send = 'attack_correct' + self.separator + username + ' предпринял атаку (' + message + ')'
                # Добавление одного очка за верно написанную команду по атаке
                self.info[room]['points'][0] += 1
                # Отправка верной атаки всем в комнате
                await self.send_data(room, message_to_send.encode('utf-8'))
            elif message == 'атакующий неправильно ответил на вопрос':
                message_to_send = 'incorrect' + self.separator + message
                await self.send_data(room, message_to_send.encode('utf-8'))
            elif message == 'атакующий правильно ответил на вопрос':
                message_to_send = 'incorrect' + self.separator + message
                await self.send_data(room, message_to_send.encode('utf-8'))
            # Если написал что-то, чего нет в командах для атакующего
            else:
                message_to_send = 'incorrect' + self.separator + username + ', нельзя использовать данную атаку ' \
                                  + '(' + message + ')'
                # Отправка сообщения о неверной команде только атакующему
                await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Обновление значений в эксель таблице
            self.create_dict(username=username, score_practice=self.info[room]['points'][0])

        # Если пришло сообщение от защищающегося
        else:
            print('Message from defender:', message)
            # Если атакующий еще не совершил атаку
            if self.info[room]['last_action'] == '':
                message_to_send = 'incorrect' + self.separator + username + ', на данную сеть не совершенно никаких атак'
                # Отправка сообщения только защитнику
                await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Если атакующий уже совершил атаку
            else:
                # Если команда защитника защищает от типа нападения атакующего
                if self.attack_defend[self.info[room]['last_action']] == message:
                    message_to_send = 'defend_correct1' + self.separator + username + ' предпринял защиту (' + message +\
                                      ')' + '\nЗащитник воздействовал вопросом'
                    self.info[room]['last_action'] = ''
                    # Добавление одного очка за верно написанную команду по защите
                    self.info[room]['points'][1] += 1
                    # Отправка верной защиты всем в комнате
                    await self.send_data(room, message_to_send.encode('utf-8'))

                    # Отправка вопроса нападающему
                    question = self.defend_questions[self.question_index]
                    answer1 = '\n1) ' + self.dict.quest[question][0][1]
                    answer2 = '\n2) ' + self.dict.quest[question][1][1]
                    answer3 = '\n3) ' + self.dict.quest[question][2][1] + '\n'
                    correct = None
                    for i in range(3):
                        if self.dict.quest[question][i][2] == 1:
                            correct = str(i + 1)
                    message_to_send = 'defend_correct2' + self.separator + '\n' + question[1] + answer1 + answer2 +\
                                      answer3 + self.separator + correct
                    self.question_index += 1
                    await self.send_data(room, message_to_send.encode('utf-8'), socket=self.info[room]['socket'][0])

                # Если написана неверная команда или команда не соответствует типу нападения
                else:
                    message_to_send = 'incorrect' + self.separator + username + ', нельзя использовать данную защиту' +\
                                      '(' + message + ')'
                    # Отправка сообщения о недопустимости использования команды только защитнику
                    await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Обновление значений в эксель таблице
            self.create_dict(username=username, score_practice=self.info[room]['points'][1])

    # Создание текстового файла, когда один из игроков в комнате закрывает приложение
    def create_txt(self, room, message):
        text = open(self.info[room]['txt_file'], 'w')
        text.write(message)
        text.close()

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

    def start(self):
        self.main_loop.run_until_complete(self.main())












