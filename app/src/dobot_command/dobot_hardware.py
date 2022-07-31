"""Dobot Hardware."""

import threading
import numpy as np
from tcp_interface.realtime_packet import RealtimePacket


class DobotHardware:
    """DobotHardware"""

    def __init__(self) -> None:
        self.__digital_inputs = 0
        self.__digital_outputs = 0
        self.__robot_mode = 0
        self.__test_value = 0
        self.__speed_scaling = 1
        self.__q_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__qd_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__qdd_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__i_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__m_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__q_actual: np.ndarray = np.array([0] * 6, np.float64)
        self.__qd_actual: np.ndarray = np.array([0] * 6, np.float64)
        self.__i_actual: np.ndarray = np.array([0] * 6, np.float64)
        self.__actual_i_TCP_force: np.ndarray = np.array([0] * 6, np.float64)
        self.__tool_vector_actual: np.ndarray = np.array([0] * 6, np.float64)
        self.__TCP_speed_actual: np.ndarray = np.array([0] * 6, np.float64)
        self.__TCP_force: np.ndarray = np.array([0] * 6, np.float64)
        self.__tool_vector_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__TCP_speed_target: np.ndarray = np.array([0] * 6, np.float64)
        self.__load = 0
        self.__center_x = 0
        self.__center_y = 0
        self.__center_z = 0

        self.__error_id = 0
        self.__q_previous = np.array([0] * 6, np.float64)
        self.__status = RealtimePacket()
        self.__lock = threading.Lock()

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

    def lock_mutex(self):
        """lock_mutex"""
        self.__lock.acquire()

    def release_mutex(self):
        """release_mutex"""
        self.__lock.release()

    def get_error_id(self) -> np.int64:
        """get_error_id

        Returns:
            np.int64: 0 indicates that there are no errors.
                Other numbers indicate that the dobot has some errors.
        """
        return self.__error_id

    def get_status(self):
        """get_status"""
        self.__pack_status()
        return self.__status.packet()

    def set_q_target(self, q_target: np.ndarray):
        """set_q_target"""
        print(q_target)
        # self.__q_target = q_target.copy()

    def set_qd_target(self, qd_target: np.ndarray):
        """set_qd_target"""
        self.__qd_target = qd_target.copy()

    def set_qdd_target(self, qdd_target: np.ndarray):
        """set_qdd_target"""
        self.__qdd_target = qdd_target.copy()

    def set_tool_vector_target(self, tool_vector_target: np.ndarray):
        """set_tool_vector_target"""
        self.__tool_vector_target = tool_vector_target.copy()

    def set_TCP_speed_target(self, TCP_speed_target: np.ndarray):
        """set_TCP_speed_target"""
        self.__TCP_speed_target = TCP_speed_target.copy()

    def __q_controller(self):
        self.__q_actual = self.__q_target.copy()

    def __update_qd(self, timestep: float):
        self.__qd_actual = (self.__q_actual - self.__q_previous) / timestep

    def update_status(self, timestep: float):
        """update_status"""
        self.__q_controller()
        self.__update_qd(timestep)
        self.__q_previous = self.__q_actual.copy()

    def clear_error(self):
        """clear_error"""
        self.__error_id = 0
