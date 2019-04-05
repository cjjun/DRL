from DataType import *
import time

STATIC_THRESHOLD = 10
STATIC_DEFAULT_POWER = 100

Global_Current_Cost = 1
Current_Time = 0

def Get_Current_time():
    Current_Time = time.time()
    return Current_Time

def Power_Static(server):
    """
    Return the static power
    """
    server.Update()
    if server.Ur < STATIC_THRESHOLD:
        return 0
    else:
        return STATIC_DEFAULT_POWER

def Power_Dynamic(server):
    """
    Return the dynamic power
    """
    if server.Ur < server.Ur_opt:
        return server.Ur * server.Dynamic_Power_Parameters[0]
    else:
        return (server.Ur - server.Ur_opt)**2 * server.Dynamic_Power_Parameters[1] + 
        server.Ur_opt * server.Dynamic_Power_Parameters[0]

def Power_Total(server):
    """
    Return the total power
    """
    return Power_Static(server) + Power_Dynamic(server)

def Electricity_Price(t,power):
    """
    This function is the electricity bill parameter
    """
    pass


def Global_Cost():
    """
    Calculate the global power cost at this time
    """
    Global_Current_Cost = 0
    t = Get_Current_time()
    for server in Global_Servers:
        pow_ttl = Power_Total(server)
        Global_Current_Cost += Price(t,power)
    return Global_Current_Cost
    
def TotalCPU():


def Energy_Cost_Efficiency(ser):
"""
    Calculate the Energy Cost Efficiency(ECE) 
"""
    pass

        