from abc import abstractmethod
import socket
from threading import Thread


class TcpInterfaceBase(Thread):

    MAX_RECEIVE_BYTES = 1024

    __ip: str
    __port: int

    @abstractmethod
    def callback(self, socket, max_receive_bytes):
        pass

    def __init__(self, ip: str, port: int, callback) -> None:
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__callback = callback

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__ip, self.__port))
            s.listen(10)
            self.__callback(s, self.MAX_RECEIVE_BYTES)
