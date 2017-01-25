from SA import SA
from datetime import datetime



print("start ...")
before_run_time = datetime.now()

mySA = SA(256,0.9)

print("exec time = " + str(datetime.now() - before_run_time))
