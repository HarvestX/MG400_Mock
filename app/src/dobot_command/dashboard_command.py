"""Dobot DashBoard Commands."""

from dobot_command.dobot_hardware import DobotHardware, RobotMode


class DashboardCommands:
    """DashboardCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot
        self.none = "None"

    def EnableRobot(self, **kwargs) -> str:
        """EnableRobot"""
        error_id = self.__dobot.get_error_id()
        if error_id == 0:
            self.__dobot.set_robot_mode(RobotMode().mode_init)
            return str(error_id)
        else:
            return str(error_id)

    def DisableRobot(self) -> str:
        """DisableRobot"""
        return self.none

    def ClearError(self) -> str:
        """ClearError"""
        self.__dobot.clear_error()
        return self.none

    def GetErrorID(self) -> str:
        """GetErrorID"""
        return self.none
