"""
Original data that read from  CSV
"""

Global_Farms = []
Global_Servers = []
Global_VMs = []
Global_Jobs = []
Global_Tasks = []

class MachineAttribute():
    def __init__(self):
        self.Timestamp = None
        self.MachineId = None
        self.Attribute_Name = None
        self.Attribute_Value = None 
        self.Attribute_Deleted = None

class MachineEvent():
    def __init__():
        self.Timestamp = None
        self.MachineId = None
        self.Type = None
        self.PlatformId = None
        self.Capacity_CPU = None
        self.Capacity_Memory = None

class JobEvent():
    def __init__(self):
        self.Timestamp = None
        self.Missing_Info = None 
        self.JobId = None 
        self.Type = None 
        self.Username = None 
        self.ScheduleClass = None 
        self.JobName = None 
        self.LogicJobName = None

class TaskEvent():
    def __init__(self):
        self.Timestamp = None
        self.MissingInfo = None
        self.JobId = None
        self.TaskId_in_job = None
        self.MachineId = None 
        self.Type = None
        self.Username = None
        self.ScheduleClass = None
        self.Priority = None
        self.Request_CPU_cores = None
        self.Request_RAM = None
        self.Request_local_disk_space = None
        self.Machine_Constraint = None

class TaskConstraint():
    def __init__(self):
        self.Timestamp = None
        self.JobId = None
        self.TaskId = None
        self.Attribute_Name = None
        self.Attribute_Value = None 
        self.Operator = None

class TaskUsage():
    def __init__(self): 
        self.StartTime = None
        self.Endtime = None
        self.JobId = None
        self.TaskId = None
        self.MachineId = None 
        self.Mean_CPU_usage_rate = None
        self.Canonical_memory_usage = None
        self.Assigned_memory_usage = None
        self.Unmapped_page_cache_memory_usage = None
        self.Total_page_cache_memory_usage = None
        self.Maximum_memory_usage = None
        self.Mean_disk_IO_time = None
        self.Mean_local_disk_space_used = None
        self.Maximum_CPU_usage = None
        self.Maximum_disk_IO_time = None
        self.Cycles_per_instruction = None
        self.Memory_accesses_per_instruction = None
        self.Sample_portion = None

"""
Model classes description

1. Parent pointer
2. Child lists

3. out_edges = [] (tuple like (edge_id,edge_weight) )
4. in_edges = []

5. Personal Permanent INFO (e.g. ID, TYPE, CPU)
6. Personal temporary INFO ( which requires update from child)

7. Whether it has been initially runned from childs
7. ShouldUpdate (0: not update, 1:update)
8. Increment that should be updated ( This avoid point revision to traverse all childs )
"""

TASK_STATUS_WAITING = 0
TASK_STATUS_SUSPENDED = 1
TASK_STATUS_RUNNING = 2 
TASK_STATUS_FINISHED = 3

class Farm:
    def __init__(self):
        self.super = []     # A list reference which includes all farms
        self.servers = []

        self.outedges = []
        self.inedges = []

        self.ID = [] 

class Server():
    def __init__(self):
        self.farm = None 
        self.VMs = []

        self.outedges = []
        self.inedges = []

        self.ID = []

        self.Capacity_CPU = None
        self.Capacity_Memory = None
        self.Dynamic_Power_Parameters = (1,1)

        self.Current_CPU = None 
        self.Current_Memory = None 

        self.Ur_opt = None 
        self.Ur = None

        self.has_initialized = 0
        self.should_update = 0
        self.incre = (0,0)

    def Update():
        if not self.has_initialized:
            self.Get_from_child() 
            self.has_initialized = 1
        else:
            self.Update_from_child()

        self.Update_Unknown_Info()

    def Get_from_child(self):
        self.Current_CPU = 0
        self.Current_Memory = 0

        for vm in self.VMs:
            self.Current_CPU += vm.Current_CPU
            self.Current_Memory += vm.Current_Memory

    def Update_from_child(self):
        if self.should_update == 1:
            self.should_update = 0
            self.Current_CPU += self.incre[0]
            self.Current_Memory += self.incre[1]
            self.incre = 0,0

            self.Update_Unknown_Info()


    def Update_Unknown_Info(self):
        self.Ur = self.Current_CPU / self.Capacity_CPU

class VM():
    def __init__(self):
        self.server = None
        self.jobs = []

        self.outedges = []
        self.inedges = []

        self.type = None
        self.ID = None

        self.Capacity_CPU = None
        self.Capacity_Memory = None

        self.Current_CPU = None 
        self.Current_Memory = None 

        self.has_initialized = 0
        self.should_update = 0
        self.incre = (0,0)

    def Update():
        if not self.has_initialized:
            self.Get_from_child() 
            self.has_initialized = 1
        else:
            self.Update_from_child()


    def Get_from_child(self):
        self.Current_CPU = 0
        self.Current_Memory = 0

        for job in self.jobs:
            self.Current_CPU += job.Current_CPU
            self.Current_Memory += job.Current_Memory

    def Update_from_child(self):
        if not self.server and self.should_update == 1:
            self.should_update = 0

            # Update from child
            self.Current_CPU += self.incre[0]
            self.Current_Memory += self.incre[1]

            # Push_up
            self.server.incre[0] += self.incre[0]
            self.server.incre[1] += self.incre[1]
            self.server.should_update = 1
            self.incre = (0,0)

class Job():
    def __init__(self):
        self.VM = None 
        self.tasks = []
    
        self.ID = None

        self.Request_CPU = None 
        self.Request_Memory = None 

        self.should_update = 0

    def Update_from_child(self):
        if not self.VM and self.should_update == 1:
            self.should_update = 0
            # self.VM.should_update = 1
            old = (self.Request_CPU,self.Request_Memory)

            self.Request_CPU = 0
            self.Request_Memory = 0

            for task in self.tasks:
                if task.status == TASK_STATUS_RUNNING:
                    self.Request_CPU += task.Request_CPU
                    self.Request_Memory += task.Request_Memory

            self.VM.incre[0] += self.Request_CPU - old[0]
            self.VM.incre[1] += self.Request_Memory - old[1]
            self.VM.should_update = 1
            

class Task():
    def __init__(self):
        self.job = None 
        
        # Tuple in the form (id,data_bandwidth)
        self.outedges = []
        self.inedges = []

        self.ID = None
        self.status = None 

        self.Request_CPU = None 
        self.Request_Memory = None 
        self.VM_type = None 

        # priority
        self.Prr = None
        self.DDL = None
        