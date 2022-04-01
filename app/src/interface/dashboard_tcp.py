from .tcp_socket import TcpSocket


class DashboardTcp(TcpSocket):
    def __init__(self, ip: str, port: int) -> None:
        super().__init__('DashboartTcp', ip, port)
