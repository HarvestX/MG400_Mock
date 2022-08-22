"""dobot thread."""
import logging
import threading
import time

from .dobot_hardware import DobotHardware


class DobotThread(threading.Thread):
    """DobotThread"""
    logger: logging.Logger

    def __init__(self, dobot: DobotHardware) -> None:
        super(DobotThread, self).__init__()
        self.logger = logging.getLogger("Dobot_Thread")
        self.__dobot = dobot
        self.__timestep = self.__dobot.get_timestep()

    def run(self):
        """run"""
        while True:
            self.__dobot.update_status()
            time.sleep(self.__timestep)
