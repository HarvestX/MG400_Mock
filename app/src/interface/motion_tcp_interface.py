from .function_parser import FunctionParser
from .tcp_socket import TcpSocket
from .realtime_packet import RealtimePacket
from queue import Queue
import logging

from dobot_command.realtime_command import RealtimeCommands


class MotionTcpInterface(TcpSocket):

    logger: logging.Logger = None
    __socket_pool: Queue = None

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger('MotionTcp')
        self.__socket_pool = Queue()

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

                    try:
                        FunctionParser.exec(RealtimeCommands(), recv)
                    except ValueError as err:
                        self.logger.error(err)