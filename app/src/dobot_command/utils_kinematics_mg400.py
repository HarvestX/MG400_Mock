"""utilities for tester mg400."""
import numpy as np

J1_MIN = -160
J1_MAX = 160
J2_MIN = -25
J2_MAX = 85
J3_MIN = -25
J3_MAX = 105
J3_1_MIN = -60
J3_1_MAX = 60


def in_working_space(angles):
    """in_working_space_angle"""
    j_1, j_2, j_3, _, _, _ = angles
    j_1_able = in_check(J1_MIN, j_1, J1_MAX)
    j_2_able = in_check(J2_MIN, j_2, J2_MAX)
    j_3_able = in_check(J3_MIN, j_3, J3_MAX)
    j_3_1_able = in_check(J3_1_MIN, j_2 + j_3, J3_1_MAX)
    if j_1_able and j_2_able and j_3_able and j_3_1_able:
        return True
    return False


def rot_y(vec, angle):
    """rot_y"""
    angle = np.deg2rad(angle)
    rot_mtrx = np.array([[np.cos(angle), 0, np.sin(angle)],
                         [0, 1, 0],
                         [-np.sin(angle), 0, np.cos(angle)]])
    return np.dot(rot_mtrx, vec)


def rot_z(vec, angle):
    """rot_z"""
    angle = np.deg2rad(angle)
    rot_mtrx = np.array([[np.cos(angle), -np.sin(angle), 0],
                         [np.sin(angle), np.cos(angle), 0],
                         [0, 0, 1]])
    return np.dot(rot_mtrx, vec)


def in_check(min_val, x_val, max_val):
    """in_check"""
    if min_val <= x_val <= max_val:
        return True
    else:
        return False
