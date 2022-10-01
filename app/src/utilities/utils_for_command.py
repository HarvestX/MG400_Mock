"""Utils for Commands."""
from typing import List


def generate_return_msg(error_id: int, vals=None):
    """generate_return_msg"""
    if vals is None:
        vals = []
    msg = str(error_id) + ",{" + ",".join(list(map(str, vals))) + "},"
    return msg


def args_parser_mt_cmd(args: List[str]):
    """args_parser_mt_cmd"""
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
