"""statics for mg400"""
import numpy as np
from numpy import linalg as LA

from .specification_mg400 import LINK1, LINK2, LINK3, LINK4


def jacobian_fk(angles):
    """jacobian_fk"""
    j_1, j_2, j_3, _, _, _ = np.deg2rad(angles)
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

    jacobi = np.array([[elm_11, elm_12, elm_13],
                       [elm_21, elm_22, elm_23],
                       [elm_31, elm_32, elm_33]])
    return jacobi


def jacobian_inv(angles):
    """jacobian_inv"""
    j_1, j_2, j_3, _, _, _ = np.deg2rad(angles)
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

    jacobi_inv = np.array([[elm_11, elm_12, elm_13],
                           [elm_21, elm_22, elm_23],
                           [elm_31, elm_32, elm_33]])
    return jacobi_inv


def convert_speed(q_actual, tool_speed):
    """convert_speed"""
    joint_speed = np.dot(jacobian_inv(q_actual), tool_speed)
    return np.rad2deg(np.squeeze(np.asarray(joint_speed)))
