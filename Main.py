from Topology import Topology
from datetime import datetime

myTopology = Topology(16, 16, 4, 4, [0, 4, 3, 2, 43, 53, 100, 254], 0.09)

print("start ...")
before_run_time = datetime.now()
print("topology average distance = " + str(myTopology.get_topology_avg_distance()))
print("exec time = " + str(datetime.now() - before_run_time))
