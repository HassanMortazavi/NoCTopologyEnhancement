import math
from numpy import matrix
from datetime import datetime
import threading

class Topology:
    global_x_dim = 0
    global_y_dim = 0
    local_x_dim = 0
    local_y_dim = 0
    node_hub_connection_list = []
    hub_reliability = 0
    radio_unit_area = 0
    hub_port_unit_area = 0

    def __init__(self, global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list, hub_reliability,
                 radio_unit_area, hub_port_unit_area):
        self.set_new_config(global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list,
                            hub_reliability, radio_unit_area, hub_port_unit_area)

    # ok
    def set_new_config(self, global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list,
                       hub_reliability, radio_unit_area, hub_port_unit_area):
        if global_x_dim == 0 or global_y_dim == 0 or local_x_dim == 0 or local_y_dim == 0 or global_x_dim < local_x_dim or global_y_dim < local_y_dim or global_x_dim % local_x_dim != 0 or global_y_dim % local_y_dim != 0:
            return 0

        if len(node_hub_connection_list) != global_x_dim * global_y_dim:
            return 0
        if hub_reliability < 0 or hub_reliability > 1:
            return 0
        for node_hub_connection in node_hub_connection_list:
            if node_hub_connection < 0 or node_hub_connection > 1:
                return 0
        if radio_unit_area < 0 or hub_port_unit_area < 0:
            return 0
        self.global_x_dim = global_x_dim
        self.global_y_dim = global_y_dim
        self.local_x_dim = local_x_dim
        self.local_y_dim = local_y_dim
        self.node_hub_connection_list = node_hub_connection_list
        self.hub_reliability = hub_reliability
        self.radio_unit_area = radio_unit_area
        self.hub_port_unit_area = hub_port_unit_area
        return 1

    def hub_to_hub_distance(self):
        result = 0
        total_hub_number = self.get_total_hub_number()
        if total_hub_number < 1:
            return 1

        for i in range(0, total_hub_number):
            result += i + 1
        result = result / total_hub_number
        return result

    # ok
    def is_node_validate_on_network(self, node_address):
        if node_address < 0 or node_address >= self.global_x_dim * self.global_y_dim:
            return 0
        return 1

    # ok
    def is_subnet_validate_on_network(self, subnet_address):
        if subnet_address < 0 or subnet_address >= (self.global_x_dim / self.local_x_dim) * (
                    self.global_y_dim / self.local_y_dim):
            return 0
        return 1

    def get_total_subnet_number(self):
        return int((self.global_x_dim * self.global_y_dim) / (self.local_x_dim * self.local_y_dim))

    def get_total_hub_number(self):
        result = 0
        for i in range(0, self.get_total_subnet_number()):
            if len(self.get_subnet_node_hub_connection_list(i)) > 0:
                result += 1
        return result

    # ok
    def neighbor_subnet_list(self, subnet_address):
        result = []
        if subnet_address >= self.get_total_subnet_number():
            return result
        subnet_x_dim = int(self.global_x_dim / self.local_x_dim)
        subnet_y_dim = int(self.global_y_dim / self.local_y_dim)
        if subnet_address % subnet_x_dim != subnet_x_dim - 1:
            if len(self.get_subnet_node_hub_connection_list(subnet_address + 1)) > 0:
                result.append(subnet_address + 1)
        if subnet_address % subnet_x_dim != 0:
            if len(self.get_subnet_node_hub_connection_list(subnet_address - 1)) > 0:
                result.append(subnet_address - 1)
        if subnet_address < (subnet_x_dim * subnet_y_dim) - subnet_x_dim:
            if len(self.get_subnet_node_hub_connection_list(subnet_address + subnet_x_dim)) > 0:
                result.append(subnet_address + subnet_x_dim)
        if subnet_address >= subnet_x_dim:
            if len(self.get_subnet_node_hub_connection_list(subnet_address - subnet_x_dim)) > 0:
                result.append(subnet_address - subnet_x_dim)
        return result

    # ok
    def get_subnet_address(self, node_address):
        if self.is_node_validate_on_network(node_address) == 0:
            return -1
        subnet_x_cord = int(node_address % self.global_x_dim / self.local_x_dim)
        subnet_y_cord = int(int(node_address / self.global_x_dim) / self.local_y_dim)
        return int(subnet_y_cord * (self.global_x_dim / self.local_x_dim) + subnet_x_cord)

    def get_subnet_nodes_list(self, subnet_address):
        result = []
        if subnet_address >= self.get_total_subnet_number():
            return result
        subnet_x_dim = int(self.global_x_dim / self.local_x_dim)
        subnet_x_cord = subnet_address % subnet_x_dim
        subnet_y_cord = int(subnet_address / subnet_x_dim)
        for j in range(subnet_y_cord * self.local_y_dim, subnet_y_cord * self.local_y_dim + self.local_y_dim):
            for i in range(subnet_x_cord * self.local_x_dim, subnet_x_cord * self.local_x_dim + self.local_x_dim):
                result.append(i + j * self.global_x_dim)
        return result

    # ok
    def get_mesh_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1
        x_dis = abs(i_node % self.global_x_dim - j_node % self.global_x_dim)
        y_dis = abs(int(i_node / self.global_x_dim) - int(j_node / self.global_x_dim))
        return x_dis + y_dis

    # ok
    def get_subnet_node_hub_connection_list(self, subnet_address):
        intra_subnet_node_hub_connection_list = []
        if subnet_address >= self.get_total_subnet_number():
            return intra_subnet_node_hub_connection_list
        for i in self.get_subnet_nodes_list(subnet_address):
            if self.node_hub_connection_list[i] == 1:
                intra_subnet_node_hub_connection_list.append(i)
        return intra_subnet_node_hub_connection_list

    """
        return nearest intra subnet connected to hub node distance
        if dont have any node connected to hub in subnet return -1
    """

    # ok
    def get_to_hub_xy_distance(self, node_address, hub_subnet_address):
        if self.is_node_validate_on_network(node_address) == 0:
            return -1
        if self.is_subnet_validate_on_network(hub_subnet_address) == 0:
            return -1
        subnet_connected_to_hub_nodes = self.get_subnet_node_hub_connection_list(hub_subnet_address)

        if len(subnet_connected_to_hub_nodes) == 0:
            return -1
        result = self.global_x_dim * self.global_y_dim
        for node_hub_connection in subnet_connected_to_hub_nodes:
            temp_dis = self.get_mesh_distance(node_address, node_hub_connection)
            if temp_dis < result:
                result = temp_dis
        return result + 1

    # ok
    def calculate_distance_at_hub_reliability(self, is_src_hub_exist, is_des_hub_exist, src_spare_hubs, des_spare_hubs,
                                              fault_free_hubs_distance,
                                              faulty_src_distance, faulty_des_distance,
                                              faulty_src_and_des_distance, xy_distance):
        r = self.hub_reliability
        f = 1 - self.hub_reliability

        rs = r
        if not is_src_hub_exist:
            rs = 0
        rd = r
        if not is_des_hub_exist:
            rd = 0
        fs = 1 - rs
        fd = 1 - rd

        p_fault_free = rs * rd
        p_faulty_src_subnet = fs * rd * (1 - math.pow(f, src_spare_hubs))
        p_faulty_des_subnet = rs * fd * (1 - math.pow(f, des_spare_hubs))
        p_faulty_src_and_des_subnet = fs * fd * (1 - math.pow(f, src_spare_hubs)) * (1 - math.pow(f, des_spare_hubs))
        p_go_mesh = 1 - (p_fault_free + p_faulty_src_subnet + p_faulty_des_subnet + p_faulty_src_and_des_subnet)

        fault_free_distance = p_fault_free * fault_free_hubs_distance
        faulty_src_subnet_distance = p_faulty_src_subnet * faulty_src_distance
        faulty_des_subnet_distance = p_faulty_des_subnet * faulty_des_distance
        faulty_src_and_des_subnet_distance = p_faulty_src_and_des_subnet * faulty_src_and_des_distance
        mesh_distance = p_go_mesh * xy_distance
        return fault_free_distance + faulty_src_subnet_distance + faulty_des_subnet_distance + faulty_src_and_des_subnet_distance + mesh_distance

    # ok
    def get_fault_free_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)

        to_src_hub_distance = self.get_to_hub_xy_distance(i_node, i_node_subnet_address)
        to_des_hub_distance = self.get_to_hub_xy_distance(j_node, j_node_subnet_address)
        if to_src_hub_distance == -1 or to_des_hub_distance == -1:
            return self.global_x_dim * self.global_y_dim
        if i_node_subnet_address == j_node_subnet_address:
            return to_src_hub_distance + to_des_hub_distance
        return to_src_hub_distance + to_des_hub_distance + self.hub_to_hub_distance()

    def get_faulty_src_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)

        to_des_hub_distance = self.get_to_hub_xy_distance(j_node, j_node_subnet_address)
        src_neighbor_subnet_list = self.neighbor_subnet_list(i_node_subnet_address)
        if len(src_neighbor_subnet_list) == 0 or to_des_hub_distance == -1:
            return self.global_x_dim * self.global_y_dim

        to_src_hub_distance = self.global_x_dim * self.global_y_dim

        for src_neighbor_subnet in src_neighbor_subnet_list:
            temp = self.get_to_hub_xy_distance(i_node, src_neighbor_subnet)
            if temp > 0:
                to_src_hub_distance = temp
                i_node_subnet_address = src_neighbor_subnet
                break

        if i_node_subnet_address == j_node_subnet_address:
            return to_src_hub_distance + to_des_hub_distance
        return to_src_hub_distance + to_des_hub_distance + self.hub_to_hub_distance()

    def get_faulty_des_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)

        to_src_hub_distance = self.get_to_hub_xy_distance(i_node, i_node_subnet_address)
        des_neighbor_subnet_list = self.neighbor_subnet_list(j_node_subnet_address)
        if len(des_neighbor_subnet_list) == 0 or to_src_hub_distance == -1:
            return self.global_x_dim * self.global_y_dim

        to_des_hub_distance = self.global_x_dim * self.global_y_dim

        for des_neighbor_subnet in des_neighbor_subnet_list:
            temp = self.get_to_hub_xy_distance(j_node, des_neighbor_subnet)
            if temp > 0:
                to_des_hub_distance = temp
                j_node_subnet_address = des_neighbor_subnet
                break

        if i_node_subnet_address == j_node_subnet_address:
            return to_src_hub_distance + to_des_hub_distance
        return to_src_hub_distance + to_des_hub_distance + self.hub_to_hub_distance()

    def get_faulty_src_and_des_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)

        src_neighbor_subnet_list = self.neighbor_subnet_list(i_node_subnet_address)
        des_neighbor_subnet_list = self.neighbor_subnet_list(j_node_subnet_address)
        if len(des_neighbor_subnet_list) == 0 or len(des_neighbor_subnet_list) == 0:
            return self.global_x_dim * self.global_y_dim

        to_src_hub_distance = self.global_x_dim * self.global_y_dim

        for src_neighbor_subnet in src_neighbor_subnet_list:
            temp = self.get_to_hub_xy_distance(i_node, src_neighbor_subnet)
            if temp > 0:
                to_src_hub_distance = temp
                i_node_subnet_address = src_neighbor_subnet
                break

        to_des_hub_distance = self.global_x_dim * self.global_y_dim

        for des_neighbor_subnet in des_neighbor_subnet_list:
            temp = self.get_to_hub_xy_distance(j_node, des_neighbor_subnet)
            if temp > 0:
                to_des_hub_distance = temp
                j_node_subnet_address = des_neighbor_subnet
                break

        if i_node_subnet_address == j_node_subnet_address:
            return to_src_hub_distance + to_des_hub_distance
        return to_src_hub_distance + to_des_hub_distance + self.hub_to_hub_distance()

    def get_novel_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1
        if i_node == j_node:
            return 0
        xy_distance = self.get_mesh_distance(i_node, j_node)
        if xy_distance <= 2:
            return xy_distance
        fault_free_distance = self.get_fault_free_distance(i_node, j_node)
        faulty_src_distance = self.get_faulty_src_distance(i_node, j_node)
        faulty_des_distance = self.get_faulty_des_distance(i_node, j_node)
        faulty_src_and_des_distance = self.get_faulty_src_and_des_distance(i_node, j_node)

        src_subnet_address = self.get_subnet_address(i_node)
        des_subnet_address = self.get_subnet_address(j_node)
        src_subnet_neighbor_count = len(self.neighbor_subnet_list(src_subnet_address))
        des_subnet_neighbor_count = len(self.neighbor_subnet_list(des_subnet_address))
        is_src_hub_exist = len(self.get_subnet_node_hub_connection_list(src_subnet_address)) > 0
        is_des_hub_exist = len(self.get_subnet_node_hub_connection_list(des_subnet_address)) > 0

        tmp = self.calculate_distance_at_hub_reliability(is_src_hub_exist, is_des_hub_exist, src_subnet_neighbor_count,
                                                         des_subnet_neighbor_count, fault_free_distance,
                                                         faulty_src_distance, faulty_des_distance,
                                                         faulty_src_and_des_distance, xy_distance)
        if xy_distance < tmp:
            return xy_distance
        return tmp

    def get_topology_avg_distance(self):
        total_distance = 0
        x = 0

        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    total_distance += self.get_novel_distance(i, j)
                    x += 1
        return total_distance / x

    def get_topology_distance_matrix(self):
        w, h = self.global_x_dim * self.global_y_dim, self.global_x_dim * self.global_y_dim
        Matrix = [[0 for x in range(w)] for y in range(h)]
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    Matrix[i][j] = self.get_novel_distance(i, j)
        return Matrix

    def matrix_corrector(self, matrix, node_address):
        if self.is_node_validate_on_network(node_address) == 0:
            return -1
        tmp = self.get_total_hub_number()
        self.node_hub_connection_list[node_address] = 1 - self.node_hub_connection_list[node_address]
        tmp2 = self.get_total_hub_number()
        self.node_hub_connection_list[node_address] = 1 - self.node_hub_connection_list[node_address]
        if tmp != tmp2:
            return self.get_topology_distance_matrix()

        node_subnet_address = self.get_subnet_address(node_address)
        effected_subnets = [node_subnet_address]
        effected_subnets.extend(self.neighbor_subnet_list(node_subnet_address))
        effected_nodes = []
        for effected_subnet in effected_subnets:
            effected_nodes.extend(self.get_subnet_nodes_list(effected_subnet))
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    for k in effected_nodes:
                        if i == k or j == k:
                            matrix[i][j] = self.get_novel_distance(i, j)
                            break
        return matrix

    def get_topology_avg_distance_via_matrix(self, matrix):
        total_distance = 0
        x = 0
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    total_distance += matrix[i][j]
                    x += 1
        return total_distance / x

    def get_topology_maximum_avg_distance(self):
        total_distance = 0
        x = 0
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    total_distance += self.get_mesh_distance(i, j)
                    x += 1
        return total_distance / x

    def get_total_hub_area_overhead(self):
        hub_connection_number = 0
        for hub_connection in self.node_hub_connection_list:
            if hub_connection:
                hub_connection_number += 1
        hub_ports_total_area = hub_connection_number * self.hub_port_unit_area
        total_subnets_have_radio = 0
        for subnet in range(0, self.get_total_subnet_number()):
            for node in self.get_subnet_nodes_list(subnet):
                if self.node_hub_connection_list[node]:
                    total_subnets_have_radio += 1
                    break
        radios_total_area = total_subnets_have_radio * self.radio_unit_area
        return hub_ports_total_area + radios_total_area

    def get_maximum_total_hub_area_overhead(self):
        hub_connection_number = self.global_x_dim * self.global_y_dim
        hub_ports_total_area = hub_connection_number * self.hub_port_unit_area
        total_subnets_have_radio = self.get_total_subnet_number()
        radios_total_area = total_subnets_have_radio * self.radio_unit_area
        return hub_ports_total_area + radios_total_area

    def cal_cost_function(self, alpha):
        if alpha < 0 or alpha > 1:
            return -1
        a = self.get_topology_avg_distance()
        b = self.get_topology_maximum_avg_distance()
        c = self.get_total_hub_area_overhead()
        d = self.get_maximum_total_hub_area_overhead()

        avg_distance_ratio = a / b
        total_hub_area_overhead_ratio = c / d
        return (alpha * avg_distance_ratio) + ((1 - alpha) * total_hub_area_overhead_ratio)

    def fast_cal_cost_function_via_matrix(self, alpha, matrix):
        if alpha < 0 or alpha > 1:
            return -1
        a = self.get_topology_avg_distance_via_matrix(matrix)
        b = self.get_topology_maximum_avg_distance()
        c = self.get_total_hub_area_overhead()
        d = self.get_maximum_total_hub_area_overhead()

        avg_distance_ratio = a / b
        total_hub_area_overhead_ratio = c / d
        return (alpha * avg_distance_ratio) + ((1 - alpha) * total_hub_area_overhead_ratio)

    def pairs_props(self, i_node, j_node):
        fault_free_distance = self.get_fault_free_distance(i_node, j_node)
        faulty_src_distance = self.get_faulty_src_distance(i_node, j_node)
        faulty_des_distance = self.get_faulty_des_distance(i_node, j_node)
        faulty_src_and_des_distance = self.get_faulty_src_and_des_distance(i_node, j_node)
        xy_distance = self.get_mesh_distance(i_node,j_node)

        src_subnet_address = self.get_subnet_address(i_node)
        des_subnet_address = self.get_subnet_address(j_node)
        src_subnet_neighbor_count = len(self.neighbor_subnet_list(src_subnet_address))
        des_subnet_neighbor_count = len(self.neighbor_subnet_list(des_subnet_address))
        is_src_hub_exist = len(self.get_subnet_node_hub_connection_list(src_subnet_address)) > 0
        is_des_hub_exist = len(self.get_subnet_node_hub_connection_list(des_subnet_address)) > 0

        return {'is_src_hub_exist': is_src_hub_exist, 'is_des_hub_exist': is_des_hub_exist,
                'src_subnet_neighbor_count': src_subnet_neighbor_count,
                'des_subnet_neighbor_count': des_subnet_neighbor_count,
                'fault_free_distance': fault_free_distance, 'faulty_src_distance': faulty_src_distance,
                'faulty_des_distance': faulty_des_distance, 'faulty_src_and_des_distance': faulty_src_and_des_distance, 'xy_distance':xy_distance}

    def topology_props(self):
        w, h = self.global_x_dim * self.global_y_dim, self.global_x_dim * self.global_y_dim
        Matrix = [[0 for x in range(w)] for y in range(h)]
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    Matrix[i][j] = self.pairs_props(i, j)
        return Matrix

    def topology_average_distance_by_props_matrix(self, matrix):
        total_distance = 0
        x = 0
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    tmp = matrix[i][j]
                    total_distance += self.calculate_distance_at_hub_reliability(tmp['is_src_hub_exist'], tmp['is_des_hub_exist'], tmp['src_subnet_neighbor_count'],
                                                         tmp['des_subnet_neighbor_count'], tmp['fault_free_distance'],
                                                         tmp['faulty_src_distance'], tmp['faulty_des_distance'],
                                                         tmp['faulty_src_and_des_distance'], tmp['xy_distance'])
                    x += 1
        return total_distance / x

    def robustness_check(self):
        self.hub_reliability = 1.0
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))

        self.hub_reliability -= 0.1
        print("hub_reliability= " + str(self.hub_reliability) + " topology_avg_distance= " + str(
            self.get_topology_avg_distance()))
