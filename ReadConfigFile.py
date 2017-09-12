import json
from Improver import Improver

from FileHandler import read_file


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def read_config_file(file_name):
    content = read_file(file_name)
    config_json = json.loads(find_between(content, "START_CONFIG_JSON", "END_CONFIG_JSON"))
    topo_lines_list = find_between(content, "START_INITIAL_TOPOLOGY", "END_INITIAL_TOPOLOGY").splitlines()
    hub_connections_list = []

    for topo_line in reversed(topo_lines_list):
        for char in topo_line:
            if char == "0" or char == "1":
                hub_connections_list.append(int(char))

    return Improver(network_size=len(hub_connections_list), subnet_x_dim=config_json['subnet_x_dim'], subnet_y_dim=config_json['subnet_y_dim'], network_hub_reliability=config_json['network_hub_reliability'], radio_unit_area=config_json['radio_unit_area'], hub_port_unit_area=config_json['hub_port_unit_area'],
             alpha=config_json['alpha'], maximum_hub_number=config_json['maximum_hub_number'], hub_connections_list=hub_connections_list)

