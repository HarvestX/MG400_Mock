"""Tcp Interface Base."""

import socket as so
from abc import abstractmethod
from threading import Thread


class TcpInterfaceBase(Thread):
    """TcpInterfaceBase"""
    MAX_RECEIVE_BYTES = 1024

    __ip: str
    __port: int

    @abstractmethod
    def callback(self, socket, max_receive_bytes):
        """callback"""

    def __init__(self, ip: str, port: int, callback) -> None:
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__callback = callback

    def run(self):
        with so.socket(so.AF_INET, so.SOCK_STREAM) as skt:
            skt.bind((self.__ip, self.__port))
            skt.listen(10)
            self.__callback(skt, self.MAX_RECEIVE_BYTES)
