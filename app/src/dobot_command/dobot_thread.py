"""dobot thread."""
import threading
import time

from .dobot_hardware import DobotHardware


class DobotThread(threading.Thread):
    """DobotThread"""

    def __init__(self, dobot: DobotHardware) -> None:
        super(DobotThread, self).__init__()
        self.__dobot = dobot
        self.__timestep = self.__dobot.get_timestep()

    def run(self):
        """run"""
        while True:
            # self.__dobot.test_func()
            self.__dobot.update_status()
            time.sleep(self.__timestep)
