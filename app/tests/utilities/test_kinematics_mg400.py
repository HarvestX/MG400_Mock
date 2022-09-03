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


class TestFunctionParser(TestCase):
    """Test Function parser."""

    def fk_test_good(self):
        """Handle acceptable value."""
        angles_1 = [0]*6
        exp_ret_1 = [0]*6
        solved_flag, ret_1 = forward_kinematics(angles_1)
        self.assertTrue(solved_flag)
        self.assertIsNone(assert_allclose(
            ret_1, exp_ret_1,  rtol=1e-5, atol=0))

    def ik_test_good(self):
        """Handle acceptable value."""
        tool_vec_1 = [0]*6
        exp_ret_1 = [0]*6
        solved_flag, ret_1 = inverse_kinematics(tool_vec_1)
        self.assertTrue(solved_flag)
        self.assertIsNone(assert_allclose(
            ret_1, exp_ret_1,  rtol=1e-5, atol=0))


if __name__ == '__main__':
    main()
