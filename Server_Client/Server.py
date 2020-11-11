from Server_Client.Socket import Socket
import asyncio
import pandas as pd
from datetime import datetime
import xlsxwriter


# Table по хорошему нужно вынести в новый файл
class Table:
    def __init__(self):
        pass

    def change(self, operations=None):
        # Изменение поля в зависимости от operations
        pass


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        print('Сервер запущен')
        self.slovar = {'ip': [], 'token': []}
        self.users = []
        self.table = Table()
        self.separator = '4&**@'
        self.available_rooms = []
        for i in range(1, 13):
            self.available_rooms.append(i)
            self.available_rooms.append(i)

        self.info = {'room_1': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_1.txt', 'text': ''},
                     'room_2': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_2.txt', 'text': ''},
                     'room_3': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_3.txt', 'text': ''},
                     'room_4': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_4.txt', 'text': ''},
                     'room_5': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_5.txt', 'text': ''},
                     'room_6': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_6.txt', 'text': ''},
                     'room_7': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_7.txt', 'text': ''},
                     'room_8': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_8.txt', 'text': ''},
                     'room_9': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_9.txt', 'text': ''},
                     'room_10': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_10.txt', 'text': ''},
                     'room_11': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_11.txt', 'text': ''},
                     'room_12': {'username': [], 'ip': [], 'socket': [], 'txt_file': 'room_12.txt', 'text': ''}}

    def set_up(self):
        self.socket.bind(('127.0.0.1', 1234))
        self.socket.listen(3)
        self.socket.setblocking(False)

    async def send_data(self, room, data=None):
        for user in self.info[room]['socket']:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, ip, listened_socket=None):
        if not listened_socket:

            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                data_decode = data.decode('utf-8')
                if data_decode.split(' ')[0] == 't':
                    token = data_decode.split(' ')[1]
                    self.create_dict(ip, token)

                    room = self.available_rooms[0]
                    self.info['room_' + str(room)]['ip'].append(ip)
                    self.info['room_' + str(room)]['socket'].append(listened_socket)
                    self.available_rooms.remove(room)
                    data = 'r' + self.separator + 'Вы присоединились к ' + str(room) + ' комнате'

                    await self.main_loop.sock_sendall(listened_socket, data.encode('utf-8'))
                else:
                    username = data_decode.split(self.separator)[0]
                    room = data_decode.split(self.separator)[1]
                    message = data_decode.split(self.separator)[2]
                    if username not in self.info[room]['username']:
                        self.info[room]['username'].append(username)

                    message_to_send = '(' + username + ') ' + message
                    print(username + '(' + room + ')' + ':', message)
                    self.info[room]['text'] += str(datetime.now().time()).split('.')[0] + ':' + message_to_send + '\n'
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

    async def accept_sockets(self):
        i = 0
        while True:
            i += 1
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"Пользователь <{address[0]}> подключился!")
            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(address[0], user_socket))

    def create_dict(self, address, token):
        self.slovar['ip'].append(address)
        self.slovar['token'].append(token)
        data_m = pd.DataFrame(self.slovar)
        writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
        data_m.to_excel(writer, 'Sheet1')
        writer.save()

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