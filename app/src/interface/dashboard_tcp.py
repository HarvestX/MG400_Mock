from .function_parser import FunctionParser
from .tcp_socket import TcpSocket
import logging

class DashboardTcp(TcpSocket):

    logger: logging.Logger = None

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port, self.callback)

        self.logger = logging.getLogger('DashboardTcp')

    def callback(self, socket, max_receive_bytes):
        while True:
            connection, _ = socket.accept()
            with connection:
                recv = connection.recv(max_receive_bytes).decode()
                self.logger.info(recv)

                try:
                    FunctionParser.exec(DashboardCommands(), recv)
                except ValueError as err:
                    self.logger.error(err)

                connection.send((recv + ' returned.').encode())
