import socket
import threading

address = "127.0.0.1"
users = []
server = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,
                )
server.bind(
                    (address, 1234) #localhost
                )
server.listen(5)


def start_server():
    while True:
        user_socket, address = server.accept()
        print(f"Юзер <{address[0]}> присоединился!")

        users.append(user_socket)

        listen_accepted_user = threading.Thread(target=listen_user,
                     args=(user_socket, )
                     )

        listen_accepted_user.start()


def send_all(data):
    for user in users:
        user.send(data.encode("utf-8"))


def listen_user(user):
    while True:
        data = user.recv(2048).decode("utf-8")
        print("Юзер отправил {}".format(data))
        send_all("Юзер внес изменение: "+data)

if __name__ == '__main__':
    print(f"Сервер запущен {address} запущен.")
    start_server()