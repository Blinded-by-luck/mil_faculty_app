from Socket import Socket
import asyncio
import PyQt5
import pandas as pd
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

    def set_up(self):
        self.socket.bind(('127.0.0.1', 1234))
        self.socket.listen(3)
        self.socket.setblocking(False)

    async def send_data(self, data=None):
        for user in self.users:
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
                else:
                    print(data_decode.split('#')[0] + ':', data_decode.split('#')[1])
                    await self.send_data(data_decode.split('#')[1].encode('utf-8'))
            except ConnectionResetError:
                print('Пользователь вышел')
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



    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

        #xls()

if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()