"""Realtime Feedback Tcp Interface."""

from .tcp_interface_base import TcpInterfaceBase
from .realtime_packet import RealtimePacket
from queue import Queue
import logging
from socket import error as SocketError
import time

from dobot_command.dobot_hardware import DobotHardware


class RealtimeFeedbackTcpInterface(TcpInterfaceBase):

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
                        self.__dobot.lock_mutex()
                        self.__dobot.update_status(self.__realtime_feedback_period)
                        packet: RealtimePacket = self.__dobot.get_status()
                        self.__dobot.release_mutex()
                        connection.send(packet.packet())
                    except SocketError:
                        connection.close()

                    time.sleep(self.__realtime_feedback_period)
