import socket
import threading

users = []
server = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,
                )
server.bind(
                    ("127.0.0.1", 1234) #localhost
                )
server.listen(5)


def start_server():
    while True:
        user_socket, address = server.accept()
        print(f"User <{address[0]}> connected!")

        users.append(user_socket)
        listen_accepted_user = threading.Thread(target=listen_user,
                     args=(user_socket, )
                     )

        listen_accepted_user.start()


def send_all(data):
    for user in users:
        user.send(data)


def listen_user(user):
    print("Listening user")
    while True:
        data = user.recv(2048)
        print("User sent {}".format(data))
        send_all(data)

if __name__ == '__main__':
    start_server()