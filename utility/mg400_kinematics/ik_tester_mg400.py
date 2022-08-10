"""MG400 Kinematics Tester."""

import math
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from utils_tester_mg400 import (J2_MAX, J2_MIN, J3_1_MAX, J3_1_MIN, J3_MAX,
                                J3_MIN, cal_link_pos, in_check, init_fig)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def inverse_kinematics(p_x, p_y):
    """inverse_kinematics"""
    p_x = p_x - 66 - 43
    p_y = p_y + 57
    length2 = 175
    length3 = 175

    val1 = (p_x**2+p_y**2-length2**2-length3**2) / (2*length2*length3)
    if val1 < -1 or val1 > 1:
        return False, 0, 0

    j3_1_ik = math.asin(val1)
    j2_ik = math.atan2(p_y, p_x) -\
        math.atan2(length2+length3 * math.sin(j3_1_ik),
                   length3*math.cos(j3_1_ik))
    j2_ik = -np.rad2deg(j2_ik)
    j3_1_ik = -np.rad2deg(j3_1_ik)
    j3_ik = j2_ik + j3_1_ik

    if not(in_check(J2_MIN, j2_ik, J2_MAX) and
           in_check(J3_1_MIN, j3_1_ik, J3_1_MAX) and in_check(J3_MIN, j3_ik, J3_MAX)):
        return False, 0, 0

    return True, j2_ik, j3_ik


def update(_):
    """update"""

    x_val = x_slider.val
    y_val = y_slider.val

    tip.set_offsets([x_val, y_val])

    solved, j2_ik, j3_ik = inverse_kinematics(x_val, y_val)

    if solved is True:
        link1, link2, link3, link4 = cal_link_pos(j2_ik, j3_ik)

        link1_line[0].set_xdata([origin[0], link1[0]])
        link1_line[0].set_ydata([origin[1], link1[1]])
        link2_line[0].set_xdata([link1[0], link2[0]])
        link2_line[0].set_ydata([link1[1], link2[1]])
        link3_line[0].set_xdata([link2[0], link3[0]])
        link3_line[0].set_ydata([link2[1], link3[1]])
        link4_line[0].set_xdata([link3[0], link4[0]])
        link4_line[0].set_ydata([link3[1], link4[1]])

    fig.canvas.draw_idle()


fig, ax = init_fig()
J2_INIT = 0
J3_INIT = 0

X_MIN = 100
X_MAX = 500
Y_MIN = -300
Y_MAX = 300

origin = np.array([0, 0])
init_link1, init_link2, init_link3, init_link4 = cal_link_pos(
    J2_INIT, J3_INIT-J2_INIT)

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
link4_line = ax.plot([init_link3[0], init_link4[0]],
                     [init_link3[1], init_link4[1]],
                     linewidth=3)

tip = ax.scatter(0, 0, s=100, c="red", zorder=100)

slider1_pos = plt.axes([0.11, 0.05, 0.8, 0.03])
slider2_pos = plt.axes([0.11, 0.01, 0.8, 0.03])

x_slider = Slider(slider1_pos, "x", X_MIN, X_MAX, valinit=(X_MAX+X_MIN)/2)
y_slider = Slider(slider2_pos, "y", Y_MIN, Y_MAX, valinit=(Y_MAX+Y_MIN)/2)

x_slider.on_changed(update)
y_slider.on_changed(update)

plt.grid()
plt.show()
