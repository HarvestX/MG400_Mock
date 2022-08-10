"""Dobot Motion Commands."""

from typing import List

from dobot_command.dobot_hardware import DobotHardware


class MotionCommands:
    """MotionCommands"""

    def __init__(self, dobot: DobotHardware) -> None:
        self.__dobot = dobot

    def MovJ(self, args):
        """MovJ"""
        if len(args) < 6:
            return False
        X, Y, Z, Rx, Ry, Rz = map(float, args[0:6])
        solved, j_1, j_2, j_3, j_4 = self.__dobot.inverse_kinematics(
            X, Y, Z, Rx, Ry, Rz)
        print(f"solved:{solved}")
        print(f"j1:{j_1}")
        print(f"j2:{j_2}")
        print(f"j3:{j_3}")
        print(f"j4:{j_4}")
        if solved:
            angles = [j_1, j_2, j_3, j_4, 0, 0]
            self.__dobot.set_q_target(angles)

    def MoveJog(self, axis_id: str, *args):
        """MoveJog"""
        _ = args  # for pylint waring
        # TODO: update the following algorithm
        # temporary implementation:
        # The following algorithm differs from that of the actual Dobot.
        axis_id = axis_id[0]
        angles: List[float] = [0.0] * 6
        if axis_id == "j1+":
            angles[0] = 90
        elif axis_id == "j1-":
            angles[0] = -90
        elif axis_id == "j2+":
            angles[1] = -90
        elif axis_id == "j2-":
            angles[1] = -90
        elif axis_id == "j3+":
            angles[2] = -90
        elif axis_id == "j3-":
            angles[2] = -90
        elif axis_id == "j4+":
            angles[3] = -90
        elif axis_id == "j4-":
            angles[3] = -90
        elif axis_id == "j5+":
            angles[4] = -90
        elif axis_id == "j5-":
            angles[4] = -90
        elif axis_id == "j6+":
            angles[5] = -90
        elif axis_id == "j6-":
            angles[5] = -90
        self.__dobot.set_q_target(angles)
