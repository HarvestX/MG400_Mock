"""Dobot Motion Commands."""

import dobot_command.controller_mode as ctrl_mode
import dobot_command.robot_mode as robot_mode
from dobot_command.dobot_hardware import DobotHardware
from utilities.kinematics_mg400 import forward_kinematics, inverse_kinematics


class MotionCommands:
    """MotionCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def MovJ(self, args):
        """MovJ"""
        # TODO: to be acceptable optional args.
        self.__dobot.set_count()
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            self.__dobot.log_msg("mode is enable.")
            return False
        if len(args) < 6:
            self.__dobot.log_msg("number of args is not validated.")
            return False

        tool_vec = list(map(float, args[0:6]))
        solved, angles = inverse_kinematics(tool_vec)
        if solved:
            self.__dobot.set_robot_mode(robot_mode.MODE_RUNNING)
            self.__dobot.set_ctrl_mode(ctrl_mode.MODE_JOINT)
            self.__dobot.register_init_status()
            self.__dobot.set_tool_vector_target(tool_vec)
            self.__dobot.set_q_target(angles)
            return True

        self.__dobot.log_msg("out of range.")
        return False

    def MoveJog(self, args):
        """MoveJog"""
        # TODO: to be acceptable optional args.
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            return False
        if len(args) < 1:
            return False

        axis_id = args[0]
        global_speed = self.__dobot.get_global_speed()
        angle_step = 5 * global_speed / 100  # [deg]
        pos_step = 10 * global_speed / 100  # [mm]
        solved = False

        options_joint = ["j1+", "j1-", "j2+", "j2-", "j3+",
                         "j3-", "j4+", "j4-", "j5+", "j5-", "j6+", "j6-"]
        if axis_id in options_joint:
            angles = self.__dobot.get_q_actual()
            index = sum(divmod(options_joint.index(axis_id)+1, 2))-1
            if axis_id[-1] == "+":
                angles[index] += angle_step
            else:
                angles[index] -= angle_step
            solved, tool_vec = forward_kinematics(angles)
            self.__dobot.set_ctrl_mode(ctrl_mode.MODE_JOINT)

        options_tool = ["x+", "x-", "y+", "y-", "z+",
                        "z-", "rx+", "rx-", "ry+", "ry-", "rz+", "rz-"]
        if axis_id in options_tool:
            tool_vec = self.__dobot.get_tool_vector_actual()
            index = sum(divmod(options_tool.index(axis_id)+1, 2))-1
            step = pos_step if index in [0, 1, 2] else angle_step
            if axis_id[-1] == "+":
                tool_vec[index] += step
            else:
                tool_vec[index] -= step
            solved, angles = inverse_kinematics(tool_vec)
            self.__dobot.set_ctrl_mode(ctrl_mode.MODE_TOOL)

        if solved:
            self.__dobot.set_robot_mode(robot_mode.MODE_JOG)
            self.__dobot.register_init_status()
            self.__dobot.set_tool_vector_target(tool_vec)
            self.__dobot.set_q_target(angles)
            return True
        return False

    def MovL(self, args):
        """MovL"""
        # TODO: to be acceptable optional args.
        if self.__dobot.get_robot_mode() is not robot_mode.MODE_ENABLE:
            return False
        if len(args) < 6:
            return False
        tool_target = list(map(float, args[0:6]))

        self.__dobot.set_tool_vector_target(tool_target)
        self.__dobot.register_init_status()
        time_acc, time_const, _ = self.__dobot.mov_l_time()
        flag = self.__dobot.generate_liner_target(
            time_acc, time_const, 8.0 / 1000)
        if not flag:
            self.__dobot.log_msg("no liner interpolate.")
            return False
        else:
            self.__dobot.set_robot_mode(robot_mode.MODE_RUNNING)
            self.__dobot.set_ctrl_mode(ctrl_mode.MODE_TOOL)
            self.__dobot.reset_time_index()
            return True

    def JointMovJ(self, args):
        """JointMovJ"""
