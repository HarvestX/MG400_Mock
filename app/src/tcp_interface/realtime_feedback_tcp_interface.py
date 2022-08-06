"""Realtime Feedback Tcp Interface."""

from queue import Queue

import logging
import time
from socket import error as SocketError

from .tcp_interface_base import TcpInterfaceBase

from dobot_command.dobot_hardware import DobotHardware


class RealtimeFeedbackTcpInterface(TcpInterfaceBase):
    """RealtimeFeedbackTcpInterface"""
    logger: logging.Logger
    __realtime_feedback_period: float = 8.0 / 1000
    __socket_pool: Queue

    def __init__(self, ip: str, port: int, dobot: DobotHardware) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger("RealtimeFeedback Tcp Interface")
        self.__socket_pool = Queue()
        self.__dobot = dobot

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            self.__socket_pool.put(connection)
            with connection:
                while True:
                    try:
                        packet = self.__dobot.update_status(
                            self.__realtime_feedback_period)
                        connection.send(packet)
                    except SocketError:
                        connection.close()
                        break

                    time.sleep(self.__realtime_feedback_period)
