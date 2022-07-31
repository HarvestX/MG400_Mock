"""Dobot DashBoard Commands."""

from dobot_command.dobot_hardware import DobotHardware


class DashboardCommands:
    """DashboardCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def ClearError(self):
        """ClearError"""
        self.__dobot.lock_mutex()
        self.__dobot.clear_error()
        self.__dobot.release_mutex()
