from Topology import Topology
from datetime import datetime

def get_hub_connections_list(network_size):
    result = []
    for i in range(0,network_size):
        result.append(i%2)
    return result

myTopology = Topology(16, 16, 4, 4, get_hub_connections_list(256), 0.99)
print("start ...")
before_run_time = datetime.now()
print("topology average distance = " + str(myTopology.get_topology_avg_distance()))
print("exec time = " + str(datetime.now() - before_run_time))
