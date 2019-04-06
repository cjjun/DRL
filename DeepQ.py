import numpy as np 
import tensorflow as tf 
from tensorflow.nn import relu
import Agent
import Metrics

global_params = None 
global_parameters = None 
global_terminal = None 
global_result_dict = None

REJECT = 0  

def Initialize_Parameters(params):
    """
    Clear the default graph setting.
    Initialize with four layer parameters e.g. params = [ [1,2,1],[1,3,1],[1,4,1],[1,5,1] ]
    layer 1:  Input: 1--->2---(Relu)---> 1:output
    ...
    layer 4:  Input: 1--->5---(Relu)---> 1:output
    
    Args:
        params: A list of four lists,each list includes information of network construction
    Return:
        parameters: A dictionary with key in format W_(layer_id)_(order_id),b_(layer_id)_(order_id).
            e.g.  W_1_1, the first W in network 1 in layer 1
        terminal: A dictionary with key X_(layer),Y_(layer), the input and output port for input and output
    """
    tf.reset_default_graph()
    
    layers = len(params)

    terminal = {}
    for i in range(layers):
        param = params[i]
        terminal[ "X"+str(i+1) ] = tf.placeholder('float32',shape = [param[0],1],name = 'Input'+str(i+1))
        terminal[ "Y"+str(i+1) ] = tf.placeholder('float32',shape = [ param[-1],1 ],name = 'Output'+str(i+1) )

    for l in range(layers):
        param = params[l]
        for i in range(1,len(param)):
            parameters[ "W"+str(l+1)+'_'+str(i) ] = tf.get_variable("W"+str(l+1)+'_'+str(i),shape = [ param[i],param[i-1] ],initializer = tf.contrib.layers.xavier_initializer())
            parameters[ "b"+str(l+1)+'_'+str(i) ] = tf.get_variable("b"+str(l+1)+'_'+str(i),shape= [ param[i] ,1],initializer=tf.zeros_initializer() )
    return parameters,terminal

def forward_propogation_sub_network(terminal,parameters,params):
    """
    Forward progogation for each sub-network. Must indicate network layer id.

    Args:
        terminal: A dictionary with key X_(layer),Y_(layer), the input and output port for input and output
        parameters: parameters: A dictionary with key in format W_(layer_id)_(order_id),b_(layer_id)_(order_id).
        params: Network configuration of all layer
    
    Returns:
        result_dict: A diction with key Z1,Z2,...,Z4 as output of each layer.
    """
    result_dict = {}
    for lay in range(len(params)):
        param = params[lay]
        n = len(param) - 1
        A = terminal["X"+str(lay+1)]

        for i in range(1,n):
            W = parameters[ "W"+str(lay+1)+'_'+str(i) ]
            b = parameters[ "b"+str(lay+1)+'_'+str(i) ]
            Z = tf.matmul(W,A) + b 
            A = relu(Z)

        W = parameters[ "W"+str(n)+'_'+str(i) ]
        b = parameters[ "b"+str(n)+'_'+str(i) ]
        Z = tf.matmul(W,A) + b
        cost = compute_cost(Z,terminal[Y+str(lay+1)])

        result_dict[ "Z"+str(lay+1) ] = Z
        result_dict[ "cost"+ +str(lay+1) ] = cost
   
    return result_dict

def compute_cost(Old_Q,next_Q):
    """ 
    Return L-2 norm between old Q value vector and next_Q value vector
    """
    return tf.reduce_sum( tf.square( Old_Q - next_Q ) )

def eipsilon_greedy(vector,episilon):
    
    assert( vector.shape[1] == 1 )

    p = np.random.random(1)
    if p[0] <= episilon:
        choice = np.random.randint(0,vec.shape[0],1)
    else:
        choice = np.argmax( vec, axis = 0 )
    return choice

