"""Dobot Hardware."""

import threading

from tcp_interface.realtime_packet import RealtimePacket


class DobotHardware:
    def __init__(self) -> None:
        self.__status = RealtimePacket()
        self.__pre_status = RealtimePacket()
        self.__lock = threading.Lock()

    def get_status(self) -> RealtimePacket:
        return self.__status

    def lock_mutex(self):
        self.__lock.acquire()

    def release_mutex(self):
        self.__lock.release()

    def set_status(self, key: str, value):
        self.__status.write(key, value)

    def __updata_qd(self, timestep: float):
        pre_q = self.__pre_status.read("q_actual")
        current_q = self.__status.read("q_actual")
        self.__status.write("qd_actual", (current_q - pre_q) / timestep)

    def update_status(self, timestep: float):
        self.__updata_qd(timestep)
        self.__pre_status = self.__status

    def clear_error(self):
        # TODO: clear error flags in this dobot
        pass
