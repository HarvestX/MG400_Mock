import socket
from threading import Thread

class DobotServer(Thread):

    MAX_RECEIVE_BYTES = 1024

    socket_info = None

    def __init__(self, socket_info):
        self.socket_info = socket_info
        super().__init__()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.socket_info[0], self.socket_info[1]))  # IPとポート番号を指定
        s.listen(10)

        while True:
            connection, _ = s.accept()
            test = connection.recv(self.MAX_RECEIVE_BYTES).decode()
            connection.send((test + ' returned.').encode())
