import numpy as np 
import tensorflow as tf 
from tensorflow.nn import relu

global_params = None 
global_parameters = None 
global_terminal = None 
global_result_dict = None

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

    with tf.Session() as sess:
        sess.run( tf.global_variables_initializer() )

        # For layer 1, farm decision
        Rej,S1 = agent.state()
        if Rej == 1:
            S1 = agent.round_robin()
        Qout1 = sess.run( Z1, feed_dict={ X1:S1 } )

        Act1 = eipsilon_greedy( Qout1,episilon )
        agent.Select_farm(Act1)
        new_S1 = agent.state()

        Qout1_new = sess.run( Z1, feed_dict={ X1:new_S1 } )
        # For layer 2, server decision
        # S2 = agent.state()



        # Backpropogation
        _,loss1 = sess.run( [optim1,cost1] , feed_dict= { X1:S1, Y1:Qout1_new } )

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
        S1 = agent.state(1)
        Qout1 = sess.run( Z1, feed_dict={ X1:S1 } )
        Act1 = eipsilon_greedy( Qout1,episilon )
    
    return Act1
      

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
    