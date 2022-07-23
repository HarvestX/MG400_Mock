import tcp_interface

from dobot_command.dashboard_command import DashboardCommands
from dobot_command.motion_command import MotionCommands
from dobot_command.dobot_hardware import DobotHardware
import logging

logging.basicConfig(level=logging.INFO)


def main():
    dobot = DobotHardware()
    dashboard_commands = DashboardCommands(dobot)
    motion_commands = MotionCommands(dobot)

    dashboard_tcp = tcp_interface.DashboardTcpInterface(
        "172.10.0.3", 29999, dashboard_commands
    )

    motion_tcp = tcp_interface.MotionTcpInterface(
        "172.10.0.3", 30003, motion_commands
    )

    feedback_tcp = tcp_interface.RealtimeFeedbackTcpInterface(
        "172.10.0.3", 30004, dobot
    )

    dashboard_tcp.start()
    motion_tcp.start()
    feedback_tcp.start()


if __name__ == "__main__":
    main()
