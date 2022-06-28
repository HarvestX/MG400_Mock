import tcp_interface

import logging
logging.basicConfig(level=logging.INFO)


def main():
    dashboard_tcp = tcp_interface.DashboardTcpInterface(
        '172.10.0.3', 29999)

    motion_tcp = tcp_interface.MotionTcpInterface(
        '172.10.0.3', 30003)

    feedback_tcp = tcp_interface.RealtimeFeedbackTcpInterface(
        '172.10.0.3', 30004)

    dashboard_tcp.start()
    motion_tcp.start()
    feedback_tcp.start()


if __name__ == "__main__":
    main()
