"""Motion Tcp Interface."""

from .function_parser import FunctionParser
from .tcp_interface_base import TcpInterfaceBase
from queue import Queue
import logging

from dobot_command.motion_command import MotionCommands


class MotionTcpInterface(TcpInterfaceBase):

    logger: logging.Logger
    __socket_pool: Queue

    def __init__(self, ip: str, port: int, motion_commands: MotionCommands) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger("Motion Tcp Interface")
        self.__socket_pool = Queue()
        self.__motion_commands = motion_commands

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
                        FunctionParser.exec(self.__motion_commands, recv)
                    except ValueError as err:
                        self.logger.error(err)
