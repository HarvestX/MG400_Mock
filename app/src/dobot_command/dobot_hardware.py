"""Dobot Hardware."""

import copy
import math
import threading
from typing import List

import dobot_command.robot_mode as robot_mode
import numpy as np
from numpy import linalg as LA
from tcp_interface.realtime_packet import RealtimePacket
from utilities.kinematics_mg400 import in_working_space, rot_y, rot_z


class DobotHardware:
    """DobotHardware"""

    def __init__(self) -> None:
        self.__error_id = 0
        self.__q_previous = np.array([0] * 6)
        self.__status = RealtimePacket()
        self.__lock = threading.Lock()

        self.__link1 = np.array([43, 0, 0])
        self.__link2 = np.array([0, 0, 175])
        self.__link3 = np.array([175, 0, 0])
        self.__link4 = np.array([66, 0, -57])

        self.__digital_inputs = 0
        self.__digital_outputs = 0
        self.__robot_mode = robot_mode.MODE_ENABLE
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
        solved, tool_vec = self.forward_kinematics(self.__q_actual)
        if solved:
            self.__tool_vector_actual: np.ndarray = tool_vec
        else:
            raise ValueError("initial joint angles are invalid!")
        self.__TCP_speed_actual: np.ndarray = np.array([0] * 6)
        self.__TCP_force: np.ndarray = np.array([0] * 6)
        self.__tool_vector_target: np.ndarray = np.array([0] * 6)
        self.__TCP_speed_target: np.ndarray = np.array([0] * 6)
        self.__load = 0
        self.__center_x = 0
        self.__center_y = 0
        self.__center_z = 0

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
            return copy.deepcopy(self.__error_id)

    def get_collision_status(self):
        """get_collision_status"""
        # TODO:implementing an algorithm for detecting collisions
        with self.__lock:
            return [None] * 6

    def get_robot_mode(self):
        """get_robot_mode"""
        with self.__lock:
            return copy.deepcopy(self.__robot_mode)

    def get_q_actual(self):
        """get_q_actual"""
        with self.__lock:
            return copy.deepcopy(self.__q_actual)

    def get_tool_vector_actual(self):
        """get_tool_vector_actual"""
        with self.__lock:
            return copy.deepcopy(self.__tool_vector_actual)

    def get_status(self):
        """get_status"""
        with self.__lock:
            self.__pack_status()
            return self.__status.packet()

    def forward_kinematics(self, angles):
        """forward_kinematics"""

        if not in_working_space(angles):
            return False, np.array([0.]*6)
        j_1, j_2, j_3, j_4, _, _ = angles
        pos = self.__link1 + \
            rot_y(self.__link2, j_2) + \
            rot_y(self.__link3, j_3) + self.__link4

        p_x, p_y, p_z = rot_z(pos, j_1)
        Rz = j_1 + j_4
        return True, np.array([p_x, p_y, p_z, 0, 0, Rz])

    def inverse_kinematics(self, tool_vec):
        """inverse_kinematics"""
        p_x, p_y, p_z, _, _, Rz = tool_vec
        pp_x = LA.norm([p_x, p_y]) - self.__link4[0] - self.__link1[0]
        pp_z = p_z - self.__link4[2] - self.__link1[2]
        length2 = LA.norm(self.__link2)
        length3 = LA.norm(self.__link3)

        j1_ik = math.atan2(p_y, p_x)

        val1 = (pp_x**2+pp_z**2-length2**2-length3**2) / (2*length2*length3)
        if val1 < -1 or val1 > 1:
            return False, np.array([0.]*6)
        j3_1_ik = math.asin(val1)

        j2_ik = math.atan2(pp_z, pp_x) -\
            math.atan2(length2+length3 * math.sin(j3_1_ik),
                       length3*math.cos(j3_1_ik))

        j1_ik = np.rad2deg(j1_ik)
        j2_ik = -np.rad2deg(j2_ik)
        j3_1_ik = -np.rad2deg(j3_1_ik)
        j3_ik = j2_ik + j3_1_ik
        j4_ik = np.rad2deg(Rz) - j1_ik

        if not in_working_space([j1_ik, j2_ik, j3_ik, j4_ik, 0., 0.]):
            return False, np.array([0.]*6)
        return True, np.array([j1_ik, j2_ik, j3_ik, j4_ik, 0., 0.])

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

    def __q_controller(self, timestep):
        # TODO: implement a controller with non-zero accelerations
        if self.__robot_mode in \
                [robot_mode.MODE_RUNNING, robot_mode.MODE_JOG]:
            working = np.abs(self.__q_target -
                             self.__q_actual) < self.__qd_target*timestep
            if np.all(working):
                self.__robot_mode = robot_mode.MODE_ENABLE
            else:
                self.__q_actual = timestep * self.__qd_target * \
                    np.sign(self.__q_target-self.__q_actual) + \
                    self.__q_actual

    def __update_qd(self, timestep: float):
        self.__qd_actual = (self.__q_actual - self.__q_previous) / timestep

    def update_status(self, timestep: float):
        """update_status"""
        with self.__lock:
            self.__q_controller(timestep)
            self.__update_qd(timestep)
            solved, tool_vec = self.forward_kinematics(self.__q_actual)
            if solved:
                self.__tool_vector_actual = tool_vec
            self.__q_previous = self.__q_actual
            self.__pack_status()
            return self.__status.packet()

    def clear_error(self):
        """clear_error"""
        with self.__lock:
            self.__error_id = 0
