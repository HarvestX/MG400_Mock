"""Dobot DashBoard Commands."""

import dobot_command.robot_mode as robot_mode
from dobot_command.dobot_hardware import DobotHardware
from dobot_command.return_msg_generator import generate_return_msg


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
