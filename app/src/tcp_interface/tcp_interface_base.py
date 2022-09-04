"""Tcp Interface Base."""
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

import socket as so
from abc import abstractmethod
from threading import Thread


class TcpInterfaceBase(Thread):
    """TcpInterfaceBase"""
    MAX_RECEIVE_BYTES = 1024

    __ip: str
    __port: int

    @abstractmethod
    def callback(self, socket, max_receive_bytes):
        """callback"""

    def __init__(self, ip: str, port: int, callback) -> None:
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__callback = callback

    def run(self):
        with so.socket(so.AF_INET, so.SOCK_STREAM) as skt:
            skt.bind((self.__ip, self.__port))
            skt.listen(10)
            self.__callback(skt, self.MAX_RECEIVE_BYTES)
