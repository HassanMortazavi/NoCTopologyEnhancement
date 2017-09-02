from Improver import Improver

myImprover = Improver(network_size=256, network_hub_reliability=0.9, radio_unit_area=100, hub_port_unit_area=60,
                      alpha=1)

myImprover.test()
