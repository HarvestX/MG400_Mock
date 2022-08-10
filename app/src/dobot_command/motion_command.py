"""Dobot Motion Commands."""

from dobot_command.dobot_hardware import (ControllerMode, DobotHardware,
                                          RobotMode)


class MotionCommands:
    """MotionCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def MovJ(self, args):
        """MovJ"""
        # TODO: to be acceptable optional args.
        if len(args) < 6:
            return False
        X, Y, Z, Rx, Ry, Rz = map(float, args[0:6])
        solved, angles = self.__dobot.inverse_kinematics(
            X, Y, Z, Rx, Ry, Rz)
        if solved:
            self.__dobot.set_q_target(angles)
            self.__dobot.set_qd_target([10]*6)
            self.__dobot.set_robot_mode(RobotMode().mode_running)
            self.__dobot.set_controller_mode(ControllerMode().joint_based)
        return True

    def MoveJog(self, args):
        """MoveJog"""
        # TODO: to be acceptable optional args.
        if len(args) < 1:
            return False
        axis_id = args[0]
        angle_step = 1
        pos_step = 1

        options_joint = ["j1+", "j1-", "j2+", "j2-", "j3+",
                         "j3-", "j4+", "j4-", "j5+", "j5-", "j6+", "j6-"]
        if axis_id in options_joint:
            angles = self.__dobot.get_q_actual()
            index = sum(divmod(options_joint.index(axis_id)+1, 2))-1
            if axis_id[-1] == "+":
                angles[index] += angle_step
            else:
                angles[index] -= angle_step
            self.__dobot.set_robot_mode(RobotMode().mode_jog)
            self.__dobot.set_q_target(angles)
            self.__dobot.set_controller_mode(ControllerMode().joint_based)
            return True

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

            self.__dobot.set_robot_mode(RobotMode().mode_jog)
            self.__dobot.set_tool_vector_target(tool_vec)
            self.__dobot.set_controller_mode(ControllerMode().tool_based)
            return True

        return False
