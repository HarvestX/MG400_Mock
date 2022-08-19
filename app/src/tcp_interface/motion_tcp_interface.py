"""Motion Tcp Interface."""

import logging
from queue import Queue

from dobot_command.dobot_hardware import DobotHardware

from .tcp_interface_base import TcpInterfaceBase


class MotionTcpInterface(TcpInterfaceBase):
    """MotionTcpInterface"""
    logger: logging.Logger
    __socket_pool: Queue

    def __init__(self, ip: str, port: int, dobot: DobotHardware) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger("Motion Tcp Interface")
        self.__socket_pool = Queue()
        self.__dobot = dobot

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            self.__socket_pool.put(connection)
            with connection:
                while True:
                    recv = connection.recv(max_receive_bytes).decode()
                    if not recv:
                        break
                    self.logger.info(recv)
                    self.__dobot.motion_stack(recv)
