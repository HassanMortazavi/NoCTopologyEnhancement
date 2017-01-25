import math


class Topology:
    global_x_dim = 0
    global_y_dim = 0
    local_x_dim = 0
    local_y_dim = 0
    node_hub_connection_list = []
    hub_reliability = 0

    def __init__(self, global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list, hub_reliability):
        self.set_new_config(global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list,
                            hub_reliability)

    # ok
    def set_new_config(self, global_x_dim, global_y_dim, local_x_dim, local_y_dim, node_hub_connection_list,
                       hub_reliability):
        if global_x_dim == 0 or global_y_dim == 0 or local_x_dim == 0 or local_y_dim == 0 or global_x_dim < local_x_dim or global_y_dim < local_y_dim or global_x_dim % local_x_dim != 0 or global_y_dim % local_y_dim != 0:
            return 0

        if len(node_hub_connection_list) > global_x_dim * global_y_dim:
            return 0
        if hub_reliability < 0 or hub_reliability > 1:
            return 0
        for node_hub_connection in node_hub_connection_list:
            if node_hub_connection < 0 or node_hub_connection >= global_x_dim * global_y_dim:
                return 0
        self.global_x_dim = global_x_dim
        self.global_y_dim = global_y_dim
        self.local_x_dim = local_x_dim
        self.local_y_dim = local_y_dim
        self.node_hub_connection_list = node_hub_connection_list
        self.hub_reliability = hub_reliability
        return 1

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

    # ok
    def neighbor_subnet_list(self, subnet_address):
        result = []
        subnet_x_dim = int(self.global_x_dim / self.local_x_dim)
        subnet_y_dim = int(self.global_y_dim / self.local_y_dim)
        if subnet_address % subnet_x_dim != subnet_x_dim - 1:
            result.append(subnet_address + 1)
        if subnet_address % subnet_x_dim != 0:
            result.append(subnet_address - 1)
        if subnet_address < (subnet_x_dim * subnet_y_dim) - subnet_x_dim:
            result.append(subnet_address + subnet_x_dim)
        if subnet_address >= subnet_x_dim:
            result.append(subnet_address - subnet_x_dim)
        return result

    # ok
    def get_subnet_address(self, node_address):
        if self.is_node_validate_on_network(node_address) == 0:
            return -1
        subnet_x_cord = int(node_address % self.global_x_dim / self.local_x_dim)
        subnet_y_cord = int(int(node_address / self.global_x_dim) / self.local_y_dim)
        return int(subnet_y_cord * (self.global_x_dim / self.local_x_dim) + subnet_x_cord)

    # ok
    def get_xy_distance(self, i_node, j_node):
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
        for node_hub_connection in self.node_hub_connection_list:
            if self.get_subnet_address(node_hub_connection) == subnet_address:
                intra_subnet_node_hub_connection_list.append(node_hub_connection)
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
        # todo: needs improvement
        subnet_connected_to_hub_nodes = self.get_subnet_node_hub_connection_list(hub_subnet_address)
        # endtodo
        if len(subnet_connected_to_hub_nodes) == 0:
            return -1
        result = self.global_x_dim * self.global_y_dim
        for node_hub_connection in subnet_connected_to_hub_nodes:
            temp_dis = self.get_xy_distance(node_address, node_hub_connection)
            if temp_dis < result:
                result = temp_dis
        return result + 1

    def calculate_distance_at_hub_reliability(self, fault_free_distance, faulty_src_distance, faulty_des_distance,
                                              faulty_src_and_des_distance, xy_distance, src_spare_hubs, des_spare_hubs):
        fault_free_distance = self.hub_reliability * self.hub_reliability * fault_free_distance
        faulty_src_subnet_distance = self.hub_reliability * (1 - self.hub_reliability) * (
            (1 - (math.pow(1 - self.hub_reliability, src_spare_hubs))) * faulty_src_distance + (
                (math.pow(1 - self.hub_reliability, src_spare_hubs)) * xy_distance))
        faulty_des_subnet_distance = (1 - self.hub_reliability) * self.hub_reliability * (
            (1 - (math.pow(1 - self.hub_reliability, des_spare_hubs))) * faulty_des_distance + (
                math.pow(1 - self.hub_reliability, des_spare_hubs)) * xy_distance)
        faulty_src_and_des_subnet_distance = (1 - self.hub_reliability) * (1 - self.hub_reliability) * (
            (1 - (math.pow(1 - self.hub_reliability, src_spare_hubs))) * (1 - (
                math.pow(1 - self.hub_reliability,
                         des_spare_hubs))) * faulty_src_and_des_distance + (
                1 - ((1 - (math.pow(1 - self.hub_reliability, src_spare_hubs))) * (
                    1 - (math.pow(1 - self.hub_reliability, des_spare_hubs))))) * xy_distance)
        return fault_free_distance + faulty_src_subnet_distance + faulty_des_subnet_distance + faulty_src_and_des_subnet_distance

    # ok
    def get_novel_distance_fault_free(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        xy_distance = self.get_xy_distance(i_node, j_node)
        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)
        src_subnet_set = [i_node_subnet_address]
        des_subnet_set = [j_node_subnet_address]

        src_subnet_set.extend(self.neighbor_subnet_list(i_node_subnet_address))
        des_subnet_set.extend(self.neighbor_subnet_list(j_node_subnet_address))
        src_to_hub = self.global_x_dim * self.global_y_dim
        src_hub_subnet_address = i_node_subnet_address
        for subnet in src_subnet_set:
            temp = self.get_to_hub_xy_distance(i_node, subnet)
            if 0 < temp < src_to_hub:
                src_to_hub = temp
                src_hub_subnet_address = subnet

        des_to_hub = self.global_x_dim * self.global_y_dim
        des_hub_subnet_address = j_node_subnet_address
        for subnet in des_subnet_set:
            temp = self.get_to_hub_xy_distance(j_node, subnet)
            if 0 < temp < des_to_hub:
                des_to_hub = temp
                des_hub_subnet_address = subnet

        distance = src_to_hub + des_to_hub
        if src_hub_subnet_address != des_hub_subnet_address:
            distance += 1  # 1= hub to hub(inter hub) hop
        if distance > xy_distance:
            distance = xy_distance
        return distance

    def get_novel_distance_faulty_src(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1
        xy_distance = self.get_xy_distance(i_node, j_node)
        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)
        src_subnet_set = []
        des_subnet_set = [j_node_subnet_address]
        src_subnet_set.extend(self.neighbor_subnet_list(i_node_subnet_address))
        des_subnet_set.extend(self.neighbor_subnet_list(j_node_subnet_address))
        src_to_hub = self.global_x_dim * self.global_y_dim
        src_hub_subnet_address = i_node_subnet_address
        for subnet in src_subnet_set:
            temp = self.get_to_hub_xy_distance(i_node, subnet)
            if 0 < temp < src_to_hub:
                src_to_hub = temp
                src_hub_subnet_address = subnet

        des_to_hub = self.global_x_dim * self.global_y_dim
        des_hub_subnet_address = j_node_subnet_address
        for subnet in des_subnet_set:
            temp = self.get_to_hub_xy_distance(j_node, subnet)
            if 0 < temp < des_to_hub:
                des_to_hub = temp
                des_hub_subnet_address = subnet

        distance = src_to_hub + des_to_hub
        if src_hub_subnet_address != des_hub_subnet_address:
            distance += 1  # 1= hub to hub(inter hub) hop
        if distance > xy_distance:
            distance = xy_distance
        return distance

    def get_novel_distance_faulty_des(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1
        xy_distance = self.get_xy_distance(i_node, j_node)
        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)
        src_subnet_set = [i_node_subnet_address]
        des_subnet_set = []
        src_subnet_set.extend(self.neighbor_subnet_list(i_node_subnet_address))
        des_subnet_set.extend(self.neighbor_subnet_list(j_node_subnet_address))
        src_to_hub = self.global_x_dim * self.global_y_dim
        src_hub_subnet_address = i_node_subnet_address
        for subnet in src_subnet_set:
            temp = self.get_to_hub_xy_distance(i_node, subnet)
            if 0 < temp < src_to_hub:
                src_to_hub = temp
                src_hub_subnet_address = subnet

        des_to_hub = self.global_x_dim * self.global_y_dim
        des_hub_subnet_address = j_node_subnet_address
        for subnet in des_subnet_set:
            temp = self.get_to_hub_xy_distance(j_node, subnet)
            if 0 < temp < des_to_hub:
                des_to_hub = temp
                des_hub_subnet_address = subnet

        distance = src_to_hub + des_to_hub
        if src_hub_subnet_address != des_hub_subnet_address:
            distance += 1  # 1= hub to hub(inter hub) hop
        if distance > xy_distance:
            distance = xy_distance
        return distance

    def get_novel_distance_faulty_src_and_des(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1
        xy_distance = self.get_xy_distance(i_node, j_node)
        i_node_subnet_address = self.get_subnet_address(i_node)
        j_node_subnet_address = self.get_subnet_address(j_node)
        src_subnet_set = []
        des_subnet_set = []
        src_subnet_set.extend(self.neighbor_subnet_list(i_node_subnet_address))
        des_subnet_set.extend(self.neighbor_subnet_list(j_node_subnet_address))
        src_to_hub = self.global_x_dim * self.global_y_dim
        src_hub_subnet_address = i_node_subnet_address
        for subnet in src_subnet_set:
            temp = self.get_to_hub_xy_distance(i_node, subnet)
            if 0 < temp < src_to_hub:
                src_to_hub = temp
                src_hub_subnet_address = subnet

        des_to_hub = self.global_x_dim * self.global_y_dim
        des_hub_subnet_address = j_node_subnet_address
        for subnet in des_subnet_set:
            temp = self.get_to_hub_xy_distance(j_node, subnet)
            if 0 < temp < des_to_hub:
                des_to_hub = temp
                des_hub_subnet_address = subnet

        distance = src_to_hub + des_to_hub
        if src_hub_subnet_address != des_hub_subnet_address:
            distance += 1  # 1= hub to hub(inter hub) distance
        if distance > xy_distance:
            distance = xy_distance
        return distance

    def get_novel_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        src_subnet_neighbor_count = len(self.neighbor_subnet_list(self.get_subnet_address(i_node)))
        des_subnet_neighbor_count = len(self.neighbor_subnet_list(self.get_subnet_address(j_node)))
        xy_distance = self.get_xy_distance(i_node, j_node)
        novel_distance_fault_free = self.get_novel_distance_fault_free(i_node, j_node)
        novel_distance_faulty_src = self.get_novel_distance_faulty_src(i_node, j_node)
        novel_distance_faulty_des = self.get_novel_distance_faulty_des(i_node, j_node)
        novel_distance_faulty_src_and_des = self.get_novel_distance_faulty_src_and_des(i_node, j_node)

        return self.calculate_distance_at_hub_reliability(novel_distance_fault_free, novel_distance_faulty_src,
                                                          novel_distance_faulty_des, novel_distance_faulty_src_and_des,
                                                          xy_distance, src_subnet_neighbor_count,
                                                          des_subnet_neighbor_count)

    def get_fast_novel_distance(self, i_node, j_node):
        if self.is_node_validate_on_network(i_node) == 0:
            return -1
        if self.is_node_validate_on_network(j_node) == 0:
            return -1

        i_node_subnet_address = self.get_subnet_address(i_node)
        src_neighbor_subnets = self.neighbor_subnet_list(i_node_subnet_address)
        src_subnet_neighbor_count = len(src_neighbor_subnets)

        j_node_subnet_address = self.get_subnet_address(j_node)
        des_neighbor_subnets = self.neighbor_subnet_list(j_node_subnet_address)
        des_subnet_neighbor_count = len(des_neighbor_subnets)

        xy_distance = self.get_xy_distance(i_node, j_node)

        i_node_to_main_hub_distance = self.global_x_dim * self.global_y_dim
        src_spare_subnet = 0
        i_node_to_spare_hub_distance = self.global_x_dim * self.global_y_dim

        j_node_to_main_hub_distance = self.global_x_dim * self.global_y_dim
        des_spare_subnet = 0
        j_node_to_spare_hub_distance = self.global_x_dim * self.global_y_dim

        temp = self.get_to_hub_xy_distance(i_node, i_node_subnet_address)
        if temp > 0:
            i_node_to_main_hub_distance = temp

        for subnet in src_neighbor_subnets:
            temp = self.get_to_hub_xy_distance(i_node, subnet)
            if temp > 0:
                i_node_to_spare_hub_distance = temp
                src_spare_subnet = subnet
                break

        temp = self.get_to_hub_xy_distance(j_node, j_node_subnet_address)
        if temp > 0:
            j_node_to_main_hub_distance = temp

        for subnet in des_neighbor_subnets:
            temp = self.get_to_hub_xy_distance(j_node, subnet)
            if temp > 0:
                j_node_to_spare_hub_distance = temp
                des_spare_subnet = subnet
                break

        main_src_main_des = i_node_to_main_hub_distance + j_node_to_main_hub_distance
        if i_node_subnet_address != j_node_subnet_address:
            main_src_main_des += 1

        spare_src_main_des = i_node_to_spare_hub_distance + j_node_to_main_hub_distance
        if src_spare_subnet != j_node_subnet_address:
            spare_src_main_des += 1

        main_src_spare_des = i_node_to_main_hub_distance + j_node_to_spare_hub_distance
        if i_node_subnet_address != des_spare_subnet:
            main_src_spare_des += 1

        spare_src_spare_des = i_node_to_spare_hub_distance + j_node_to_spare_hub_distance
        if src_spare_subnet != des_spare_subnet:
            spare_src_spare_des += 1

        novel_distance_fault_free = min(
            [main_src_main_des, spare_src_main_des, main_src_spare_des, spare_src_spare_des, xy_distance])

        novel_distance_faulty_src = min(
            [spare_src_main_des, spare_src_spare_des, xy_distance])

        novel_distance_faulty_des = min(
            [main_src_spare_des, spare_src_spare_des, xy_distance])

        novel_distance_faulty_src_and_des = min(
            [spare_src_spare_des, xy_distance])

        return self.calculate_distance_at_hub_reliability(novel_distance_fault_free, novel_distance_faulty_src,
                                                          novel_distance_faulty_des, novel_distance_faulty_src_and_des,
                                                          xy_distance, src_subnet_neighbor_count,
                                                          des_subnet_neighbor_count)

    def get_topology_avg_distance(self):
        total_distance = 0
        x = 0
        for i in range(0, self.global_x_dim * self.global_y_dim):
            for j in range(i, self.global_x_dim * self.global_y_dim):
                if i != j:
                    total_distance += self.get_fast_novel_distance(i, j)
                    x += 1
        return total_distance / x
