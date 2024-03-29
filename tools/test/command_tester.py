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
sys.path.append('../../app/src/')
utilities = importlib.import_module('utilities')
forward_kinematics = utilities.kinematics_mg400.forward_kinematics
J1_MAX = utilities.kinematics_mg400.J1_MAX
J1_MIN = utilities.kinematics_mg400.J1_MIN
J2_MAX = utilities.kinematics_mg400.J2_MAX
J2_MIN = utilities.kinematics_mg400.J2_MIN
J3_MAX = utilities.kinematics_mg400.J3_MAX
J3_MIN = utilities.kinematics_mg400.J3_MIN
EPS = 1

CMD_TYPE = "MovJ"

RATIO = 10
SPEED_FACTOR = \
    f"ros2 service call /mg400/speed_factor \
        mg400_msgs/srv/SpeedFactor '{{ratio: {RATIO}}}'"
print(SPEED_FACTOR)
proc = subprocess.run(SPEED_FACTOR, shell=True, check=True)

for _ in range(100):

    while True:
        j_1 = round(random.uniform(J1_MIN+EPS, J1_MAX-EPS), 3)
        j_2 = round(random.uniform(J2_MIN+EPS, J2_MAX-EPS), 3)
        j_3 = round(random.uniform(J3_MIN+EPS, J3_MAX-EPS), 3)
        j_4 = round(random.uniform(-180+EPS, 180-EPS), 3)

        angles = np.array([j_1, j_2, j_3, j_4, 0, 0])
        try:
            tool_vec = forward_kinematics(angles)
            break
        except ValueError:
            continue

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

    time.sleep(0.5)
