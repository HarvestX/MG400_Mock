"""MG400 Mock Initial File."""
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

import tcp_interface
from dobot_command.dobot_hardware import DobotHardware
from dobot_command.dobot_thread import DobotThread

logging.basicConfig(level=logging.INFO)


def main():
    """MG400 Mock Initial Point"""
    dobot = DobotHardware()

    dobot_thread = DobotThread(dobot)

    dashboard_tcp = tcp_interface.DashboardTcpInterface(
        "0.0.0.0", 29999, dobot
    )

    motion_tcp = tcp_interface.MotionTcpInterface(
        "0.0.0.0", 30003, dobot
    )

    feedback_tcp = tcp_interface.RealtimeFeedbackTcpInterface(
        "0.0.0.0", 30004, dobot
    )

    dobot_thread.start()
    dashboard_tcp.start()
    motion_tcp.start()
    feedback_tcp.start()


if __name__ == "__main__":
    main()
