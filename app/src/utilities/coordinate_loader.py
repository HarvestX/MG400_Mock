"""coordinate loader."""
import re

import yaml


def load_coordinate(path, max_list_length=10):
    """load_coordinate"""
    with open(path, 'r', encoding="utf-8") as file:
        coord_dict: dict = yaml.safe_load(file)

    coord_list = [[0., 0., 0., 0.]] * max_list_length
    for coord_name, values in coord_dict.items():
        index = int(re.sub(r"\D", "", coord_name))
        coord_list[index] = \
            [values["x"], values["y"], values["z"], values["r"]]
    return coord_list
