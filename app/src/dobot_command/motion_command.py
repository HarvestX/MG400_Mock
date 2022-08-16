"""Dobot Motion Commands."""

from dobot_command import robot_mode
from dobot_command.dobot_hardware import DobotHardware


class MotionCommands:
    """MotionCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def MovJ(self, args):
        """MovJ"""
        # TODO: to be acceptable optional args.
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 6:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        tool_target = list(map(float, args[0:6]))
        self.__dobot.set_tool_vector_target(tool_target)
        self.__dobot.register_init_status()
        accepted = self.__dobot.generate_target_in_joint()
        if accepted:
            self.__dobot.set_robot_mode(robot_mode.MODE_RUNNING)
            self.__dobot.reset_time_index()
            self.__dobot.log_info_msg("The dobot accepts MovJ command.")
            return True

        self.__dobot.log_warning_msg("out of range.")
        return False

    def MoveJog(self, args):
        """MoveJog"""
        # TODO: to be acceptable optional args.
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 1:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        axis_id = args[0]
        accepted = self.__dobot.generate_jog_target(axis_id)

        if accepted:
            self.__dobot.set_robot_mode(robot_mode.MODE_JOG)
            self.__dobot.register_init_status()
            self.__dobot.log_info_msg("The dobot accepts MoveJog command.")
            return True

        self.__dobot.log_info_msg("out of range.")
        return False

    def MovL(self, args):
        """MovL"""
        # TODO: to be acceptable optional args.
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 6:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False
        tool_target = list(map(float, args[0:6]))

        self.__dobot.set_tool_vector_target(tool_target)
        self.__dobot.register_init_status()
        accepted = self.__dobot.generate_target_in_tool()
        if accepted:
            self.__dobot.set_robot_mode(robot_mode.MODE_RUNNING)
            self.__dobot.reset_time_index()
            self.__dobot.log_info_msg("The dobot accepts MovL command.")
            return True

        self.__dobot.log_info_msg("The straight path is not feasible.")
        return False

    def JointMovJ(self, args):
        """JointMovJ"""
        _ = args  # for pylint waring
        self.__dobot.log_warning_msg(
            "The JointMovJ command has not yet been implemented.")
