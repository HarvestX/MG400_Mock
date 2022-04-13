from abc import abstractmethod
import socket
from threading import Thread

import logging


class TcpSocket(Thread):

    MAX_RECEIVE_BYTES = 1024

    ip: str = None
    port: int = None
    logger: logging.Logger = None

    @abstractmethod
    def callback(self, socket, max_receive_bytes):
        pass

    def __init__(self, ip: str, port: int, callback) -> None:
        super().__init__()
        self.__callback = callback

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._ip, self._port))
            s.listen(10)
            self.__callback(s, self.MAX_RECEIVE_BYTES)
