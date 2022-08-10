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
