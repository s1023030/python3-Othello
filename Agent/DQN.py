import tensorflow as tf
import numpy as np
import random
import tensorflow.layers as tl
from Agent.Agent import AI

is_restore = False
restore_num = 500
PROB_EXPLOR = 0.3


class AI_DQN(AI):
    def __init__(self,is_human=False):
        super().__init__(is_human)
        self.name = 'DQN'
        self.store_path = "Agent/model/DQN_%d.ckpt"
        self.p_LR = 5e-4
        self._construct_network()
        self.pre_state_np = None
        self.pre_action = None
        self.episode_num = 0
        if is_restore:
            print("Restore from: ", self.store_path%restore_num)
            self.saver.restore(self.sess, self.store_path%restore_num)
            self.episode_num = restore_num


    def new_episode(self):
        self.first_turn = True
        self.episode_num +=1

    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        '''
        board
        00  10  20  30  40  50  60  70
        01  11  21  31  41  51  61  71
        02  12  22  32  42  52  62  72
        03  13  23  33  43  53  63  73
        04  14  24  34  44  54  64  74
        05  15  25  35  45  55  65  75
        06  16  26  36  46  56  66  76
        07  17  27  37  47  57  67  77
        '''
        board_np = np.array(board)
        state_np = np.zeros(board_np.shape,dtype=np.float32)
        replacement = {you_are: 1.0, (you_are^1):-1.0, -1:0.0}
        for original, after in replacement.items():
            state_np[board_np==original]=after
        reward_post = self._value_fn(winner, you_are, reward)

        if not self.first_turn:

            self._train(self.pre_state_np, self.pre_action, reward_post)

        self.first_turn = False
        if winner>-1:
            #print(self.grad_)
            print("Loss: ", self.loss_)
            store_path = self.saver.save(self.sess, self.store_path%self.episode_num)
            print("Store model : ",store_path, " !!!!!!!!!!!!")
            return [(-1,-1)]
        elif  len(poss_next_steps)==0:
            return [(-1,-1)]
        else:
            action =None
            prob = random.uniform(0.0,1.0)
            if prob<=PROB_EXPLOR:
                secure_random = random.SystemRandom()
                action = secure_random.sample(poss_next_steps,1)
            else:
                action_np = self._predict(state_np)
                min_val = abs(np.min(action_np))+1
                mask1 = np.zeros(action_np.shape)
                mask2 = np.zeros(action_np.shape)
                for step in poss_next_steps:
                    tmp_int = step[0]*8+step[1]
                    mask1[tmp_int]=1.0
                    mask2[tmp_int]=min_val 
                action_np = np.multiply(action_np, mask1)
                action_np = np.add(action_np, mask2)
                step = np.argmax(action_np,axis=-1)
                action = [(int(step/8),int(step%8))]
            self.pre_state_np = state_np
            self.pre_action = action
            return action

    def _train(self, state, action, reward):
        state = np.reshape(state, [1,8,8,1])
        reward_np = np.zeros([1,64])
        action_index = action[0][0]*8+action[0][1]
        reward_np[0][action_index] = reward
        a_, self.loss_ , a___, self.grad_ = self.sess.run([self.Q_evals,self.loss,self.train_op, self.grad],feed_dict={self.state:state,self.reward:reward_np})
        

    def _predict(self, state):
        state = np.reshape(state, [1,8,8,1])
        action_np = self.sess.run(self.Q_evals,feed_dict={self.state:state})
        return action_np[0]

    def _construct_network(self):
        self.state = tf.placeholder(tf.float32, [1,8,8,1])
        self.reward = tf.placeholder(tf.float32, [1,64])

        self.Q_evals = self._DQ_fn(self.state)

        condition = tf.math.logical_or(tf.math.greater(self.reward,0.0001), tf.math.less(self.reward,-0.0001) )
        Q_evals_ =  tf.where(condition, self.Q_evals, tf.zeros_like(self.reward))


        DQ_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, "DQ_fn")


        self.loss = tf.keras.losses.MSE(self.reward,Q_evals_)
        with tf.variable_scope("optimizer", reuse=tf.AUTO_REUSE) as scope:
            optimizer =  tf.train.AdamOptimizer(learning_rate=self.p_LR)
            self.train_op = optimizer.minimize(self.loss, var_list=DQ_vars)
            gvs = optimizer.compute_gradients(self.loss, var_list=DQ_vars)
            self.grad = [ grad for grad , var in gvs]
        gpu_options = tf.GPUOptions(allow_growth=True)
        self.saver = tf.train.Saver(max_to_keep=50,var_list=DQ_vars)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.sess.run(tf.global_variables_initializer())

    def _DQ_fn(self, state_tmp):
        with tf.variable_scope("DQ_fn",reuse=tf.AUTO_REUSE) as scope:
            conv1 = self._conv2d(state_tmp,   8, 3)
            conv2 = self._conv2d(conv1,   16, 3)
            conv3 = self._conv2d(conv2,   32, 3)
            conv3_p = self._pool(conv3, 3, 2) # 4 4 32

            conv4= self._conv2d(conv3_p,   64, 3)
            conv4_p = self._pool(conv4, 3, 2) # 2 2 64

            conv5 = self._conv2d(conv4_p,   128, 1)
            conv5_p = self._pool(conv5, 3, 2) # 1 1 64

            #feature1 = tf.reshape(conv5_p, [-1])
            feature1 = tf.layers.flatten(conv5_p)

            feature2 =self._fully_connected(feature1, 96)
            feature3 =self._fully_connected(feature2, 64)
            #feature4 =  tf.maximum(feature3, 0.01)
            feature4 = tf.where(tf.equal(feature3, 0.0), tf.constant(0.001,tf.float32,feature3.get_shape()), feature3 )
            return feature4
        
    def _value_fn(self, winner, you_are, reward):
        score = reward[you_are]-reward[(you_are^1)]
        if winner == you_are:
            score += 32.0
        elif winner == (you_are^1):
            score -= 32.0

        return score

    def _fully_connected(self, feature, o_size):
        return tl.dense(feature, units=o_size, activation=tf.nn.selu)

    def _conv2d(self, feature, o_size, k_size):
        return tl.conv2d(feature, filters=o_size, kernel_size=k_size,padding='SAME',activation=tf.nn.selu)

    def _pool(self, feature, k_size, stride):
        return tl.average_pooling2d(feature, pool_size=k_size ,strides=stride,padding='SAME')