"""Dobot Hardware."""

import copy
import logging
import threading
from logging import getLogger
from typing import List

import dobot_command.controller_mode as ctrl_mode
import dobot_command.robot_mode as robot_mode
import numpy as np
from tcp_interface.realtime_packet import RealtimePacket
from utilities.kinematics_mg400 import (forward_kinematics, in_working_space,
                                        inverse_kinematics, normalize_vec)


class DobotHardware:
    """DobotHardware"""

    def __init__(self) -> None:
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
        solved, tool_vec = forward_kinematics(self.__q_actual)
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

        self.__error_id = 0

        # TODO(m12watanabe1a): adjust value
        self.__global_speed_rate = 50  # 0-100
        self.__speed_j_max = 360  # [deg/s]
        self.__speed_j_rate = 50  # 1-100
        self.__acc_j_max = 360  # [deg/s^2]
        self.__acc_j_rate = 50  # 1-100
        self.__speed_l_max = 1500  # [mm/s]
        self.__speed_l_rate = 50  # 1-100
        self.__acc_l_max = 1500  # [mm/s^2]
        self.__acc_l_rate = 100  # 1-100
        # end (adjust value)
        self.__update_speed_acc_params()

        self.__ctrl_mode = ctrl_mode.MODE_NONE
        self.__q_init = np.array([0] * 6)
        self.__tool_vector_init = np.array([0] * 6)
        self.__q_previous = self.__q_actual
        self.__tool_vector_previous = self.__tool_vector_actual
        self.__qd_ref = np.array([0]*6)
        self.__speed_l_ref = 0
        self.__status = RealtimePacket()
        self.__lock = threading.Lock()

        logging.basicConfig(filename='test_MovJ.log', level=logging.INFO)
        self.__logger = getLogger("test_MovJ")
        self.__count = 0
        self.__q_target_set: List[np.ndarray] = []
        self.__tool_vector_target_set: List[np.ndarray] = []
        self.__time_index = 0

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

    def set_count(self):
        """set_count"""
        with self.__lock:
            self.__count += 1

    def reset_time_index(self):
        """reset_time_index"""
        with self.__lock:
            self.__time_index = 0

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

    def get_global_speed(self):
        """get_global_speed"""
        with self.__lock:
            return copy.deepcopy(self.__global_speed_rate)

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

    def register_init_status(self):
        """register_init_status"""
        with self.__lock:
            self.__q_init = self.__q_actual
            self.__tool_vector_init = self.__tool_vector_actual
            self.__qd_ref = self.__qd_actual
            self.__speed_l_ref = np.linalg.norm(self.__TCP_speed_actual[0:3])

    def __update_speed_acc_params(self):
        self.__acc_j = self.__acc_j_rate * self.__acc_j_max * 0.01
        self.__acc_l = self.__acc_l_rate * self.__acc_l_max * 0.01
        self.__speed_j = self.__global_speed_rate * \
            self.__speed_j_max * self.__speed_j_rate * 0.01**2
        self.__speed_l = self.__global_speed_rate * \
            self.__speed_l_max * self.__speed_l_rate * 0.01**2

    def set_ctrl_mode(self, mode: int):
        """set_ctrl_mode"""
        with self.__lock:
            self.__ctrl_mode = mode

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

    def set_speed_j(self, speed_j: int):
        """set_speed_j"""
        with self.__lock:
            self.__speed_j_rate = speed_j

    def set_speed_l(self, speed_l: int):
        """set_speed_l"""
        with self.__lock:
            self.__speed_l_rate = speed_l

    def log_msg(self, text):
        """out_of_range"""
        self.__logger.info("%s: %s", self.__count, text)

    def mov_l_time(self):
        """cal_move_time"""
        with self.__lock:
            dist = np.linalg.norm(
                self.__tool_vector_target[0:3] - self.__tool_vector_init[0:3])
            v_max = np.sqrt(self.__acc_l*dist + self.__speed_l_ref**2)

            if v_max > self.__speed_l:
                time_acc = (self.__speed_l-self.__speed_l_ref) / self.__acc_l
                time_const = dist/self.__speed_l - \
                    (self.__speed_l**2 - self.__speed_l_ref**2) / \
                    (self.__acc_l*self.__speed_l)
                time_total = 2*time_acc + time_const
            else:
                time_acc = (v_max-self.__speed_l_ref)/self.__acc_l
                time_const = 0
                time_total = 2*time_acc
            return time_acc, time_const, time_total

    def generate_liner_target(self, time_acc, time_const, timestep):
        """intrpt_2d"""
        with self.__lock:
            direction = normalize_vec(
                self.__tool_vector_target[0:3] - self.__tool_vector_init[0:3])

            time_acc_list = np.linspace(0, time_acc, num=int(
                time_acc/timestep) + 1, endpoint=True)
            length_start = 0.5 * self.__acc_l*(time_acc_list**2)

            time_const_list = np.linspace(0, time_const, num=int(
                time_const/timestep) + 1, endpoint=True)
            length_mid = self.__speed_l*time_const_list + length_start[-1]

            length_end = length_mid[-1] - \
                0.5 * self.__acc_l*(time_acc_list**2-2*time_acc_list*time_acc)

            length_total = np.concatenate(
                [length_start, length_mid, length_end], 0)
            pos = np.array(
                [length * direction + self.__tool_vector_init[0:3]
                 for length in length_total])
            np.append(pos, self.__tool_vector_target[0:3])

            self.__tool_vector_target_set = []
            self.__q_target_set = []
            for pos in pos:
                pos = np.concatenate([pos, [0]*3], 0)
                flag, angles = inverse_kinematics(pos)
                if not flag:
                    print(pos)
                    return False
                else:
                    self.__tool_vector_target_set.append(pos)
                    self.__q_target_set.append(angles)
            return True

    def __q_controller(self, timestep):
        # TODO: implement a controller with non-zero accelerations
        if self.__robot_mode in \
                [robot_mode.MODE_RUNNING, robot_mode.MODE_JOG]:
            error_j = self.__q_target-self.__q_actual

            if self.__ctrl_mode is ctrl_mode.MODE_JOINT:
                acc_sign = 0.5 * np.abs(self.__q_target - self.__q_init) >= \
                    np.abs(self.__q_actual - self.__q_init)
                acc = np.where(acc_sign, -1, 1) * \
                    np.sign(error_j) * self.__acc_j
                self.__qd_ref += acc * timestep
                self.__qd_target = np.sign(error_j) * \
                    np.clip(np.abs(self.__qd_ref), 3, self.__speed_j)

                working = np.abs(error_j) <= np.abs(
                    self.__qd_target) * timestep
                if np.all(working):
                    self.__q_actual = self.__q_target
                    self.__qd_target = np.array([0]*6)
                    self.__TCP_speed_target = np.array([0]*6)
                    self.__robot_mode = robot_mode.MODE_ENABLE
                    self.__ctrl_mode = ctrl_mode.MODE_NONE
                    self.log_msg("finish.")

                updated_q = timestep * self.__qd_target + self.__q_actual
                if in_working_space(updated_q):
                    self.__q_actual = updated_q
                else:
                    self.__robot_mode = robot_mode.MODE_ENABLE
                    self.__ctrl_mode = ctrl_mode.MODE_NONE
                    self.log_msg("out of range.")

            if self.__ctrl_mode is ctrl_mode.MODE_TOOL:
                self.__q_target = self.__q_target_set[self.__time_index]
                self.__tool_vector_target = \
                    self.__tool_vector_target_set[self.__time_index]
                self.__q_actual = self.__q_target
                velo = np.linalg.norm(self.__TCP_speed_actual[0:3])
                self.log_msg(f"index: {self.__time_index}, velo: {velo}")

                self.__time_index += 1
                if self.__time_index >= len(self.__q_target_set):
                    self.__robot_mode = robot_mode.MODE_ENABLE
                    self.__ctrl_mode = ctrl_mode.MODE_NONE
                    self.__time_index = 0
                    self.log_msg("finish.")

    def __update_actual_status(self, timestep: float):
        solved, tool_vec = forward_kinematics(self.__q_actual)
        if solved:
            self.__tool_vector_actual = tool_vec

        self.__qd_actual = (self.__q_actual - self.__q_previous) / timestep
        self.__TCP_speed_actual = (
            self.__tool_vector_actual - self.__tool_vector_previous) / timestep

        self.__q_previous = self.__q_actual
        self.__tool_vector_previous = self.__tool_vector_actual

    def update_status(self, timestep: float):
        """update_status"""
        with self.__lock:
            self.__q_controller(timestep)
            self.__update_actual_status(timestep)
            self.__pack_status()
            return self.__status.packet()

    def clear_error(self):
        """clear_error"""
        with self.__lock:
            self.__error_id = 0
