"""Dobot DashBoard Commands."""

from dobot_command.dobot_hardware import DobotHardware


class DashboardCommands:
    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def ClearError(self) -> str:
        self.__dobot.clear_error()
        return "null"
