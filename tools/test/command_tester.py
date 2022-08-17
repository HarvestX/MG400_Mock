"""tester MovJ."""
import importlib
import os
import random
import subprocess
import sys
import time

import numpy as np

# for relative import
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../../app/src/utilities/')
kinematics_mg400 = importlib.import_module('kinematics_mg400')
forward_kinematics = kinematics_mg400.forward_kinematics

J1_MAX = kinematics_mg400.J1_MAX
J1_MIN = kinematics_mg400.J1_MIN
J2_MAX = kinematics_mg400.J2_MAX
J2_MIN = kinematics_mg400.J2_MIN
J3_MAX = kinematics_mg400.J3_MAX
J3_MIN = kinematics_mg400.J3_MIN
EPS = 1

CMD_TYPE = "MovJ"

for _ in range(100):

    SOLVED = False
    while not SOLVED:
        j_1 = round(random.uniform(J1_MIN+EPS, J1_MAX-EPS), 3)
        j_2 = round(random.uniform(J2_MIN+EPS, J2_MAX-EPS), 3)
        j_3 = round(random.uniform(J3_MIN+EPS, J3_MAX-EPS), 3)
        j_4 = round(random.uniform(-180+EPS, 180-EPS), 3)

        angles = np.array([j_1, j_2, j_3, j_4, 0, 0])
        SOLVED, tool_vec = forward_kinematics(angles)

    xx = round(tool_vec[0]/1000, 3)
    yy = round(tool_vec[1]/1000, 3)
    zz = round(tool_vec[2]/1000, 3)

    if CMD_TYPE == "MovJ":
        cmd = "ros2 service call /mg400/mov_j mg400_msgs/srv/MovJ " \
            f"'{{x: {xx}, y: {yy}, z: {zz}}}'"
    elif CMD_TYPE == "MovL":
        cmd = "ros2 service call /mg400/mov_l mg400_msgs/srv/MovL " \
            f"'{{x: {xx}, y: {yy}, z: {zz}}}'"

    print(cmd)
    proc = subprocess.run(cmd, shell=True, check=True)

    time.sleep(5)
