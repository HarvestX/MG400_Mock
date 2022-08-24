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

import random
from unittest import TestCase, main

from numpy.testing import assert_allclose
from src.utilities import kinematics_mg400
from src.utilities.kinematics_mg400 import (forward_kinematics,
                                            in_working_space,
                                            inverse_kinematics)


class TestFunctionParser(TestCase):
    """Test Function parser."""

    def test_good(self):
        """Handle acceptable value."""
        for _ in range(0, 500):
            j1_max = kinematics_mg400.J1_MAX
            j1_min = kinematics_mg400.J1_MIN
            j2_max = kinematics_mg400.J2_MAX
            j2_min = kinematics_mg400.J2_MIN
            j3_max = kinematics_mg400.J3_MAX
            j3_min = kinematics_mg400.J3_MIN
            in_space = False
            while not in_space:
                j_1 = round(random.uniform(j1_min, j1_max), 3)
                j_2 = round(random.uniform(j2_min, j2_max), 3)
                j_3 = round(random.uniform(j3_min, j3_max), 3)
                j_4 = round(random.uniform(-180, 180), 3)
                angles = [j_1, j_2, j_3, j_4, 0, 0]
                in_space = in_working_space(angles)

            solved_fk, ret_tool_vec = forward_kinematics(angles)
            self.assertTrue(solved_fk)
            solved_ik, ret_angles = inverse_kinematics(ret_tool_vec)
            self.assertTrue(solved_ik)
            solved_fk_2, ret_tool_vec_2 = forward_kinematics(ret_angles)
            self.assertTrue(solved_fk_2)

            self.assertIsNone(assert_allclose(
                angles, ret_angles,  rtol=1e-5, atol=0))
            self.assertIsNone(assert_allclose(
                ret_tool_vec, ret_tool_vec_2,  rtol=1e-5, atol=0))


if __name__ == '__main__':
    main()
