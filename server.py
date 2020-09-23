from Socket import Socket
import threading

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.bind(("localhost", 1234))
        self.listen(2)
        print("Server is listening\n")

        self.users = []

    def set_up(self):
        self.accept_sockets()

    def send_data(self, data):
        for user in self.users:
            user.send(data)

    def listen_socket(self, listen_socket=None):
        print("Listening user")

        while True:
            data = listen_socket.recv(2048)
            print(f"User sent {data}")

            self.send_data(data)

    def accept_sockets(self):
        while True:
            user_socket, address = self.accept()
            print(f"User <{address[0]}> connected!")
            user_socket.send("You are connected".encode("utf-8"))
            self.users.append(user_socket)

            listen_accepted_user = threading.Thread(target=self.listen_socket,
                             args=(user_socket, )
                             )
            listen_accepted_user.start()






if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.accept_sockets()