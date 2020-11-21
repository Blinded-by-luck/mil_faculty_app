from Server_Client.Socket import Socket
import asyncio
import pandas as pd
from datetime import datetime
import xlsxwriter


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        print('Сервер запущен')
        self.slovar = {'ip': [], 'token': [], 'ФИО': [], 'Баллы за тест': [], 'Баллы за практику': []}
        self.users = []
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
        self.attack_defend = {'атаковать комп1 ddos': 'защитить комп1 ddos',
                              'атаковать комп1 пароль': 'защитить комп1 пароль'}

        self.points_practika = 0
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

    # Настройка сервера
    def set_up(self):
        self.socket.bind(('127.0.0.1', 1234))
        self.socket.listen(3)
        self.socket.setblocking(False)

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
                data_decode = data.decode('utf-8')

                # Если это первое сообщение, то получаем информацию о токене, фио и количество очков за тест
                if data_decode.split(self.separator)[0] == 'first message':
                    token = data_decode.split(self.separator)[1]
                    username = data_decode.split(self.separator)[2]
                    score = data_decode.split(self.separator)[3]
                    # Создаем эксель файл с полученными данными
                    self.create_dict(ip, token, username, score)

                    # Выбираем комнату и роль для игрока и далее отправляем эти данные пользователю
                    room = self.available_rooms[0]
                    self.info['room_' + str(room)]['ip'].append(ip)
                    self.info['room_' + str(room)]['socket'].append(listened_socket)
                    role = self.info['room_' + str(room)]['role'][0]
                    if role == 'attack':
                        role_sign = ' атакует'
                    else:
                        role_sign = ' защищается'

                    self.available_rooms.remove(room)
                    self.info['room_' + str(room)]['role'].remove(role)

                    data = 'first message' + self.separator + username + ' присоединился к ' + self.separator + str(room) + \
                           self.separator + ' комнате. ' + self.separator + username + role_sign
                    await self.send_data('room_' + str(room), data.encode('utf-8'))

                    data = 'role' + self.separator + role
                    await self.send_data('room_' + str(room), data.encode('utf-8'), socket=listened_socket)

                else:
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
                        self.info[room]['text'] += str(datetime.now().time()).split('.')[0] + ':' + message_to_send

                        await self.send_data(room, message_to_send.encode('utf-8'))

            except ConnectionResetError:
                print('Пользователь вышел')
                for room in self.info.keys():
                    if listened_socket in self.info[room]['socket']:
                        self.create_txt(room, self.info[room]['text'])

                        self.info[room]['ip'].remove(ip)
                        self.info[room]['socket'].remove(listened_socket)
                        self.users.remove(listened_socket)
                return

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
            # Если команда верная
            if message in self.attack_defend.keys():
                # Записываем в self.info[room]['last_action'] команду, чтобы защищающийся ввел команду, которая
                # защищает конкретно от этого вида атаки
                self.info[room]['last_action'] = message
                message_to_send = 'attack_correct' + self.separator + username + ' предпринял атаку (' + message + ')'
                # Добавление одного очка за верно написанную команду по атаке
                self.info[room]['points'][0] += 1
                # Отправка верной атаки всем в комнате
                await self.send_data(room, message_to_send.encode('utf-8'))

            # Если написал что-то, чего нет в командах для атакующего
            else:
                message_to_send = 'incorrect' + self.separator + username + ', нельзя использовать данную атаку ' \
                                  + '(' + message + ')'
                # Отправка сообщения о неверной команде только атакующему
                await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Обновление значений в эксель таблице
            self.create_dict(username=username, score_practika=self.info[room]['points'][0])

        # Если пришло сообщение от защищающегося
        else:
            # Если атакующий еще не совершил атаку
            if self.info[room]['last_action'] == '':
                message_to_send = 'incorrect' + self.separator + username + ', на данную сеть не совершенно никаких атак'
                # Отправка сообщения только защитнику
                await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Если атакующий уже совершил атаку
            else:
                # Если команда защитника защищает от типа нападения атакующего
                if self.attack_defend[self.info[room]['last_action']] == message:
                    message_to_send = 'defend_correct' + self.separator + username + ' предпринял защиту (' + message + ')'
                    self.info[room]['last_action'] = ''
                    # Добавление одного очка за верно написанную команду по защите
                    self.info[room]['points'][1] += 1
                    # Отправка верной защиты всем в комнате
                    await self.send_data(room, message_to_send.encode('utf-8'))

                # Если написана неверная команда или команда не соответствует типу нападения
                else:
                    message_to_send = 'incorrect' + self.separator + username + ', нельзя использовать данную защиту' +\
                                      '(' + message + ')'
                    # Отправка сообщения о недопустимости использования команды только защитнику
                    await self.send_data(room, message_to_send.encode('utf-8'), socket=socket)

            # Обновление значений в эксель таблице
            self.create_dict(username=username, score_practika=self.info[room]['points'][1])

    # Создание эксель таблицы
    def create_dict(self, address=None, token=None, username=None, score=None, score_practika=None):
        if address is not None:
            self.slovar['ip'].append(address)
            self.slovar['token'].append(token)
            self.slovar['ФИО'].append(username)
            self.slovar['Баллы за тест'].append(str(score))
        if score_practika is None:
            self.slovar['Баллы за практику'].append('0')
        else:
            for i in range(len(self.slovar['ФИО'])):
                if username == self.slovar['ФИО'][i]:
                    self.slovar['Баллы за практику'][i] = str(score_practika)
        data_m = pd.DataFrame(self.slovar)
        writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
        data_m.to_excel(writer, 'Sheet1')
        writer.save()

    # Создание текстового файла, когда один из игроков в комнате закрывает приложение
    def create_txt(self, room, message):
        text = open(self.info[room]['txt_file'], 'w')
        text.write(message)
        text.close()

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
