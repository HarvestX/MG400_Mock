"""dobot thread."""
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

import logging
import threading
import time

from utilities.function_parser import FunctionParser

from .dobot_hardware import DobotHardware
from .motion_command import MotionCommands


class DobotThread(threading.Thread):
    """DobotThread"""
    logger: logging.Logger

    def __init__(self, dobot: DobotHardware) -> None:
        super(DobotThread, self).__init__()
        self.logger = logging.getLogger("Dobot_Thread")
        self.__dobot = dobot
        self.__motion_commands = MotionCommands(dobot)
        self.__timestep = self.__dobot.get_timestep()

    def run(self):
        """run"""
        while True:
            empty, command = self.__dobot.motion_unstack()

            if not empty:
                self.logger.info(command)
                try:
                    FunctionParser.exec(self.__motion_commands, command)
                except ValueError as err:
                    self.logger.error(err)
            self.__dobot.update_status()
            time.sleep(self.__timestep)
