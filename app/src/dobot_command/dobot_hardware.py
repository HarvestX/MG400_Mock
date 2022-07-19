"""Dobot Hardware."""
import threading


class DobotHardware:
    def __init__(self) -> None:
        self.__lock = threading.Lock()
        self.__joint_angle = [0] * 3

    def set_joint_angle(self, angle, joint_index) -> None:
        self.__lock.acquire()
        self.__joint_angle[joint_index] = angle
        self.__lock.release()

    def get_joint_angle(self, joint_index) -> float:
        return self.__joint_angle[joint_index]
