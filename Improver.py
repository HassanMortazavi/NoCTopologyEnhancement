import math
from datetime import datetime
from random import randint
from Topology import Topology
from FileHandler import save_topology


class Improver:
    alpha = 0.0
    current_topology = Topology(0, 0, 0, 0, [], 0, 0, 0)

    def __init__(self, network_size, network_hub_reliability, radio_unit_area, hub_port_unit_area, alpha):
        net_dim = int(math.sqrt(network_size))
        hub_connections_list = []
        for i in range(0, network_size):
            hub_connections_list.append(0)
        hub_connections_list[30] = 1
        hub_connections_list[54] = 1
        hub_connections_list[80] = 1
        hub_connections_list[107] = 1
        hub_connections_list[148] = 1
        hub_connections_list[175] = 1
        hub_connections_list[201] = 1
        hub_connections_list[225] = 1

        self.current_topology.set_new_config(net_dim, net_dim, 4, 4, hub_connections_list, network_hub_reliability,
                                             radio_unit_area, hub_port_unit_area)
        self.alpha = alpha

    def generate_new_topology(self):
        random_selected_node = randint(0, len(self.current_topology.node_hub_connection_list) - 1)
        temp = self.current_topology.node_hub_connection_list
        temp[random_selected_node] = 1 - temp[random_selected_node]
        self.current_topology.set_new_config(self.current_topology.global_x_dim, self.current_topology.global_y_dim,
                                             self.current_topology.local_x_dim, self.current_topology.local_y_dim, temp,
                                             self.current_topology.hub_reliability,
                                             self.current_topology.radio_unit_area,
                                             self.current_topology.hub_port_unit_area)
        return random_selected_node

    def sa(self):
        Ti = 0.001
        Tf = 0.00001
        fast_down = 0.01
        typical_down = 0.05
        slow_down = 0.005
        iteration = 1

        current_t = Ti

        current_cost_function_value = self.current_topology.get_topology_avg_distance()

        while current_t > Tf:
            for i in range(0, iteration):
                old_topo = self.current_topology
                changed_node = self.generate_new_topology()
                next_cost_function_value = self.current_topology.get_topology_avg_distance()
                total_cost = (next_cost_function_value - current_cost_function_value)

                if total_cost > 0:
                    r = randint(0, 100) / 100
                    if r > math.exp(-total_cost / current_t):
                        self.current_topology = old_topo
                    else:
                        current_cost_function_value = next_cost_function_value
                        #self.current_topology = old_topo

                else:
                    current_cost_function_value = next_cost_function_value

            print("on T = " + str(current_t) + " cost_value = " + str(current_cost_function_value))
            # save_topology(self.current_topology)
            if Ti * 0.9 < current_t:
                current_t -= Ti * fast_down
            elif Ti * 0.1 < current_t:
                current_t -= Ti * typical_down
            else:
                current_t -= Ti * slow_down

    def start(self):
        print("start ...")
        before_run_time = datetime.now()
        #self.sa()
        save_topology(self.current_topology)
        print("finished!!!")
        print("exec time = " + str(datetime.now() - before_run_time))


    def test(self):
        self.current_topology.topology_relaibility_check()
        #print(self.current_topology.get_topology_avg_distance())
        """self.current_topology.set_new_config(self.current_topology.global_x_dim, self.current_topology.global_y_dim,
                                             self.current_topology.local_x_dim, self.current_topology.local_y_dim, self.current_topology.node_hub_connection_list,
                                             0.8,
                                             self.current_topology.radio_unit_area,
                                             self.current_topology.hub_port_unit_area)
        print(self.current_topology.get_topology_avg_distance())"""
