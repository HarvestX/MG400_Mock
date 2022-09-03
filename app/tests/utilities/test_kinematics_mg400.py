"""Test kinematics mg400."""
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

from unittest import TestCase, main

from numpy.testing import assert_allclose
from src.utilities.kinematics_mg400 import (forward_kinematics,
                                            inverse_kinematics)


class TestKinematics(TestCase):
    """Test Kinematics."""

    def fk_test_good(self):
        """forward kinematics test."""
        angles_list = [
            [0, 0, 0, 0, 0, 0],
            [160, 0, 0, 0, 0, 0],
            [-160, 0, 0, 0, 0, 0],
            [0, -25, 25, 0, 0, 0],
            [0, 35, -25, 0, 0, 0],
            [0, 70, 15, 0, 0, 0],
            [0, 85, 25, 0, 0, 0],
            [0, 85, 105, 0, 0, 0],
            [0, 45, 105, 0, 0, 0],
            [0, -25, 50, 0, 0, 0],
        ]
        exp_ret_list = [
            [0, 0, 0, 0, 0, 0],
            [160, 0, 0, 0, 0, 0],
            [-160, 0, 0, 0, 0, 0],
            [0, -25, 25, 0, 0, 0],
            [0, 35, -25, 0, 0, 0],
            [0, 70, 15, 0, 0, 0],
            [0, 85, 25, 0, 0, 0],
            [0, 85, 105, 0, 0, 0],
            [0, 45, 105, 0, 0, 0],
            [0, -25, 50, 0, 0, 0],
        ]
        for angles, exp_ret in zip(angles_list, exp_ret_list):
            solved_flag, ret = forward_kinematics(angles)
            print(ret)
            self.assertTrue(solved_flag)
            self.assertIsNone(assert_allclose(
                ret, exp_ret,  rtol=1e-5, atol=0))

    def ik_test_good(self):
        """inverse kinematics test."""
        tool_vec_list = [
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
        ]
        exp_ret_list = [
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
        ]
        for tool_vec, exp_ret in zip(tool_vec_list, exp_ret_list):
            solved_flag, ret = inverse_kinematics(tool_vec)
            self.assertTrue(solved_flag)
            self.assertIsNone(assert_allclose(
                ret, exp_ret,  rtol=1e-5, atol=0))

    def fk_test_out_of_range(self):
        """forward kinematics test."""
        angles_list = [
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
        ]
        for angles in angles_list:
            solved_flag, _ = forward_kinematics(angles)
            self.assertFalse(solved_flag)

    def ik_test_out_of_range(self):
        """inverse kinematics test."""
        tool_vec_list = [
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
            [0]*6,
        ]
        for tool_vec in tool_vec_list:
            solved_flag, _ = inverse_kinematics(tool_vec)
            self.assertFalse(solved_flag)


if __name__ == '__main__':
    main()
