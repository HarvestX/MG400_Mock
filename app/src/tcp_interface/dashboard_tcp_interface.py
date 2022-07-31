"""Dashboard Tcp Interface."""

import logging

from dobot_command.dashboard_command import DashboardCommands
from .function_parser import FunctionParser
from .tcp_interface_base import TcpInterfaceBase


class DashboardTcpInterface(TcpInterfaceBase):
    """DashboardTcpInterface"""
    logger: logging.Logger

    def __init__(
        self, ip: str, port: int, dashboard_commands: DashboardCommands
    ) -> None:
        super().__init__(ip, port, self.callback)
        self.__dashboard_commands = dashboard_commands
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
                        FunctionParser.exec(self.__dashboard_commands, recv)
                    except ValueError as err:
                        self.logger.error(err)

                    connection.send((recv + " returned.").encode())
