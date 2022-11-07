"""Dobot DashBoard Commands."""
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
from utilities.utils_for_command import generate_return_msg


class DashboardCommands:
    """DashboardCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def __error_msg(self, error_id, smg):
        self.__dobot.set_error_id(error_id)
        self.__dobot.log_warning_msg(smg)
        return generate_return_msg(error_id)

    def __single_int_command(self, args, v_min, v_max, set_func):
        if len(args) < 1:
            return self.__error_msg(
                -20000, "The number of arguments is invalid.")

        try:
            value = int(args[0])
        except ValueError:
            return self.__error_msg(
                -30001, "The first parameter type is invalid.")

        if not v_min <= value <= v_max:
            return self.__error_msg(
                -40001, "The first parameter has an incorrect range.")

        set_func(value)
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)

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
        error_id = self.__dobot.get_error_id()
        # TODO: Chekc error id.
        # Some error id is not clearable
        self.__dobot.clear_error()
        self.__dobot.set_robot_mode(robot_mode.MODE_ENABLE)
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
        error_id = self.__dobot.get_error_id()
        return generate_return_msg(error_id)

    def SpeedFactor(self, args):
        """SpeedFactor"""
        return self.__single_int_command(args, 0, 100, self.__dobot.set_speed_factor)

    def Tool(self, args):
        """Tool"""
        return self.__single_int_command(args, 0, 9, self.__dobot.set_tool_index)

    def User(self, args):
        """User"""
        return self.__single_int_command(args, 0, 9, self.__dobot.set_user_index)

    def AccJ(self, args):
        """AccJ"""
        return self.__single_int_command(args, 1, 100, self.__dobot.set_acc_j_rate)

    def AccL(self, args):
        """AccL"""
        return self.__single_int_command(args, 1, 100, self.__dobot.set_acc_l_rate)

    def SpeedJ(self, args):
        """SpeedJ"""
        return self.__single_int_command(args, 1, 100, self.__dobot.set_speed_j_rate)

    def SpeedL(self, args):
        """SpeedL"""
        return self.__single_int_command(args, 1, 100, self.__dobot.set_speed_l_rate)
