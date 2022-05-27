from .function_parser import FunctionParser
from .tcp_socket import TcpSocket
from .realtime_packet import RealtimePacket
from threading import Thread
from queue import Queue
import logging
import socket
import time

from dobot_command.realtime_command import RealtimeCommands


class RealtimeTcp(TcpSocket):

    logger: logging.Logger = None
    __realtime_feedback_period: float = 20.0 / 1000
    __socket_pool: Queue = None
    __feed_back_sender: Thread = None

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger('RealtimeTcp')
        self.__socket_pool = Queue()

        self.__feed_back_sender = Thread(target=self.__real_time_feedback)
        self.__feed_back_sender.start()

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            self.__socket_pool.put(connection)

            recv = connection.recv(max_receive_bytes).decode()
            self.logger.info(recv)

            try:
                FunctionParser.exec(RealtimeCommands(), recv)
            except ValueError as err:
                self.logger.error(err)

            connection.send((recv + ' returned.').encode())

    def __real_time_feedback(self):
        packet = RealtimePacket()

        while True:
            count = self.__socket_pool.qsize()
            while count:
                connection = self.__socket_pool.get()
                try:
                    connection.send(packet.packet())
                    self.__socket_pool.put(connection)
                except socket.error:
                    self.logger.info('tcp connection close')
                    connection.close()

                count = count - 1

            time.sleep(self.__realtime_feedback_period)
