import logging
from queue import Queue

from dobot_command.motion_command import MotionCommands

from .function_parser import FunctionParser
from .tcp_interface_base import TcpInterfaceBase


class MotionTcpInterface(TcpInterfaceBase):

    logger: logging.Logger
    __socket_pool: Queue

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger('Motion Tcp Interface')
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
                        FunctionParser.exec(MotionCommands(), recv)
                    except ValueError as err:
                        self.logger.error(err)