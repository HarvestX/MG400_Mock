"""Dobot Motion Commands."""
# Copyright 2022 HarvestX Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dobot_command import robot_mode
from dobot_command.dobot_hardware import DobotHardware
from utilities.utils_for_command import (args_parser_jog, args_parser_mov_j,
                                         args_parser_mov_l)


class MotionCommands:
    """MotionCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def MovJ(self, args):
        """MovJ"""
        # TODO: Implement user coordinate system
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 4:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        if len(args) > 4:
            user, tool, speed_j, acc_j = args_parser_mov_j(args[4:])
            if user is not None:
                self.__dobot.set_user_index(user)
            if tool is not None:
                self.__dobot.set_tool_index(tool)
            if speed_j is not None:
                self.__dobot.set_speed_j_rate(speed_j)
            if acc_j is not None:
                self.__dobot.set_acc_j_rate(acc_j)

        tool_target = list(map(float, args[0:4])) + [0.0, 0.0]
        if not self.__dobot.set_tool_vector_target(tool_target):
            self.__dobot.log_warning_msg("Failed to calculate path.")
            return False

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
        # TODO: Implement user and tool coordinate system
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 1:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        if len(args) >= 1:
            coord_type, user, tool = args_parser_jog(args[1:])
            if coord_type is not None:
                self.__dobot.set_coord_type(coord_type)
            if user is not None:
                self.__dobot.set_user_index(user)
            if tool is not None:
                self.__dobot.set_tool_index(tool)

        axis_id = args[0]
        accepted = self.__dobot.generate_jog_target(axis_id)

        if accepted:
            self.__dobot.set_robot_mode(robot_mode.MODE_JOG)
            self.__dobot.log_info_msg("The dobot accepts MoveJog command.")
            return True

        self.__dobot.log_info_msg("out of range.")
        return False

    def MovL(self, args):
        """MovL"""
        # TODO: Implement user coordinate system
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 4:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        if len(args) > 4:
            user, tool, speed_l, acc_l = args_parser_mov_l(args[4:])
            if user is not None:
                self.__dobot.set_user_index(user)
            if tool is not None:
                self.__dobot.set_tool_index(tool)
            if speed_l is not None:
                self.__dobot.set_speed_l_rate(speed_l)
            if acc_l is not None:
                self.__dobot.set_acc_l_rate(acc_l)

        tool_target = list(map(float, args[0:4])) + [0.0, 0.0]
        if not self.__dobot.set_tool_vector_target(tool_target):
            self.__dobot.log_warning_msg("Failed to calculate path")
            return False

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
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_warning_msg("The robot mode is not enable.")
            return False
        if len(args) < 4:
            self.__dobot.log_warning_msg("The number of arguments is invalid.")
            return False

        # TODO: Support options, e.g., user, tool, speed_j, acc_j, cp.
        q_target = list(map(float, args[0:4])) + [0.0, 0.0]
        if not self.__dobot.set_q_target(q_target):
            self.__dobot.log_warning_msg("The target is invalid.")
            return False

        accepted = self.__dobot.generate_target_in_joint()
        if accepted:
            self.__dobot.set_robot_mode(robot_mode.MODE_RUNNING)
            self.__dobot.reset_time_index()
            self.__dobot.log_info_msg("The dobot accepts MovJ command.")
            return True

        self.__dobot.log_warning_msg("out of range.")
        return False
