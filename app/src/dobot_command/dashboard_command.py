"""Dobot DashBoard Commands."""

from dobot_command.dobot_hardware import DobotHardware, RobotMode
from dobot_command.return_msg_generator import generate_return_msg


class DashboardCommands:
    """DashboardCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def EnableRobot(self, *args) -> str:
        """EnableRobot"""
        error_id = self.__dobot.get_error_id()
        if error_id == 0:
            self.__dobot.set_robot_mode(RobotMode().mode_init)
            return generate_return_msg(error_id, [error_id])
        else:
            return generate_return_msg(error_id, [error_id])

    def DisableRobot(self) -> str:
        """DisableRobot"""
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)

    def ClearError(self) -> str:
        """ClearError"""
        self.__dobot.clear_error()
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)

    def GetErrorID(self) -> str:
        """GetErrorID"""
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)
