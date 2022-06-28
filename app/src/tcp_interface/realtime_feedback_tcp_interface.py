from .tcp_interface_base import TcpInterfaceBase
from .realtime_packet import RealtimePacket
from queue import Queue
import logging
from socket import error as SocketError
import time


class RealtimeFeedbackTcpInterface(TcpInterfaceBase):

    logger: logging.Logger
    __realtime_feedback_period: float = 8.0 / 1000
    __socket_pool: Queue

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger('RealtimeFeedback Tcp Interface')
        self.__socket_pool = Queue()

    def callback(self, socket, max_receive_bytes):
        packet = RealtimePacket()

        while True:
            connection, _ = socket.accept()
            self.__socket_pool.put(connection)
            with connection:
                while True:
                    try:
                        connection.send(packet.packet())
                    except SocketError:
                        connection.close()

                    time.sleep(self.__realtime_feedback_period)
