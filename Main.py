from Topology import Topology

myTopology = Topology(16, 16, 4, 4, [0, 254], 1)


print(myTopology.get_xy_distance(0, 3))
print(myTopology.get_novel_distance_fault_free(0, 3))
print(myTopology.get_novel_distance_faulty_src(0, 3))
print(myTopology.get_novel_distance(0, 3))

print(myTopology.get_topology_avg_distance())