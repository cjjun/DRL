import numpy as np 
import Agent

"""
Machine event:
    1. timestamp
    2. machine ID
    3. event type
        ADD (0): A machine became available to the cluster - all machines in the trace will have an ADD event.
        REMOVE (1): A machine was removed from the cluster. Removals can occur due to failures or maintenance.
        UPDATE (2): A machine available to the cluster had its available resources changed.
    4. platform ID
        Two machines with the same platform ID may have substantially different clock rates, memory speeds, core counts, etc.
    5. capacity: CPU
    6. capacity: memory
"""

"""
Machine attributes table:
    1. timestamp
    2. machine ID
    3. attribute name: an opaque string
    4. attribute value: either an opaque string or an integer
    5. attribute deleted: a boolean indicating whether the attribute was deleted
"""
def Load_Machine():
    with open('clusterdata-2011-2/machine_attributes/part-00000-of-00001.csv') as f:
        # timestamp = []
        # machineID = []
        # attr_name = []
        # attr_val = []
        # attr_dele = []
        cnt = 0
        while True:
            try:
                line = f.readline()
                line = line[:-1].split(',')
                timestamp, machineID, attr_name, attr_val, attr_dele = line
                while cnt < 10:
                    print(timestamp)
                    cnt += 1
            except:
                break
"""
Job events table
    1. timestamp
    2. missing info
    3. job ID
    4. event type
    5. user name
    6. scheduling class
    7. job name:  base64-encoded strings
    8. logical job name
"""
def Load_Job():
    with open('clusterdata-2011-2/machine_attributes/part-00000-of-00001.csv') as f:
        # cnt = 0
        while True:
            try:
                line = f.readline()
                line = line[:-1].split(',')
                timestamp, machineID, attr_name, attr_val, attr_dele = line
                # while cnt < 10:
                #     print(timestamp)
                #     cnt += 1
            except:
                break
"""
Task events table
    1. timestamp
    2. missing info
    3. job ID
    4. task index - within the job
    5. machine ID
    6. event type
    7. user name
    8. scheduling class
    9. priority
    10. resource request for CPU cores
    11. resource request for RAM
    12. resource request for local disk space
    13. different-machine constraint
"""
def Load_Task_Event():
    with open('clusterdata-2011-2/task_events/part-00000-of-00500.csv') as f:
        cnt = 0
        while True:
            try:
                line = f.readline()
                line = line[:-1].split(',')
                # timestamp, machineID, attr_name, attr_val, attr_dele = line
                # while cnt < 10:
                #     print(timestamp)
                #     cnt += 1
            except:
                break

"""
Task constraints table 
    1. timestamp
    2. job ID
    3. task index
    4. attribute name -- corresponds to machine attribute table
    5. attribute value -- either an opaque string or an integer or the empty string
    6. comparison operator
"""
def Load_Task_Constraint():
    with open('clusterdata-2011-2/task_constraints/part-00000-of-00500.csv') as f:
        cnt = 0
        while True:
            try:
                line = f.readline()
                line = line[:-1].split(',')
            except:
                break

"""
Task resource usage table
    1. start time of the measurement period
    2. end time of the measurement period
    3. job ID
    4. task index
    5. machine ID
    6. mean CPU usage rate
    7. canonical memory usage
    8. assigned memory usage
    9. unmapped page cache memory usage
    10.total page cache memory usage
    11. maximum memory usage
    12. mean disk I/O time
    13. mean local disk space used
    14. maximum CPU usage
    15. maximum disk IO time
    16. cycles per instruction (CPI)
    17. memory accesses per instruction (MAI)
    18. sample portion
    19. aggregation type (1 if maximums from subcontainers were summed)
    20. sampled CPU usage: mean CPU usage during a random 1s sample in the
    measurement period
"""

def Load_Task_Resource():
    with open('clusterdata-2011-2/task_usage/part-00000-of-00500.csv') as f:
        # cnt = 0
        while True:
            try:
                line = f.readline()
                line = line[:-1].split(',')
            except:
                break

if __name__ == '__main__':
    Load_Machine()