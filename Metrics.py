from DataType import *
from Agent import *
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

def Power(server):
    """
    Return the total power
    """
    return Power_Static(server) + Power_Dynamic(server)

def Electricity_Price(t,power):
    """
    This function is the electricity bill parameter
    """
    pass


def Cost_Total(agent):
    """
    Calculate the global power cost at this time
    """
    farms = agent.farms
    cost = 0
    for farm in farms:
        for server in farm.servers:
            pow_ttl = Power(server)
            cost += Electricity_Price( time.time() , pow_ttl )
    return cost

    
def CPU_Total(agent):
    farms = agent.farms
    cpu = 0
    for farm in farms:
        for ser in farm.servers:
            ser.Update()
            cpu += ser.Current_CPU
    return cpu

def Reward(lay,Ser):
    """
    Reward function for DQN
    """
    Ur = Ser.Ur
    pri = Electricity_Price( time.time() ,powerPower_Total(Ser))

    if lay == 1:
        if Ur >= 0 and Ur <= 0.45:
            return 1
        elif Ur > 0.5 :
            return -2
        else:
            return -1
    elif lay == 2:
        if Ur >= 0.2 and Ur < 0.8:
            return Ur 
        elif Ur > 1:
            return -2
        else:
            return -1
    elif lay == 3:
        if Ur > 1:
            return -1
        elif pri < 0.3:
            return - pri 
        else:
            return - 4 * pri 
    else:
        if Ur > 1:
            return -2
        elif Ur > 0.8 or Ur < 0.2:
            return -1
        elif Ur > 0.6 and Ur <= 0.8:
            return 2
        else:
            return 1

def Power_Total(agent):
    """
    Calculate the total power
    """
    farms = agent.farms
    pow_ttl = 0
    for farm in farms:
        for server in farm.servers:
            pow_ttl += Power(server)

    return pow_ttl

def Energy_Cost_Efficiency(ser):
    """
    Calculate the Energy Cost Efficiency(ECE) 
    """
    return Cost_Total(agent) / Power_Total(agent)

        