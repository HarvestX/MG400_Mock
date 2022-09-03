"""MG400 Kinematics Tester."""
import importlib
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from PIL import Image
from utils_visualizer import link_pos_2d

# for relative import
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../../app/src/')
utilities = importlib.import_module('utilities')
J2_MAX = utilities.specification_mg400.J2_MAX
J2_MIN = utilities.specification_mg400.J2_MIN
J3_MAX = utilities.specification_mg400.J3_MAX
J3_MIN = utilities.specification_mg400.J3_MIN
forward_kinematics = utilities.kinematics_mg400.forward_kinematics


def init_fig():
    """init_fig"""
    fig_plt, ax_plt = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.15)
    plt.xlim(-300, 500)
    plt.ylim(-300, 500)
    img = Image.open("../../media/mg400_workspace.png")
    ax_plt.imshow(img, alpha=1.0, extent=[-444, 756, -598, 602])
    ax_plt.set_aspect(1)
    return fig_plt, ax_plt


def update(_):
    """update"""
    j_2 = j2_slider.val
    j_3 = j3_slider.val
    angles = [0, j_2, j_3, 0, 0, 0]
    solved, tool_vec = forward_kinematics(angles)
    _ = tool_vec  # for pylint warning

    if solved is True:
        link1, link2, link3, link4 = link_pos_2d(angles)
        link1_line[0].set_xdata([ORIGIN[0], link1[0]])
        link1_line[0].set_ydata([ORIGIN[1], link1[1]])
        link2_line[0].set_xdata([link1[0], link2[0]])
        link2_line[0].set_ydata([link1[1], link2[1]])
        link3_line[0].set_xdata([link2[0], link3[0]])
        link3_line[0].set_ydata([link2[1], link3[1]])
        link4_line[0].set_xdata([link3[0], link4[0]])
        link4_line[0].set_ydata([link3[1], link4[1]])

    fig.canvas.draw_idle()


J2_INIT = 0
J3_INIT = 0
ORIGIN = np.array([0, 0])
init_angles = [0, J2_INIT, J3_INIT, 0, 0, 0]
init_link1, init_link2, init_link3, init_link4 = link_pos_2d(init_angles)

fig, ax = init_fig()
plt.grid()
link1_line = ax.plot([ORIGIN[0], init_link1[0]],
                     [ORIGIN[1], init_link1[1]],
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

j2_slider = Slider(slider1_pos, "j2 [deg]", J2_MIN, J2_MAX, valinit=0)
j3_slider = Slider(slider2_pos, "j3 [deg]", J3_MIN, J3_MAX, valinit=0)

j2_slider.on_changed(update)
j3_slider.on_changed(update)

plt.grid()
plt.show()
