from .tcp_socket import TcpSocket


class RealtimeTcp(TcpSocket):
    def __init__(self, ip: str, port: int) -> None:
        super().__init__('RealtimeTcp', ip, port)
