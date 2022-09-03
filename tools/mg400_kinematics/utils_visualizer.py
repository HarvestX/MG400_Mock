"""utils for visualize test"""
import importlib
import os
import sys

# for relative import
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../../app/src/')
utilities = importlib.import_module('utilities')
LINK1 = utilities.specification_mg400.LINK1
LINK2 = utilities.specification_mg400.LINK2
LINK3 = utilities.specification_mg400.LINK3
LINK4 = utilities.specification_mg400.LINK4
rot_y = utilities.kinematics_mg400.rot_y


def link_pos_2d(angles):
    """for calculating link positions for tools

    Args:
        angles (List[float]): joint angles (j1-j6)

    Returns:
        link vector: vectors describing the link positions
    """
    _, j_2, j_3, _, _, _ = angles
    link2_rot = LINK1 + rot_y(LINK2, j_2)
    link3_rot = link2_rot + rot_y(LINK3, j_3)
    link4_rot = link3_rot + LINK4

    return LINK1[::2], link2_rot[::2], link3_rot[::2], link4_rot[::2]
