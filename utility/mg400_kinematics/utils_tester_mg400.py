"""utilities for tester mg400."""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

J2_MIN = -25
J2_MAX = 85
J3_MIN = -25
J3_MAX = 105
J3_1_MIN = -60
J3_1_MAX = 60


def init_fig():
    """init_fig"""
    fig, ax_plt = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.15)
    plt.xlim(-300, 500)
    plt.ylim(-300, 500)
    img = Image.open("../../materials/mg400_workspace.png")
    ax_plt.imshow(img, alpha=1.0, extent=[-487+43, 713+43, -598, 602])
    ax_plt.set_aspect(1)
    return fig, ax_plt


def rotation_o(vec, angle):
    """rotation_o"""
    angle = np.deg2rad(angle)
    rot_mtrx = np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])
    return np.dot(rot_mtrx, vec)


def cal_link_pos(j2_fk, j3_fk):
    """cal_link_pos"""
    link1_base = np.array([284 - (175 + 66), 0])
    link2_base = np.array([0, 175])
    link3_base = np.array([175, 0])
    link4_base = np.array([66, -57])

    link2_base = link1_base + rotation_o(link2_base, -j2_fk)
    link3_base = link2_base + rotation_o(link3_base, -j3_fk)
    link4_base = link3_base + link4_base

    return link1_base, link2_base, link3_base, link4_base


def in_check(min_val, x_val, max_val):
    """in_check"""
    if min_val <= x_val <= max_val:
        return True
    else:
        return False