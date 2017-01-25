from Topology import Topology
from datetime import datetime

myTopology = Topology(16, 16, 4, 4, [0, 4, 254], 1)

print(myTopology.get_novel_distance_fault_free(0, 254))
print(myTopology.get_novel_distance_faulty_des(0, 254))

before_run_time = datetime.now()
print(myTopology.get_topology_avg_distance())
print(datetime.now() - before_run_time)
