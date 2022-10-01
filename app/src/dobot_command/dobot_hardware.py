"""Dobot Hardware."""
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

import copy
import logging
import threading
from queue import Queue
from typing import List

import numpy as np
from dobot_command import robot_mode
from dobot_command.utils_for_dobot import gene_trapezoid_traj
from tcp_interface.realtime_packet import RealtimePacket
from utilities.kinematics_mg400 import forward_kinematics, inverse_kinematics


class DobotHardware:
    """DobotHardware"""

    def __init__(self) -> None:
        self.__status = RealtimePacket()
        self.__lock = threading.Lock()
        self.__motion_que: Queue = Queue()  # for motion command stack
        self.__logger = logging.getLogger("Dobot Hardware")
        self.__log_info_msg("initiate dobot hardware.")

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
        try:
            tool_vec = forward_kinematics(self.__q_actual)
            self.__tool_vector_actual: np.ndarray = tool_vec
        except ValueError:
            self. __log_info_msg("the init angle is outside of the workspace.")
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
        self.__acc_l_rate = 50  # 1-100
        self.__joint_jog_base_step = 5  # [deg]
        self.__tool_jog_base_step = 5  # [deg]
        # end (adjust value)
        self.__update_speed_acc_params()

        # args for motion command
        self.__user_index = 0
        self.__tool_index = 0
        self.__coord_type = 1
        self.__q_init = np.array([0] * 6)
        self.__tool_vector_init = np.array([0] * 6)
        self.__q_previous = self.__q_actual
        self.__tool_vector_previous = self.__tool_vector_actual
        self.__qd_init = np.array([0]*6)
        self.__TCP_speed_init = np.array([0]*6)
        self.__q_target_set: List[np.ndarray] = []
        self.__tool_vector_target_set: List[np.ndarray] = []
        self.__time_index = 0
        self.__timestep = 5.0 / 1000
        self.__feedback_time = 8.0 / 1000

    def normalize_vec(self, vec):
        """normalize_vec"""
        return vec / np.linalg.norm(vec)

    def motion_stack(self, command: str):
        """motion_stack"""
        self.__motion_que.put(command)

    def motion_unstack(self):
        """motion_unstack"""
        if self.__robot_mode in [robot_mode.MODE_RUNNING, robot_mode.MODE_JOG]:
            return True, None
        if self.__motion_que.empty():
            return True, None
        return False, self.__motion_que.get(block=False)

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
            return np.int64(copy.deepcopy(self.__error_id))

    def get_collision_status(self):
        """get_collision_status"""
        # TODO:implementing an algorithm for detecting collisions
        with self.__lock:
            return [None] * 6

    def get_timestep(self):
        """get_timestep"""
        with self.__lock:
            return copy.deepcopy(self.__timestep)

    def get_feedback_time(self):
        """get_feedback_time"""
        with self.__lock:
            return copy.deepcopy(self.__feedback_time)

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

    def __register_init_status(self):
        """register_init_status"""
        self.__q_init = self.__q_actual
        self.__tool_vector_init = self.__tool_vector_actual
        self.__qd_init = self.__qd_actual
        self.__TCP_speed_init = self.__TCP_speed_actual

    def __update_speed_acc_params(self):
        self.__acc_j = self.__acc_j_rate * self.__acc_j_max * 0.01
        self.__acc_l = self.__acc_l_rate * self.__acc_l_max * 0.01
        self.__speed_j = self.__global_speed_rate * \
            self.__speed_j_max * self.__speed_j_rate * 0.01**2
        self.__speed_l = self.__global_speed_rate * \
            self.__speed_l_max * self.__speed_l_rate * 0.01**2

    def set_error_id(self, error_id: int):
        """set_error_id"""
        with self.__lock:
            self.__error_id = error_id

    def set_robot_mode(self, mode: int):
        """set_robot_mode"""
        with self.__lock:
            self.__robot_mode = mode

    def set_q_target(self, q_target: List[float]):
        """set_q_target"""
        with self.__lock:
            try:
                tool_vex = forward_kinematics(np.array(q_target))
                self.__tool_vector_target = tool_vex
                self.__q_target = np.array(q_target)
                return True
            except ValueError as err:
                self.__logger.error(err)
                return False

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
            try:
                angles = inverse_kinematics(np.array(tool_vector_target))
                self.__tool_vector_target = np.array(tool_vector_target)
                self.__q_target = angles
                return True
            except ValueError as err:
                self.__logger.error(err)
                return False

    def set_TCP_speed_target(self, TCP_speed_target: List[float]):
        """set_TCP_speed_target"""
        with self.__lock:
            self.__TCP_speed_target = np.array(TCP_speed_target)

    def set_speed_factor(self, global_speed_rate: int):
        """set_speed_factor"""
        with self.__lock:
            self.__global_speed_rate = global_speed_rate
            self.__update_speed_acc_params()

    def set_speed_j_rate(self, speed_j: int):
        """set_speed_j"""
        with self.__lock:
            self.__speed_j_rate = speed_j
            self.__update_speed_acc_params()

    def set_speed_l_rate(self, speed_l: int):
        """set_speed_l"""
        with self.__lock:
            self.__speed_l_rate = speed_l
            self.__update_speed_acc_params()

    def set_acc_j_rate(self, acc_j: int):
        """set_acc_j"""
        with self.__lock:
            self.__acc_j_rate = acc_j
            self.__update_speed_acc_params()

    def set_acc_l_rate(self, acc_l: int):
        """set_acc_l"""
        with self.__lock:
            self.__acc_l_rate = acc_l
            self.__update_speed_acc_params()

    def set_user_index(self, user: int):
        """set_user_index"""
        with self.__lock:
            self.__user_index = user

    def set_tool_index(self, tool: int):
        """set_tool_index"""
        with self.__lock:
            self.__tool_index = tool

    def set_coord_type(self, coord_type: int):
        """set_tool_index"""
        with self.__lock:
            self.__coord_type = coord_type

    def log_info_msg(self, text):
        """log_info_msg"""
        with self.__lock:
            self.__log_info_msg(text)

    def __log_info_msg(self, text):
        self.__logger.info(text)

    def log_debug_msg(self, text):
        """log_debug_msg"""
        with self.__lock:
            self.__log_debug_msg(text)

    def __log_debug_msg(self, text):
        self.__logger.debug(text)

    def log_warning_msg(self, text):
        """log_warning_msg"""
        with self.__lock:
            self.__log_warning_msg(text)

    def __log_warning_msg(self, text):
        self.__logger.warning(text)

    def generate_target_in_joint(self):
        """generate_joint_target"""
        with self.__lock:
            self.__register_init_status()
            q_trajs = []
            len_max = 0
            for q_init, q_target, qd_s in \
                    zip(self.__q_init, self.__q_target, self.__qd_init):
                traj = gene_trapezoid_traj(
                    q_init, q_target, self.__acc_j,
                    self.__speed_j, qd_s, self.__timestep)
                np.append(traj, q_target)
                len_max = max(len_max, len(traj))
                q_trajs.append(traj)

            q_trajs = \
                [np.concatenate([q_traj, [q_traj[-1]]*(len_max-len(q_traj))], 0)
                 if len(q_traj) < len_max else q_traj for q_traj in q_trajs]
            self.__q_target_set = np.array(q_trajs).T

            self.__tool_vector_target_set = []
            for q_target in self.__q_target_set:
                tool_vec = forward_kinematics(q_target)
                self.__tool_vector_target_set.append(tool_vec)
            return True

    def generate_target_in_tool(self):
        """generate_target_in_tool"""
        with self.__lock:
            self.__register_init_status()

            dist = np.linalg.norm(
                self.__tool_vector_target[0:3] - self.__tool_vector_init[0:3])
            v_s = np.linalg.norm(self.__TCP_speed_init[0:3])
            vec_length = gene_trapezoid_traj(
                0, dist, self.__acc_l, self.__speed_l, v_s, self.__timestep)

            direction = self.normalize_vec(
                self.__tool_vector_target[0:3] - self.__tool_vector_init[0:3])
            pos_list = np.array(
                [length * direction + self.__tool_vector_init[0:3]
                 for length in vec_length])
            np.append(pos_list, self.__tool_vector_target[0:3])

            r_z_traj = gene_trapezoid_traj(
                self.__tool_vector_init[-1], self.__tool_vector_target[-1],
                self.__acc_j, self.__speed_j, self.__TCP_speed_init[-1],
                self.__timestep)

            if len(r_z_traj) < len(pos_list):
                r_z_traj = np.concatenate(
                    [r_z_traj, [r_z_traj[-1]]*(len(pos_list)-len(r_z_traj))], 0)
            elif len(r_z_traj) > len(pos_list):
                pos_list = np.concatenate(
                    [pos_list, [pos_list[-1]]*(len(r_z_traj)-len(pos_list))], 0)

            self.__tool_vector_target_set = []
            self.__q_target_set = []
            for pos, r_z in zip(pos_list, r_z_traj):
                pos = np.concatenate([pos, [0, 0, r_z]], 0)
                try:
                    angles = inverse_kinematics(pos)
                    self.__tool_vector_target_set.append(pos)
                    self.__q_target_set.append(angles)
                except ValueError:
                    return False
            return True

    def generate_jog_target(self, axis_id):
        """ generate_jog_target"""
        with self.__lock:
            self.__register_init_status()

            tool_step = \
                self.__tool_jog_base_step * self.__global_speed_rate * 0.01
            angle_step = \
                self.__joint_jog_base_step * self.__global_speed_rate * 0.01

            options_joint = ["j1+", "j1-", "j2+", "j2-", "j3+",
                             "j3-", "j4+", "j4-", "j5+", "j5-", "j6+", "j6-"]
            if axis_id in options_joint:
                angles = self.__q_actual
                index = sum(divmod(options_joint.index(axis_id)+1, 2))-1
                if axis_id[-1] == "+":
                    angles[index] += angle_step
                else:
                    angles[index] -= angle_step
                try:
                    tool_vec = forward_kinematics(angles)
                except ValueError:
                    return False

            options_tool = ["x+", "x-", "y+", "y-", "z+",
                            "z-", "rx+", "rx-", "ry+", "ry-", "rz+", "rz-"]
            if axis_id in options_tool:
                tool_vec = self.__tool_vector_actual
                index = sum(divmod(options_tool.index(axis_id)+1, 2))-1
                step = tool_step if index in [0, 1, 2] else angle_step
                if axis_id[-1] == "+":
                    tool_vec[index] += step
                else:
                    tool_vec[index] -= step
                try:
                    angles = inverse_kinematics(tool_vec)
                except ValueError:
                    return False

            try:
                self.__tool_vector_target = tool_vec
                self.__q_target = angles
                return True
            except NameError:
                return False

    def __q_controller(self):
        if self.__robot_mode is robot_mode.MODE_RUNNING:
            self.__q_actual = self.__q_target_set[self.__time_index]
            self.__time_index += 1
            if self.__time_index >= len(self.__q_target_set):
                self.__robot_mode = robot_mode.MODE_ENABLE
                self.__time_index = 0
                self.__log_info_msg(
                    "The robot has reached the target position.")

        if self.__robot_mode is robot_mode.MODE_JOG:
            self.__q_actual = self.__q_target
            self.__robot_mode = robot_mode.MODE_ENABLE
            self.__log_info_msg("The Jog task is finished.")

    def __update_actual_status(self):
        try:
            tool_vec = forward_kinematics(self.__q_actual)
            self.__tool_vector_actual = tool_vec
        except ValueError:
            self.__log_info_msg("the actual angle is outside of workspace.")

        self.__qd_actual = (
            self.__q_actual - self.__q_previous) / self.__timestep
        self.__TCP_speed_actual = (
            self.__tool_vector_actual - self.__tool_vector_previous) / self.__timestep

        self.__q_previous = self.__q_actual
        self.__tool_vector_previous = self.__tool_vector_actual

    def update_status(self):
        """update_status"""
        with self.__lock:
            self.__q_controller()
            self.__update_actual_status()

    def clear_error(self):
        """clear_error"""
        with self.__lock:
            self.__error_id = 0
