"""MG400 Kinematics Tester."""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def rotation_o(vec, angle):
    """rotation_o"""
    angle = np.deg2rad(angle)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                 [np.sin(angle), np.cos(angle)]])
    return np.dot(R, vec)


def cal_link_pos(theta2, theta3):
    """cal_link_pos"""
    link1_base = np.array([0, 175])
    link2_base = np.array([175, 0])
    link3_base = np.array([66, -57])

    link1_base = rotation_o(link1_base, -theta2)
    link2_base = link1_base + rotation_o(link2_base, -theta2 - theta3)
    link3_base = link2_base + link3_base

    return link1_base, link2_base, link3_base


def update(_):
    """update"""
    j3_1_min = -60
    j3_1_max = 60

    j2_val = theta_j2_slider.val
    j3_val = theta_j3_slider.val

    j2_1 = j2_val
    j3_1 = min(max(j3_1_min, j3_val - j2_val), j3_1_max)
    link1, link2, link3 = cal_link_pos(j2_1, j3_1)

    link1_line[0].set_xdata([origin[0], link1[0]])
    link1_line[0].set_ydata([origin[1], link1[1]])
    link2_line[0].set_xdata([link1[0], link2[0]])
    link2_line[0].set_ydata([link1[1], link2[1]])
    link3_line[0].set_xdata([link2[0], link3[0]])
    link3_line[0].set_ydata([link2[1], link3[1]])
    fig.canvas.draw_idle()


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.15)
plt.xlim(-300, 500)
plt.ylim(-300, 500)
im = Image.open("../../materials/mg400_workspace.png")
ax.imshow(im, alpha=1.0, extent=[-487, 713, -598, 602])
ax.set_aspect(1)

J2_INIT = 0
J3_INIT = 0

J2_MIN = -25
J2_MAX = 85
J3_MIN = -25
J3_MAX = 105

origin = np.array([0, 0])
init_link1, init_link2, init_link3 = cal_link_pos(J2_INIT, J3_INIT-J2_INIT)

plt.grid()
link1_line = ax.plot([origin[0], init_link1[0]],
                     [origin[1], init_link1[1]],
                     linewidth=3)
link2_line = ax.plot([init_link1[0], init_link2[0]],
                     [init_link1[1], init_link2[1]],
                     linewidth=3)
link3_line = ax.plot([init_link2[0], init_link3[0]],
                     [init_link2[1], init_link3[1]],
                     linewidth=3)


slider1_pos = plt.axes([0.11, 0.05, 0.8, 0.03])
slider2_pos = plt.axes([0.11, 0.01, 0.8, 0.03])

theta_j2_slider = Slider(slider1_pos, "j2 [deg]", J2_MIN, J2_MAX, valinit=0)
theta_j3_slider = Slider(slider2_pos, "j3 [deg]", J3_MIN, J3_MAX, valinit=0)

theta_j2_slider.on_changed(update)
theta_j3_slider.on_changed(update)

plt.grid()
plt.show()
