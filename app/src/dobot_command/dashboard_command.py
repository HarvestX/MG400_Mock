"""Dobot DashBoard Commands."""

from dobot_command import robot_mode
from dobot_command.dobot_hardware import DobotHardware
from utilities.return_msg_generator import generate_return_msg


class DashboardCommands:
    """DashboardCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def EnableRobot(self, args) -> str:
        """EnableRobot"""
        # TODO: to be acceptable optional args.
        _ = args  # for pylint waring
        error_id = self.__dobot.get_error_id()
        self.__dobot.set_robot_mode(robot_mode.MODE_ENABLE)
        return generate_return_msg(error_id)

    def DisableRobot(self, args) -> str:
        """DisableRobot"""
        _ = args  # for pylint waring
        error_id = self.__dobot.get_error_id()
        self.__dobot.set_robot_mode(robot_mode.MODE_DISABLED)
        return generate_return_msg(error_id)

    def ClearError(self, args) -> str:
        """ClearError"""
        _ = args  # for pylint waring
        self.__dobot.clear_error()
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)

    def GetErrorID(self, args) -> str:
        """GetErrorID"""
        _ = args  # for pylint waring
        collision = self.__dobot.get_collision_status()
        collision_msg = "["
        for val in collision:
            if val is None:
                collision_msg += "[],"
            else:
                collision_msg += "[" + str(val) + "],"
        collision_msg = collision_msg[:-1] + "]"
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id, [collision_msg])

    def ResetRobot(self, args):
        """ResetRobot"""
        _ = args  # for pylint waring
        self.__dobot.set_robot_mode(robot_mode.MODE_ENABLE)

    def SpeedFactor(self, args):
        """SpeedFactor"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The SpeedFactor command has not yet been implemented.")

    def AccJ(self, args):
        """AccJ"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The AccJ command has not yet been implemented.")

    def AccL(self, args):
        """AccL"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The AccL command has not yet been implemented.")

    def SpeedJ(self, args):
        """SpeedJ"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The SpeedJ command has not yet been implemented.")

    def SpeedL(self, args):
        """SpeedL"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The SpeedL command has not yet been implemented.")
