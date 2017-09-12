from Topology import Topology


def read_file(file_name):
    with open(file_name) as f:
        content = f.read()
    return content


def print_to_file(file_name, str):
    file = open(file_name, "a")
    file.write(str)
    file.close()


def save_topology(topology):
    open('result.txt', 'w').close()
    print_to_file('result.txt', "topology_avg_distance:")
    print_to_file('result.txt', str(topology.get_topology_avg_distance()))
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', "Number of total Hubs:")
    print_to_file('result.txt', str(topology.get_total_hub_number()))
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', "Subnet_x_dim_size:")
    print_to_file('result.txt', str(topology.local_x_dim))
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', "Subnet_y_dim_size:")
    print_to_file('result.txt', str(topology.local_y_dim))
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', '\n')
    print_to_file('result.txt', "Topology:")
    print_to_file('result.txt', '\n')
    for j in range(0, topology.global_y_dim):
        line = ""
        from_node = (topology.global_x_dim * topology.global_y_dim) - topology.global_x_dim
        to_node = (topology.global_x_dim * topology.global_y_dim)
        for i in range(from_node - (j * topology.global_x_dim), to_node - (j * topology.global_x_dim)):
            line += str(topology.node_hub_connection_list[i]) + " - "
        line = line[:-3]
        print_to_file('result.txt', line)
        print_to_file('result.txt', '\n')
        if j != topology.global_y_dim - 1:
            tmp = ""
            for i in range(0, topology.global_x_dim):
                tmp += "|   "
            tmp = tmp[:-3]
            print_to_file('result.txt', tmp)
            print_to_file('result.txt', '\n')
