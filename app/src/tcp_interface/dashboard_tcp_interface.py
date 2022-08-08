"""Dashboard Tcp Interface."""

import logging

from dobot_command.dashboard_command import DashboardCommands
from dobot_command.dobot_hardware import DobotHardware

from .function_parser import FunctionParser
from .tcp_interface_base import TcpInterfaceBase


class DashboardTcpInterface(TcpInterfaceBase):
    """DashboardTcpInterface"""

    logger: logging.Logger

    def __init__(self, ip: str, port: int, dobot: DobotHardware) -> None:
        super().__init__(ip, port, self.callback)
        self.__dashboard_commands = DashboardCommands(dobot)
        self.logger = logging.getLogger("Dashboard Tcp Interface")

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            with connection:
                while True:
                    recv = connection.recv(max_receive_bytes).decode()
                    if not recv:
                        break
                    self.logger.info(recv)

                    try:
                        res = FunctionParser.exec(
                            self.__dashboard_commands, recv)
                    except ValueError as err:
                        self.logger.error(err)

                    if res == self.__dashboard_commands.none:
                        return_str = recv
                    else:
                        return_str = res+","+recv

                    print("return: " + return_str)
                    connection.send((return_str).encode())
