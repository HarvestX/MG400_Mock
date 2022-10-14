"""Utils for Commands."""
from typing import List


def generate_return_msg(error_id: int, vals=None):
    """generate_return_msg"""
    if vals is None:
        vals = []
    msg = str(error_id) + ",{" + ",".join(list(map(str, vals))) + "},"
    return msg


def args_parser_mov_j(args: List[str]):
    """args_parser_mov_j"""
    user = tool = speed_j = acc_j = None
    for arg in args:
        if "User=" in arg:
            user = int(arg[arg.rfind("=")+1:])
        elif "Tool=" in arg:
            tool = int(arg[arg.rfind("=")+1:])
        elif "SpeedJ=" in arg:
            speed_j = int(arg[arg.rfind("=")+1:])
        elif "AccJ=" in arg:
            acc_j = int(arg[arg.rfind("=")+1:])
    return user, tool, speed_j, acc_j


def args_parser_mov_l(args: List[str]):
    """args_parser_mov_l"""
    user = tool = speed_l = acc_l = None
    for arg in args:
        if "User=" in arg:
            user = int(arg[arg.rfind("=")+1:])
        elif "Tool=" in arg:
            tool = int(arg[arg.rfind("=")+1:])
        elif "SpeedL=" in arg:
            speed_l = int(arg[arg.rfind("=")+1:])
        elif "AccL=" in arg:
            acc_l = int(arg[arg.rfind("=")+1:])
    return user, tool, speed_l, acc_l


def args_parser_jog(args: List[str]):
    """args_parser_jog"""
    coord_type = user = tool = None
    for arg in args:
        if "CoordType=" in arg:
            coord_type = int(arg[arg.rfind("=")+1:])
        elif "User=" in arg:
            user = int(arg[arg.rfind("=")+1:])
        elif "Tool=" in arg:
            tool = int(arg[arg.rfind("=")+1:])
    return coord_type, user, tool
