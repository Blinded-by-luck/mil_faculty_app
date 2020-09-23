from Socket import Socket
from threading import Thread


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect(
            ("127.0.0.1", 1234)
        )

        listen_thread = Thread(target=self.listen_socket)
        listen_thread.start()

        send_thread = Thread(target=self.listen_socket)
        send_thread.start()

    def listen_socket(self, listen_socket=None):
        while True:
            data = self.recv(2048)  # recieve
            print("\n", data.decode("utf-8"))

    def send_data(self, data):
        self.send(data.encode('utf-8'))



if __name__ == "__main__":
    client = Client()
    client.set_up()
    client.send_data(input())