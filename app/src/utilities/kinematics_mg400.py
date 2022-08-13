"""utilities for tester mg400."""
import math

import numpy as np
from numpy import linalg as LA

J1_MIN = -160
J1_MAX = 160
J2_MIN = -25
J2_MAX = 85
J3_MIN = -25
J3_MAX = 105
J3_1_MIN = -60
J3_1_MAX = 60


LINK1 = np.array([43, 0, 0])
LINK2 = np.array([0, 0, 175])
LINK3 = np.array([175, 0, 0])
LINK4 = np.array([66, 0, -57])


def in_working_space(angles):
    """in_working_space_angle"""
    j_1, j_2, j_3, _, _, _ = angles
    j_1_able = in_check(J1_MIN, j_1, J1_MAX)
    j_2_able = in_check(J2_MIN, j_2, J2_MAX)
    j_3_able = in_check(J3_MIN, j_3, J3_MAX)
    j_3_1_able = in_check(J3_1_MIN, j_3 - j_2, J3_1_MAX)
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


def forward_kinematics(angles):
    """forward_kinematics"""

    if not in_working_space(angles):
        return False, np.array([0.]*6)
    j_1, j_2, j_3, j_4, _, _ = angles
    pos = LINK1 + \
        rot_y(LINK2, j_2) + \
        rot_y(LINK3, j_3) + LINK4

    p_x, p_y, p_z = rot_z(pos, j_1)
    Rz = j_1 + j_4
    return True, np.array([p_x, p_y, p_z, 0, 0, Rz])


def inverse_kinematics(tool_vec):
    """inverse_kinematics"""
    p_x, p_y, p_z, _, _, Rz = tool_vec
    pp_x = LA.norm([p_x, p_y]) - LINK4[0] - LINK1[0]
    pp_z = p_z - LINK4[2] - LINK1[2]
    length2 = LA.norm(LINK2)
    length3 = LA.norm(LINK3)

    j_1 = math.atan2(p_y, p_x)

    val1 = (pp_x**2+pp_z**2-length2**2-length3**2) / (2*length2*length3)
    if val1 < -1 or val1 > 1:
        return False, np.array([0.]*6)
    j_3_1 = math.asin(val1)

    j_2 = math.atan2(pp_z, pp_x) -\
        math.atan2(length2+length3 * math.sin(j_3_1),
                   length3*math.cos(j_3_1))

    j_1 = np.rad2deg(j_1)
    j_2 = -np.rad2deg(j_2)
    j_3_1 = -np.rad2deg(j_3_1)
    j_3 = j_2 + j_3_1
    j_4 = np.rad2deg(Rz) - j_1
    angles = [j_1, j_2, j_3, j_4, 0., 0.]

    if not in_working_space(angles):
        return False, np.array([0.]*6)
    return True, np.array(angles)


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


def jacobian_fk(angles):
    """jacobian_fk"""
    j_1, j_2, j_3, _, _, _ = angles
    len1 = LA.norm(LINK1)
    len2 = LA.norm(LINK2)
    len3 = LA.norm(LINK3)
    len4_x = LINK4[0]

    elm_11 = -np.sin(j_1)*(len1 + len4_x + len3*np.cos(j_3) + len2*np.sin(j_2))
    elm_12 = len2*np.cos(j_1)*np.cos(j_2)
    elm_13 = -len3*np.cos(j_1)*np.sin(j_3)
    elm_21 = np.cos(j_1)*(len1 + len4_x + len3*np.cos(j_3) + len2*np.sin(j_2))
    elm_22 = len2*np.cos(j_2)*np.sin(j_1)
    elm_23 = -len3*np.sin(j_1)*np.sin(j_3)
    elm_31 = 0.
    elm_32 = -len2*np.sin(j_2)
    elm_33 = -len3*np.cos(j_3)

    jacobi = np.matrix([[elm_11, elm_12, elm_13],
                        [elm_21, elm_22, elm_23],
                        [elm_31, elm_32, elm_33]])
    return jacobi


def jacobian_inv(angles):
    """jacobian_inv"""
    j_1, j_2, j_3, _, _, _ = angles
    len1 = LA.norm(LINK1)
    len2 = LA.norm(LINK2)
    len3 = LA.norm(LINK3)
    len4_x = LINK4[0]
    denom1 = len1 + len4_x + len3*np.cos(j_3) + len2*np.sin(j_2)
    denom2 = len2*np.cos(j_2-j_3)
    denom3 = len3*np.cos(j_2-j_3)

    elm_11 = -np.sin(j_1)/denom1
    elm_12 = np.cos(j_1)/denom1
    elm_13 = 0
    elm_21 = np.cos(j_1)*np.cos(j_3)/denom2
    elm_22 = np.sin(j_1)*np.cos(j_3)/denom2
    elm_23 = -np.sin(j_3)/denom2
    elm_31 = -np.cos(j_1)*np.sin(j_2)/denom3
    elm_32 = -np.sin(j_1)*np.sin(j_2)/denom3
    elm_33 = -np.cos(j_2)/denom3

    jacobi_inv = np.matrix([[elm_11, elm_12, elm_13],
                            [elm_21, elm_22, elm_23],
                            [elm_31, elm_32, elm_33]])
    return jacobi_inv
