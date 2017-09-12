from Improver import Improver
from ReadConfigFile import read_config_file
myImprover = read_config_file("config.txt")

# myImprover.start()
myImprover.current_topology.robustness_check()


