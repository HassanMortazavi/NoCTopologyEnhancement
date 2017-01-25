import math
from random import randint
from Topology import Topology


def re_config_hub_connections_list(hub_connections_list):
    random_selected_node = randint(0, len(hub_connections_list) - 1)
    hub_connections_list[random_selected_node] = 1 - hub_connections_list[random_selected_node]
    return hub_connections_list


class SA:
    current_topology = Topology(0, 0, 0, 0, [], 0)

    def __init__(self, network_size, network_hub_reliability):
        net_dim = int(math.sqrt(network_size))
        hub_connections_list = []
        for i in range(0, network_size):
            hub_connections_list.append(i % 2)
        self.current_topology.set_new_config(net_dim, net_dim, 1, 1, hub_connections_list, network_hub_reliability)

    def generate_new_topology(self):
        self.current_topology.node_hub_connection_list = re_config_hub_connections_list(
            self.current_topology.node_hub_connection_list)
