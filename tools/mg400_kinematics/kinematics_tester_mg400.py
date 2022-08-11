"""MG400 Kinematics Tester."""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from utils_tester_mg400 import (J2_MAX, J2_MIN, J3_MAX, J3_MIN, cal_link_pos,
                                in_check, init_fig)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def update(_):
    """update"""
    j3_1_min = -60
    j3_1_max = 60

    j2_val = theta_j2_slider.val
    j3_val = theta_j3_slider.val

    if in_check(j3_1_min, j3_val-j2_val, j3_1_max):
        link1, link2, link3, link4 = cal_link_pos(j2_val, j3_val)
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

slider1_pos = plt.axes([0.11, 0.05, 0.8, 0.03])
slider2_pos = plt.axes([0.11, 0.01, 0.8, 0.03])

theta_j2_slider = Slider(slider1_pos, "j2 [deg]", J2_MIN, J2_MAX, valinit=0)
theta_j3_slider = Slider(slider2_pos, "j3 [deg]", J3_MIN, J3_MAX, valinit=0)

theta_j2_slider.on_changed(update)
theta_j3_slider.on_changed(update)

plt.grid()
plt.show()
