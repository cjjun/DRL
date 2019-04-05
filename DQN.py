import gym
import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt
# %matplotlib inline

# Load the environment
# 加载环境

env = gym.make('FrozenLake-v0')


# The Q-Network Approach
# Q网络方法
# Implementing the network itself
# 实现网络

tf.reset_default_graph()

# These lines establish the feed-forward part of the network used to choose actions
# 下面的几行代码建立了网络的前馈部分，它将用于选择行动
inputs1 = tf.placeholder(shape=[1,16],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([16,4],0,0.01))
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

# Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
# 下面的几行代码可以获得预测Q值与目标Q值间差值的平方和加总的损失。
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

# Training the network
# 训练网络
init = tf.initialize_all_variables()

# Set learning parameters
# 设置学习参数
y = .99
e = 0.1
num_episodes = 2000
#create lists to contain total rewards and steps per episode
# 创建列表以包含每个episode对应的总回报与总步数。
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        # Reset environment and get first new observation
        # 初始化环境并获得第一个观察
        s = env.reset()
        rAll = 0
        d = False
        j = 0
        # The Q-Network
        # Q网络
        while j < 99:
            j+=1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            # 基于Q网络的输出结果，贪婪地选择一个行动（有一定的概率选择随机行动）
            a,allQ = sess.run([predict,Qout],feed_dict={inputs1:np.identity(16)[s:s+1]})
            if np.random.rand(1) < e:
                a[0] = env.action_space.sample()
            # Get new state and reward from environment
            # 从环境中获得回报以及新的状态信息
            s1,r,d,_ = env.step(a[0])5
            # Obtain the Q' values by feeding the new state through our network
            # 通过将新的状态向量输入到网络中获得Q值。
            Q1 = sess.run(Qout,feed_dict={inputs1:np.identity(16)[s1:s1+1]})
            # Obtain maxQ' and set our target value for chosen action.
            # 获得最大的Q值，并为所选行为设定目标值
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            # Train our network using target and predicted Q values
            # 用目标和预测的Q值训练网络
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:np.identity(16)[s:s+1],nextQ:targetQ})
            rAll += r
            s = s1
            if d == True:
                # Reduce chance of random action as we train the model.
                # 随着训练的进行，主键减少选择随机行为的概率
                e = 1./((i/50) + 10)
                break
        jList.append(j)
        rList.append(rAll)
print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")