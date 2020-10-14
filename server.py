from Socket import Socket
import asyncio

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

        self.users = []
        self.table = Table()

    def set_up(self):
        self.socket.bind(('127.0.0.1', 1234))
        self.socket.listen(3)
        self.socket.setblocking(False)

    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                # self.table.change(operations)
                await self.send_data(data)
            except ConnectionResetError:
                print('Пользователь вышел')
                self.users.remove(listened_socket)
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"Пользователь <{address[0]}> подключился!")

            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
