import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def rotation_o(u, t):
    t = np.deg2rad(t)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return np.dot(R, u)


def cal_link_pos(theta2, theta3):
    link1 = np.array([0, 175])
    link2 = np.array([175, 0])
    link3 = np.array([66, -57])

    link1 = rotation_o(link1, -theta2)
    link2 = link1 + rotation_o(link2, -theta2 - theta3)
    link3 = link2 + link3

    return link1, link2, link3


def update(_):
    j2 = theta_j2_slider.val
    j3 = theta_j3_slider.val

    j2_1 = j2
    j3_1 = min(max(-60, j3 - j2), 60)
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

THETA1 = 0
THETA2 = 0
origin = np.array([0, 0])
link1, link2, link3 = cal_link_pos(THETA1, THETA2)

plt.grid()
link1_line = ax.plot([origin[0], link1[0]], [origin[1], link1[1]], linewidth=3)
link2_line = ax.plot([link1[0], link2[0]], [link1[1], link2[1]], linewidth=3)
link3_line = ax.plot([link2[0], link3[0]], [link2[1], link3[1]], linewidth=3)


slider1_pos = plt.axes([0.11, 0.05, 0.8, 0.03])
slider2_pos = plt.axes([0.11, 0.01, 0.8, 0.03])


j2_min = -25
j2_max = 85
j3_min = -25
j3_max = 105

theta_j2_slider = Slider(slider1_pos, "j2 [deg]", j2_min, j2_max, valinit=0)
theta_j3_slider = Slider(slider2_pos, "j3 [deg]", j3_min, j3_max, valinit=0)

theta_j2_slider.on_changed(update)
theta_j3_slider.on_changed(update)

plt.grid()
plt.show()
