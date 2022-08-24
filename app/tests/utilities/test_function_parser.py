"""Test function parser."""
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

from src.utilities.function_parser import FunctionParser


class MyFuncClass:
    """MyFunctionClass for tests."""

    def ret_true(self, _) -> bool:
        """Return true."""
        return True

    def take_int(self, args):
        """Take int."""
        return int(args[0])


class TestFunctionParser(TestCase):
    """Test Function parser."""

    def setUp(self) -> None:
        self.my_func_class = MyFuncClass()
        return super().setUp()

    def test_good(self):
        """Handle acceptable value."""
        ret = FunctionParser.exec(self.my_func_class, "ret_true()")
        self.assertTrue(ret)

        ret = FunctionParser.exec(self.my_func_class, "take_int(100)")
        self.assertEqual(ret, 100)

    def test_without_parenthesis(self):
        """Forget parenthesis."""
        with self.assertRaises(ValueError):
            FunctionParser.exec(self.my_func_class, "ret_true")

    def test_forget_parenthesis_closing(self):
        """Forget parenthesis closing."""
        with self.assertRaises(ValueError):
            FunctionParser.exec(self.my_func_class, "ret_true(")

    def test_not_exists_function(self):
        """Test not existing function."""
        with self.assertRaises(ValueError):
            FunctionParser.exec(self.my_func_class, "no()")


if __name__ == '__main__':
    main()