def Train_model(agent,result_dict,terminal,episilon = 0.2):
    """
    Implement Deep Q Network forward propogation

    Args:
        terminal: A dictionary with key X_(layer),Y_(layer), the input and output port for input and output
        parameters: parameters: A dictionary with key in format W_(layer_id)_(order_id),b_(layer_id)_(order_id).
        params: Network configuration of all layer

        """
    X1,Y1 = terminal["X1"],terminal["Y1"]   
    X2,Y2 = terminal["X2"],terminal["Y2"]   
    X3,Y3 = terminal["X3"],terminal["Y3"]   
    X4,Y4 = terminal["X4"],terminal["Y4"]   

    Z1 = result_dict["Z1"]
    Z2 = result_dict["Z2"]
    Z3 = result_dict["Z3"]
    Z4 = result_dict["Z4"]

    cost1 = result_dict["cost1"]
    cost2 = result_dict["cost2"]
    cost3 = result_dict["cost3"]
    cost4 = result_dict["cost4"]

    optim1 = tf.train.AdamOptimizer(learning_rate).minimize(cost1)
    optim2 = tf.train.AdamOptimizer(learning_rate).minimize(cost2)
    optim3 = tf.train.AdamOptimizer(learning_rate).minimize(cost3)
    optim4 = tf.train.AdamOptimizer(learning_rate).minimize(cost4)

    agent = Agent()

    with tf.Session() as sess:
        sess.run( tf.global_variables_initializer() )

        task = agent.GetTask()

        # For layer 1, farm decision. If reject, do round_robin. If rejected once again,recycle task
        S1 = agent.state()
        Qout1 = sess.run( Z1, feed_dict={ X1:S1 } )
        Act1 = eipsilon_greedy( Qout1,episilon )

        if Act1 == REJECT:
            server = agent.Round_robin(task)
            if not server:
                agent.Recycle_Task(task)
            else:
                agent.Select_server(server,"DIRECT")
                continue 

        agent.Select_farm(Act1)
        new_S1 = agent.state(1)
        Qout1_new = sess.run( Z1, feed_dict={ X1:new_S1 } )

        # Layer 2, server selection
        S2 = agent.state(2)
        Qout2 = sess.run( Z2, feed_dict={ X2:S2 } )
        Act2 = eipsilon_greedy( Qout2,episilon )

        if Act2 == REJECT:
            server = agent.Round_robin(task)
            if not server:
                agent.Recycle_Task(task)
            else:
                agent.Select_server(server,"DIRECT")
                continue
        
        agent.Select_server(Act2)
        new_S2 = agent.state(2)
        Qout2_new = sess.run( Z2, feed_dict={ X2:new_S2 } )

        # Layer 3, Hour selection
        S3 = agent.state(3)

        if Rej == True:
            S3 = agent.Round_robin(task)
            if not S3:
                agent.Recycle_Task(task)
                continue
                
        Qout3 = sess.run( Z3, feed_dict={ X3:S3 } )

        Act3 = eipsilon_greedy( Qout3,episilon )

        if Act3 == REJECT:
            agent.Recycle_Task(task)
            continue 
        
        task.Select_Hour(Act3)
        agent.Select_server(Act3)
        new_S3 = agent.state(3)
        Qout3_new = sess.run( Z3, feed_dict={ X3:new_S3 } )

        # Layer 4, Minute selection
        S4 = agent.state(4)

        if Rej == True:
            S4 = agent.Round_robin(task)
            if not S3:
                agent.Recycle_Task(task)
                continue
                
        Qout4 = sess.run( Z4, feed_dict={ X4:S4 } )

        Act4 = eipsilon_greedy( Qout4,episilon )

        if Act4 == REJECT:
            agent.Recycle_Task(task)
            continue 
        
        task.Select_Minute(Act4)
        agent.Select_server(Act4)
        new_S4 = agent.state(4)
        Qout4_new = sess.run( Z4, feed_dict={ X4:new_S4 } )

        # Back_propogation. But for the first step we must calculate gamma + Qout_new
        Ser = agent.Get_Ser()
        Ser.Update_Unknown_Info()
        
        Qout1_new += Metrics.reward(1,Ser)
        Qout2_new += Metrics.reward(2,Ser)
        Qout3_new += Metrics.reward(3,Ser)
        Qout4_new += Metrics.reward(4,Ser)

        _,loss1 = sess.run( [optim1,cost1] , feed_dict= { X1:S1, Y1:Qout1_new } )
        _,loss2 = sess.run( [optim2,cost2] , feed_dict= { X2:S2, Y2:Qout2_new } )
        _,loss3 = sess.run( [optim3,cost3] , feed_dict= { X3:S3, Y3:Qout3_new } )
        _,loss4 = sess.run( [optim4,cost4] , feed_dict= { X4:S4, Y4:Qout4_new } )


def Predict(agent):
    result_dict = global_result_dict
    X1,Y1 = terminal["X1"],terminal["Y1"]   
    X2,Y2 = terminal["X2"],terminal["Y2"]   
    X3,Y3 = terminal["X3"],terminal["Y3"]   
    X4,Y4 = terminal["X4"],terminal["Y4"]   

    Z1 = result_dict["Z1"]
    Z2 = result_dict["Z2"]
    Z3 = result_dict["Z3"]
    Z4 = result_dict["Z4"]
    
    with tf.session() as sess:
        # Layer 1
        S1 = agent.state(1)
        Qout1 = sess.run( Z1, feed_dict={ X1:S1 } )
        Act1 = eipsilon_greedy( Qout1,episilon )
        
        if Act1 == REJECT:
            server = agent.Round_robin(task)
            if not server:
                agent.Recycle_Task(task)
            else:
                agent.Select_farm( server.farm )

        agent.Select_farm(Act1)

        # Layer 2
        S2 = agent.state(2)
        Qout2 = sess.run( Z2, feed_dict={ X2:S2 } )
        Act2 = eipsilon_greedy( Qout2,episilon )
        
        if Act2 == REJECT:
            server = agent.Round_robin(task)
            if not server:
                agent.Recycle_Task(task,"DIRECT")
            else:
                agent.Select_server(server)
                continue

        agent.Select_server(Act2)
        
      

def Entrance_Mode(mode,layer,params=[]):
    if mode == 'Load':
        pass 
    elif mode == 'Build':
        pass 
    elif mode == 'Run':
        pass 
    else:
        print(' Unknown work mode ! ')
        return -1:
    return 1
    