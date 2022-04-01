import socket
from threading import Thread

import logging


class TcpSocket(Thread):

    MAX_RECEIVE_BYTES = 1024

    ip: str = None
    port: int = None
    logger: logging.Logger = None

    def __init__(self, name: str, ip: str, port: int) -> None:
        super().__init__()
        self._ip = ip
        self._port = port
        self.logger = logging.getLogger(name)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._ip, self._port))
            s.listen(10)
            connection, _ = s.accept()
            with connection:
                while True:
                    recv = connection.recv(self.MAX_RECEIVE_BYTES).decode()
                    if not recv:
                        continue

                    self.logger.info(recv)
                    connection.send((recv + ' returned.').encode())
