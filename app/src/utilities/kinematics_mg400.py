"""kinematics for mg400"""
import math

import numpy as np
from numpy import linalg as LA

from .specification_mg400 import (J1_MAX, J1_MIN, J2_MAX, J2_MIN, J3_1_MAX,
                                  J3_1_MIN, J3_MAX, J3_MIN, J4_MAX, J4_MIN,
                                  LINK1, LINK2, LINK3, LINK4)

ROUND_DECIMALS = 6


def in_working_space(angles):
    """in_working_space_angle"""
    j_1, j_2, j_3, j_4, _, _ = angles
    j_1_able = (J1_MIN <= j_1 <= J1_MAX)
    j_2_able = (J2_MIN <= j_2 <= J2_MAX)
    j_3_able = (J3_MIN <= j_3 <= J3_MAX)
    j_3_1_able = (J3_1_MIN <= (j_3 - j_2) <= J3_1_MAX)
    j_4_able = (J4_MIN <= j_4 <= J4_MAX)
    if j_1_able and j_2_able and \
            j_3_able and j_3_1_able and j_4_able:
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


def homo_y(vec, trans, angle):
    """rot_y"""
    angle = np.deg2rad(angle)
    rot_mtrx = np.array([[np.cos(angle), 0, np.sin(angle), trans[0]],
                         [0, 1, 0, trans[1]],
                         [-np.sin(angle), 0, np.cos(angle), trans[2]],
                         [0, 0, 0, 1]])
    temp = np.dot(rot_mtrx, np.append(vec, 1))
    return temp[0:3]


def homo_z(vec, trans, angle):
    """rot_z"""
    angle = np.deg2rad(angle)
    rot_mtrx = np.array([[np.cos(angle), -np.sin(angle), 0, trans[0]],
                         [np.sin(angle), np.cos(angle), 0, trans[1]],
                         [0, 0, 1, trans[2]],
                         [0, 0, 0, 1]])
    temp = np.dot(rot_mtrx, np.append(vec, 1))
    return temp[0:3]


def forward_kinematics(angles):
    """forward_kinematics"""
    if not in_working_space(angles):
        raise ValueError("outside of workspace.")
    j_1, j_2, j_3, j_4, _, _ = angles
    pos = LINK1 + \
        rot_y(LINK2, j_2) + \
        rot_y(LINK3, j_3) + LINK4

    p_x, p_y, p_z = rot_z(pos, j_1)
    Rx = j_1 + j_4
    tool_vec = np.round([p_x, p_y, p_z, Rx, 0, 0], decimals=ROUND_DECIMALS)
    return tool_vec


def inverse_kinematics(tool_vec):
    """inverse_kinematics"""
    p_x, p_y, p_z, Rx, _, _ = tool_vec
    pp_x = LA.norm([p_x, p_y]) - LINK4[0] - LINK1[0]
    pp_z = p_z - LINK4[2] - LINK1[2]
    length2 = LA.norm(LINK2)
    length3 = LA.norm(LINK3)

    j_1 = math.atan2(p_y, p_x)

    val1 = (pp_x**2+pp_z**2-length2**2-length3**2) / (2*length2*length3)
    if val1 < -1 or val1 > 1:
        raise ValueError("outside of workspace.")
    j_3_1 = math.asin(val1)

    j_2 = math.atan2(pp_z, pp_x) -\
        math.atan2(length2+length3 * math.sin(j_3_1),
                   length3*math.cos(j_3_1))

    j_1 = np.rad2deg(j_1)
    j_2 = -np.rad2deg(j_2)
    j_3_1 = -np.rad2deg(j_3_1)
    j_3 = j_2 + j_3_1
    j_4 = Rx - j_1
    angles = np.round([j_1, j_2, j_3, j_4, 0., 0.], decimals=ROUND_DECIMALS)

    if not in_working_space(angles):
        raise ValueError("outside of workspace.")
    return np.array(angles)


def basecoord_to_toolcoord(vec, tool_coord):
    """convert_toolvec_to_toolcoord"""
    pos = np.array(vec[0:3]) + np.array(tool_coord[0:3])
    ang = vec[3]-tool_coord[-1]
    return np.array([*pos, ang, 0., 0.])


def toolcoord_to_basecoord(vec, tool_coord):
    """convert_toolcoord_to_toolvec"""
    pos = np.array(vec[0:3]) - np.array(tool_coord[0:3])
    ang = vec[3]+tool_coord[-1]
    return np.array([*pos, ang, 0., 0.])


def inverse_kinematics_t2b(tool_vec, tool_coord):
    """inverse_kinematics_t2b"""
    tool_vec_base = toolcoord_to_basecoord(tool_vec, tool_coord)
    angles = inverse_kinematics(tool_vec_base)
    return angles


def forward_kinematics_b2t(angles, tool_coord):
    """forward_kinematics_b2t"""
    tool_vec_base = forward_kinematics(angles)
    tool_vec = basecoord_to_toolcoord(tool_vec_base, tool_coord)
    return tool_vec
