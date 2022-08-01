"""MG400 Mock Initial File."""

import logging

import tcp_interface
from dobot_command.dobot_hardware import DobotHardware

logging.basicConfig(level=logging.INFO)


def main():
    """MG400 Mock Initial Point"""
    dobot = DobotHardware()

    dashboard_tcp = tcp_interface.DashboardTcpInterface(
        "172.10.0.3", 29999, dobot
    )

    motion_tcp = tcp_interface.MotionTcpInterface(
        "172.10.0.3", 30003, dobot
    )

    feedback_tcp = tcp_interface.RealtimeFeedbackTcpInterface(
        "172.10.0.3", 30004, dobot
    )

    dashboard_tcp.start()
    motion_tcp.start()
    feedback_tcp.start()


if __name__ == "__main__":
    main()
