from Roles.admin.interface_admin import Admin
from Roles.attacker.interface_attacker import Attacker
from Server_Client.Socket import Socket
from PyQt5 import QtWidgets
from datetime import datetime
from os import system
import asyncio

from Test_app.Test_app import TestApp


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""
        self.username = ''
        self.separator = '4&**@'
        self.run_test = True
        self.room = None

    def set_up(self):
        try:
            self.socket.connect(
                ('127.0.0.1', 1234)
            )
        except ConnectionRefusedError:
            print('Сервер недоступен')
            exit(0)

        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            data = data.decode('utf-8')

            if data.split(self.separator)[0] == 'r':
                self.room = 'room_' + data.split(self.separator)[1].split(' ')[3]
                print(data.split(self.separator)[1])
            else:
                self.messages = f"{str(datetime.now().time()).split('.')[0]}:  {data}\n"

                system('cls')
                print(self.messages)

    async def send_data(self, data=None):
        while True:
            if self.run_test:
                app = QtWidgets.QApplication([])
                application = TestApp()
                application.show()
                app.exec()
                data = 't ' + application.get_token()
                self.username = application.get_username()
                self.run_test = False
                app1 = QtWidgets.QApplication([])
                application1 = Admin()
                application1.show()
                app1.exec()
            else:
                data = await self.main_loop.run_in_executor(None, input)
                data = self.username + self.separator + self.room + self.separator + data
            await self.main_loop.sock_sendall(self.socket, data.encode('utf-8'))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == '__main__':
    client = Client()
    client.set_up()
    client.start()
