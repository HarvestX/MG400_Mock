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

    def test_fk_good(self):
        """forward kinematics test."""
        angles_list = [
            [0., 0., 0., 0., 0., 0],
            [160., 0., 0., 0., 0., 0],
            [-160., 0., 0., 0., 0., 0],
            [0., -25., 25., 0., 0., 0],
            [0., 35., -25., 0., 0., 0],
            [0., 70., 15., 0., 0., 0],
            [0., 85., 25., 0., 0., 0],
            [0., 85., 105., 0., 0., 0],
            [0., 45., 105., 0., 0., 0],
            [0., -25., 35., 0., 0., 0],
        ]
        exp_ret_list = [
            [284.0, 0.0, 118.0, 0.0, 0.0, 0.0],
            [-266.872704, 97.133721, 118.0, 0.0, 0.0, 0.0],
            [-266.872704, -97.133721, 118.0, 0.0, 0.0, 0.0],
            [193.645667, 0.0, 27.645667, 0.0, 0.0, 0.0],
            [367.979739, 0.0, 160.309804, 0.0, 0.0, 0.0],
            [442.483228, 0.0, -42.439808, 0.0, 0.0, 0.0],
            [441.937935, 0.0, -115.705941, 0.0, 0.0, 0.0],
            [238.040739, 0.0, -210.784765, 0.0, 0.0, 0.0],
            [187.450354, 0.0, -102.293333, 0.0, 0.0, 0.0],
            [178.393412, 0.0, 1.227986, 0.0, 0.0, 0.0],
        ]
        for angles, exp_ret in zip(angles_list, exp_ret_list):
            solved_flag, ret = forward_kinematics(angles)
            self.assertTrue(solved_flag)
            self.assertIsNone(assert_allclose(
                ret, exp_ret, atol=1e-5))

    def test_ik_good(self):
        """inverse kinematics test."""
        tool_vec_list = [
            [284., 0., 118., 0., 0., 0.],
            [-266.872704, 97.133721, 118., 0., 0., 0.],
            [-266.872704, -97.133721, 118., 0., 0., 0.],
            [193.645667, 0., 27.645667, 0., 0., 0.],
            [367.979739, 0., 160.309804, 0., 0., 0.],
            [442.483228, 0., -42.439808, 0., 0., 0.],
            [441.937935, 0., -115.705941, 0., 0., 0.],
            [238.040739, 0., -210.784765, 0., 0., 0.],
            [187.450354, 0., -102.293333, 0., 0., 0.],
            [178.393412, 0., 1.227986, 0., 0., 0.],
        ]
        exp_ret_list = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0],
            [160.0, 0.0, 0.0, 0.0, 0.0, 0],
            [-160.0, 0.0, 0.0, 0.0, 0.0, 0],
            [0.0, -25.0, 25.0, 0.0, 0.0, 0],
            [0.0, 35.0, -25.0, 0.0, 0.0, 0],
            [0.0, 70.0, 15.0, 0.0, 0.0, 0],
            [0.0, 85.0, 25.0, 0.0, 0.0, 0],
            [0.0, 85.0, 105.0, 0.0, 0.0, 0],
            [0.0, 45.0, 105.0, 0.0, 0.0, 0],
            [0.0, -25.0, 35.0, 0.0, 0.0, 0],
        ]
        for tool_vec, exp_ret in zip(tool_vec_list, exp_ret_list):
            solved_flag, ret = inverse_kinematics(tool_vec)
            self.assertTrue(solved_flag)
            self.assertIsNone(assert_allclose(
                ret, exp_ret, atol=1e-5))

    # def test_fk_out_of_range(self):
    #     """forward kinematics test."""
    #     angles_list = [
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #     ]
    #     for angles in angles_list:
    #         solved_flag, _ = forward_kinematics(angles)
    #         self.assertFalse(solved_flag)

    # def test_ik_out_of_range(self):
    #     """inverse kinematics test."""
    #     tool_vec_list = [
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #         [0]*6,
    #     ]
    #     for tool_vec in tool_vec_list:
    #         solved_flag, _ = inverse_kinematics(tool_vec)
    #         self.assertFalse(solved_flag)


if __name__ == '__main__':
    main()
