"""Dobot Hardware."""

import math
import threading
from typing import List

import numpy as np
from dobot_command.utils_kinematics_mg400 import (J1_MAX, J1_MIN, J2_MAX,
                                                  J2_MIN, J3_1_MAX, J3_1_MIN,
                                                  J3_MAX, J3_MIN, in_check)
from numpy import linalg as LA
from tcp_interface.realtime_packet import RealtimePacket


class DobotHardware:
    """DobotHardware"""

    def __init__(self) -> None:
        self.__digital_inputs = 0
        self.__digital_outputs = 0
        self.__robot_mode = 0
        self.__test_value = 0
        self.__speed_scaling = 1
        self.__q_target: np.ndarray = np.array([0] * 6)
        self.__qd_target: np.ndarray = np.array([0] * 6)
        self.__qdd_target: np.ndarray = np.array([0] * 6)
        self.__i_target: np.ndarray = np.array([0] * 6)
        self.__m_target: np.ndarray = np.array([0] * 6)
        self.__q_actual: np.ndarray = np.array([0] * 6)
        self.__qd_actual: np.ndarray = np.array([0] * 6)
        self.__i_actual: np.ndarray = np.array([0] * 6)
        self.__actual_i_TCP_force: np.ndarray = np.array([0] * 6)
        self.__tool_vector_actual: np.ndarray = np.array([0] * 6)
        self.__TCP_speed_actual: np.ndarray = np.array([0] * 6)
        self.__TCP_force: np.ndarray = np.array([0] * 6)
        self.__tool_vector_target: np.ndarray = np.array([0] * 6)
        self.__TCP_speed_target: np.ndarray = np.array([0] * 6)
        self.__load = 0
        self.__center_x = 0
        self.__center_y = 0
        self.__center_z = 0

        self.__error_id = 0
        self.__q_previous = np.array([0] * 6)
        self.__status = RealtimePacket()
        self.__lock = threading.Lock()

        self.__link1 = np.array([43, 0])
        self.__link2 = np.array([0, 175])
        self.__link3 = np.array([175, 0])
        self.__link4 = np.array([66, -57])

    def __pack_status(self):
        self.__status.write("digital_inputs", self.__digital_inputs)
        self.__status.write("digital_outputs", self.__digital_outputs)
        self.__status.write("robot_mode", self.__robot_mode)
        self.__status.write("test_value", self.__test_value)
        self.__status.write("speed_scaling", self.__speed_scaling)
        self.__status.write("q_target", self.__q_target)
        self.__status.write("qd_target", self.__qd_target)
        self.__status.write("qdd_target", self.__qdd_target)
        self.__status.write("i_target", self.__i_target)
        self.__status.write("m_target", self.__m_target)
        self.__status.write("q_actual", self.__q_actual)
        self.__status.write("qd_actual", self.__qd_actual)
        self.__status.write("i_actual", self.__i_actual)
        self.__status.write("actual_i_TCP_force", self.__actual_i_TCP_force)
        self.__status.write("tool_vector_actual", self.__tool_vector_actual)
        self.__status.write("TCP_speed_actual", self.__TCP_speed_actual)
        self.__status.write("TCP_force", self.__TCP_force)
        self.__status.write("tool_vector_target", self.__tool_vector_target)
        self.__status.write("TCP_speed_target", self.__TCP_speed_target)
        self.__status.write("load", self.__load)
        self.__status.write("center_x", self.__center_x)
        self.__status.write("center_y", self.__center_y)
        self.__status.write("center_z", self.__center_z)

    def get_error_id(self) -> np.int64:
        """get_error_id

        Returns:
            np.int64: 0 indicates that there are no errors.
                Other numbers indicate that the dobot has some errors.
        """
        with self.__lock:
            return self.__error_id

    def get_collision_status(self):
        """get_collision_status"""
        # TODO:implementing an algorithm for detecting collisions
        with self.__lock:
            return [None] * 6

    def get_status(self):
        """get_status"""
        with self.__lock:
            self.__pack_status()
            return self.__status.packet()

    def inverse_kinematics(self, p_x, p_y, p_z, Rx, Ry, Rz):
        """inverse_kinematics"""
        _, _ = Rx, Ry  # for pylint waring

        p_x = p_x - self.__link4[0] - self.__link1[0]
        p_z = p_z - self.__link4[1] - self.__link1[1]
        length2 = LA.norm(self.__link2)
        length3 = LA.norm(self.__link3)

        j1_ik = math.atan2(p_y, p_x)
        j1_ik = np.rad2deg(j1_ik)
        if not in_check(J1_MIN, j1_ik, J1_MAX):
            return False, 0, 0, 0, 0

        val1 = (p_x**2+p_z**2-length2**2-length3**2) / (2*length2*length3)
        if val1 < -1 or val1 > 1:
            return False, 0, 0, 0, 0
        j3_1_ik = math.asin(val1)

        j2_ik = math.atan2(p_z, p_x) -\
            math.atan2(length2+length3 * math.sin(j3_1_ik),
                       length3*math.cos(j3_1_ik))

        j2_ik = -np.rad2deg(j2_ik)
        j3_1_ik = -np.rad2deg(j3_1_ik)
        j3_ik = j2_ik + j3_1_ik

        if not(in_check(J2_MIN, j2_ik, J2_MAX) and
               in_check(J3_1_MIN, j3_1_ik, J3_1_MAX) and
               in_check(J3_MIN, j3_ik, J3_MAX)):
            return False, 0, 0, 0, 0

        j4_ik = Rz - j1_ik
        return True, j1_ik, j2_ik, j3_ik, j4_ik

    def set_robot_mode(self, mode: int):
        """set_robot_mode"""
        with self.__lock:
            self.__robot_mode = mode

    def set_q_target(self, q_target: List[float]):
        """set_q_target"""
        with self.__lock:
            self.__q_target = np.array(q_target)

    def set_qd_target(self, qd_target: List[float]):
        """set_qd_target"""
        with self.__lock:
            self.__qd_target = np.array(qd_target)

    def set_qdd_target(self, qdd_target: List[float]):
        """set_qdd_target"""
        with self.__lock:
            self.__qdd_target = np.array(qdd_target)

    def set_tool_vector_target(self, tool_vector_target: List[float]):
        """set_tool_vector_target"""
        with self.__lock:
            self.__tool_vector_target = np.array(tool_vector_target)

    def set_TCP_speed_target(self, TCP_speed_target: List[float]):
        """set_TCP_speed_target"""
        with self.__lock:
            self.__TCP_speed_target = np.array(TCP_speed_target)

    def __q_controller(self):
        self.__q_actual = self.__q_target

    def __update_qd(self, timestep: float):
        self.__qd_actual = (self.__q_actual - self.__q_previous) / timestep

    def update_status(self, timestep: float):
        """update_status"""
        with self.__lock:
            self.__q_controller()
            self.__update_qd(timestep)
            self.__q_previous = self.__q_actual
            self.__pack_status()
            return self.__status.packet()

    def clear_error(self):
        """clear_error"""
        with self.__lock:
            self.__error_id = 0


class RobotMode:
    """DobotHardware"""

    def __init__(self):
        self.mode_init = 1
        self.mode_brake_open = 2
        self.mode_disabled = 4
        self.mode_enable = 5
        self.mode_backdrive = 6
        self.mode_running = 7
        self.mode_recording = 8
        self.mode_error = 9
        self.mode_pause = 10
        self.mode_jog = 11
