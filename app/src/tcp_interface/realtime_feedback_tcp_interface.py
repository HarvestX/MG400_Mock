"""Realtime Feedback Tcp Interface."""
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
import time
from queue import Queue
from socket import error as SocketError

from dobot_command.dobot_hardware import DobotHardware

from .tcp_interface_base import TcpInterfaceBase


class RealtimeFeedbackTcpInterface(TcpInterfaceBase):
    """RealtimeFeedbackTcpInterface"""
    logger: logging.Logger
    __socket_pool: Queue

    def __init__(self, ip: str, port: int, dobot: DobotHardware) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger("RealtimeFeedback Tcp Interface")
        self.__socket_pool = Queue()
        self.__dobot = dobot
        self.__realtime_feedback_period: float = \
            self.__dobot.get_feedback_time()

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            self.__socket_pool.put(connection)
            with connection:
                while True:
                    try:
                        packet = self.__dobot.get_status()
                        connection.send(packet)
                    except SocketError:
                        connection.close()
                        break

                    time.sleep(self.__realtime_feedback_period)
