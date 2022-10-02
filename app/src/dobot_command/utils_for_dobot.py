"""Utilities for Dobot."""
import numpy as np


def cal_trapezoid_time(pos_init, pos_target, acc, v_l, v_s=0.):
    """cal_trapezoid_time"""
    dist = np.abs(pos_target - pos_init)
    v_s = np.abs(v_s)
    v_l_max = np.sqrt(acc*dist + v_s**2)

    if v_l_max > v_l:
        time_acc = (v_l-v_s) / acc
        time_const = dist/v_l - (v_l**2 - v_s**2) / (acc*v_l)
        time_total = 2*time_acc + time_const
    else:
        time_acc = (v_l_max-v_s)/acc
        time_const = 0
        time_total = 2*time_acc
    return time_acc, time_const, time_total


def gene_trapezoid_traj(pos_init, pos_target, acc,
                        v_l, timestep, v_s=0.):
    """gene_trapezoid_traj"""
    time_acc, time_const, _ = cal_trapezoid_time(
        pos_init, pos_target, acc, v_l, v_s)
    sign_velo = np.sign(pos_target-pos_init)

    time_acc_list = np.linspace(0, time_acc, num=int(
        time_acc/timestep) + 1, endpoint=True)
    traj_start = sign_velo * 0.5 * acc * (time_acc_list**2) + pos_init

    time_const_list = np.linspace(0, time_const, num=int(
        time_const/timestep) + 1, endpoint=True)
    traj_mid = sign_velo * v_l * time_const_list + traj_start[-1]

    traj_end = traj_mid[-1] - \
        sign_velo * 0.5 * acc*(time_acc_list**2-2*time_acc_list*time_acc)

    return np.concatenate([traj_start, traj_mid, traj_end], 0)
