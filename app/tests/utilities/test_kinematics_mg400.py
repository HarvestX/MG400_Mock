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
from src.utilities.kinematics_mg400 import (ROUND_DECIMALS, forward_kinematics,
                                            inverse_kinematics)


class TestKinematics(TestCase):
    """Test Kinematics."""

    def setUp(self) -> None:
        self.good_angles = [
            [0., 0., 0., 0., 0., 0],
            [160., 0., 0., 0., 0., 0],
            [-160., 0., 0., 0., 0., 0],
            [0., -25., -25., 0., 0., 0],
            [0., 35., -25., 0., 0., 0],
            [0., 70., 15., 0., 0., 0],
            [0., 85., 25., 0., 0., 0],
            [0., 85., 105., 0., 0., 0],
            [0., 45., 105., 0., 0., 0],
            [0., -25., 35., 0., 0., 0],
            [0., 0., 0, 90., 0., 0],
            [0., 0., 0, -90., 0., 0],
        ]
        self.good_tool_vec = [
            [284.0, 0.0, 118.0, 0.0, 0.0, 0.0],
            [-266.872704, 97.133721, 118.0, 0.0, 0.0, 0.0],
            [-266.872704, -97.133721, 118.0, 0.0, 0.0, 0.0],
            [193.645667, 0., 175.562059, 0., 0., 0.],
            [367.979739, 0.0, 160.309804, 0.0, 0.0, 0.0],
            [442.483228, 0.0, -42.439808, 0.0, 0.0, 0.0],
            [441.937935, 0.0, -115.705941, 0.0, 0.0, 0.0],
            [238.040739, 0.0, -210.784765, 0.0, 0.0, 0.0],
            [187.450354, 0.0, -102.293333, 0.0, 0.0, 0.0],
            [178.393412, 0.0, 1.227986, 0.0, 0.0, 0.0],
            [284.0, 0.0, 118.0, 0.0, 0.0, 90.0],
            [284.0, 0.0, 118.0, 0.0, 0.0, -90.0],
        ]
        return super().setUp()

    def test_fk_good(self):
        """forward kinematics test."""
        for test_input, exp_ret in zip(self.good_angles, self.good_tool_vec):
            ret = forward_kinematics(test_input)
            self.assertIsNone(assert_allclose(
                ret, exp_ret, atol=10**-(ROUND_DECIMALS-1)))

    def test_ik_good(self):
        """inverse kinematics test."""
        for test_input, exp_ret in zip(self.good_tool_vec, self.good_angles):
            ret = inverse_kinematics(test_input)
            self.assertIsNone(assert_allclose(
                ret, exp_ret, atol=10**-(ROUND_DECIMALS-1)))

    def test_fk_out_of_range(self):
        """forward kinematics test."""
        angles_list = [
            [180., 0., 0., 0., 0., 0],
            [-180., 0., 0., 0., 0., 0],
            [0., -45., 25., 0., 0., 0],
            [0., 35., -45., 0., 0., 0],
            [0., 90., 15., 0., 0., 0],
            [0., 85., 5., 0., 0., 0],
            [0., 105., 105., 0., 0., 0],
            [0., 25., 105., 0., 0., 0],
            [0., -25., 55., 0., 0., 0],
        ]
        for angles in angles_list:
            with self.assertRaises(ValueError):
                _ = forward_kinematics(angles)

    def test_ik_out_of_range(self):
        """inverse kinematics test."""
        tool_vec_list = [
            [-266.872704, 90., 118.0, 0.0, 0.0, 0.0],
            [-266.872704, -90., 118.0, 0.0, 0.0, 0.0],
            [193.645667, 0., 180., 0., 0., 0.],
            [367.979739, 0.0, 170., 0.0, 0.0, 0.0],
            [450., 0.0, -42.439808, 0.0, 0.0, 0.0],
            [450., 0.0, -115.705941, 0.0, 0.0, 0.0],
            [230., 0.0, -210.784765, 0.0, 0.0, 0.0],
            [180., 0.0, -102.293333, 0.0, 0.0, 0.0],
            [170., 0.0, 1.227986, 0.0, 0.0, 0.0],
        ]
        for tool_vec in tool_vec_list:
            with self.assertRaises(ValueError):
                _ = forward_kinematics(tool_vec)

    def test_fk_args_errors(self):
        """forward kinematics test."""
        angles = [0.]*5
        with self.assertRaises(ValueError):
            _, _ = forward_kinematics(angles)

        angles = "1234"
        with self.assertRaises(ValueError):
            _, _ = forward_kinematics(angles)

        angles = "123456"
        with self.assertRaises(TypeError):
            _, _ = forward_kinematics(angles)

    def test_ik_args_errors(self):
        """inverse kinematics test."""
        tool_vec = [0.]*5
        with self.assertRaises(ValueError):
            _, _ = inverse_kinematics(tool_vec)

        tool_vec = "1234"
        with self.assertRaises(ValueError):
            _, _ = forward_kinematics(tool_vec)

        tool_vec = "123456"
        with self.assertRaises(TypeError):
            _, _ = forward_kinematics(tool_vec)


if __name__ == '__main__':
    main()
