from DataType import *
from queue import Queue

class Agent():
    def __init__(self):
        self.status = []
        self.farms = []
        self.servers = []
        self.VMS = []
        self.tasks = []

        self.task_que = Queue() 
        self.history_que = Queue()

        self.Max_farm = 0

        self.Pointer = farms
        self.RR_index = 0


    def Load_relation(self):
        """
        Load the topological structure of the network. This includes identity info,
        the DAG structure, as well as the tree layer info.
        """
        pass 


    def Select_farm(self,id):
        """
        Select the farm with index = id. Namely, this index should be integer.

        Args: 
            id: an integer that can be used for farm index
        """
        assert( id <self.Max_farm )
        self.Pointer = self.farms[id]
    
    def Select_server(self,id,mode=None):
        """
        Select the server with index = id in the farm. Namely, this index should be integer.

        Args: 
            id: an integer that can be used for locally recognizing an server. Without further
            description, this is a local network id.
        """
        if mode == 'DIRECT':
            self.Pointer = id

        server_pointer = self.Pointer.servers
        assert( id < len( server_pointer ) )
        self.Pointer = self.Pointer[id]

    def Select_VM(self,id):
        """
        Select the Virtual Machine with index = id in the farm. Namely, this index should be integer.

        Args: 
            id: an integer that can be used for locally recognizing an VM. Without further
            description, this is a local network id.
        """
        VM_pointer = self.Pointer.VMs 
        assert( id < len( VM_pointer ) )
        self.Pointer = VM_pointer[id]
        self.Assign_task()
        

    def Start_task(self,task):
        VM = self.Pointer
        VM.tasks.append( task )
        task.VM = VM 
        task.Push_up()

    
    def Select_hour(self,h):
        """
        Select the task hour
        """
        task = self.VM.tasks[-1]
        task.Start_time ['hour'] = h
    
    def Select_minute(self,m):
        """
        Select the task minute
        """
        task = self.VM.tasks[-1]
        task.Start_time ['minu'] = m 
        
    def Get_Ser(self):
        ser = self.Pointer.server 
        ser.Update()
        return ser
    
    def Reset_pointer(self):
        """
        The select function must be use cascadingly, or error might happen. This function
        reset the traverse pointer to the root farms(i.e. the supernode at the beginning)
        """
        self.Pointer = self.farms

    def SAL(self,task,server):
        """
        Given task and self.RR index, decide if it's possible to be assigned.
        """

        # Step 1, test if server could satisfy constraint
        if task.Request_CPU + server.Current_CPU > server.Capacity_CPU or task.request_Memory + server.Current_Memory > server.Capacity_Memory:
            return False
        
        # Step 2, find out if any VM satisfies the type and resource constraint
        for vm in server.VMs:
            if vm.type == task.VM_type:
                if task.Request_CPU + vm.Current_CPU > vm.Capacity_CPU or task.Request_Memory + vm.Current_Memory > vm.Capacity_Memory:
                    return False
        return True

    def Round_robin(self,task):
        """
        Round robin selection

        Args:
            task: pointer of the task
        
        Returns: Pointer of the server, otherwise None
        """
        st = self.RR_index 
        length = len(self.servers)

        Success = False
        while (self.RR_index + i + 1 ) % length != st:
            server = self.servers[self.RR_index]
            if SAL(task,server):
                Success = True
                break 
            self.RR_index = (self.RR_index + 1) % length
            
        
        if Success:
            return self.servers[self.RR_index]
        else:
            return None

    def Get_Task(self):
        return task_que.get()
    
    def Recycle_Task(self,task):
        task_que.push(task)
