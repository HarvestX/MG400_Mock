"""dobot thread."""
import logging
import threading
import time

from tcp_interface.function_parser import FunctionParser

from .dobot_hardware import DobotHardware
from .motion_command import MotionCommands


class DobotThread(threading.Thread):
    """DobotThread"""
    logger: logging.Logger

    def __init__(self, dobot: DobotHardware) -> None:
        super(DobotThread, self).__init__()
        self.logger = logging.getLogger("Dobot Thread")
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
