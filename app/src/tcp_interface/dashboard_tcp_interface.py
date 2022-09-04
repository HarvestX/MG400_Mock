"""Dashboard Tcp Interface."""
# Copyright 2022 HarvestX Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from dobot_command.dashboard_command import DashboardCommands
from dobot_command.dobot_hardware import DobotHardware
from utilities.function_parser import FunctionParser

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

                    return_str = res+recv+";"
                    print("RETURN: " + return_str)
                    connection.send((return_str).encode())
