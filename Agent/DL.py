import tensorflow as tf
import tensorflow.contrib.layers as tcl
from Agent.Agent import AI
class AI_DL(AI):
    def __init__(self,is_human=False):
        super().__init__(is_human)
        self.name = 'AI_DL'
        self.p_LR = 5e-5


    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        if winner>-1:
            pass
        else:
            return [(-1,-1)]

    def _construct_network(self):
        self.state = tf.placeholder(tf.float32,[8,8])
        self.reward = tf.placeholder(tf.float32,[1])

        self.action = self._policy(self.state)
        self.value = self._value_fn(self.state)

        p_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='policy_CNN')
        v_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='value_CNN')

        tf.train.AdamOptimizer(learning_rate=self.p_LR).minimize()

    def _policy(self, state_tmp):
        with tf.variable_scope("policy_CNN") as scope:
            conv1 = self._conv2d(state_tmp,   4, 5)
            conv1_p = self._max_pool(conv1, 2) # 4 4 4

            conv2 = self._conv2d(conv1_p,   16, 3)
            conv2_p = self._max_pool(conv2, 2) # 2 2 16

            conv3 = self._conv2d(conv2_p,   64, 1)
            conv3_p = self._max_pool(conv3, 2) # 1 1 64

            feature1 = tf.reshape(conv3_p, [-1])

            feature2 =self._fully_connected(feature1, 70)
            feature3 =self._fully_connected(feature2, 64)
            feature4 =  tf.maximum(feature3, 0.01)
            return tf.nn.softmax(feature4)
        
    def _value_fn(self, state_tmp):
        with tf.variable_scope("value_CNN") as scope:
            conv1 = self._conv2d(state_tmp,   4, 5)
            conv1_p = self._max_pool(conv1, 2) # 4 4 4

            conv2 = self._conv2d(conv1_p,   16, 3)
            conv2_p = self._max_pool(conv2, 2) # 2 2 16

            conv3 = self._conv2d(conv2_p,   64, 1)
            conv3_p = self._max_pool(conv3, 2) # 1 1 64

            feature1 = tf.reshape(conv3_p, [-1])

            feature2 =self._fully_connected(feature1, 32)
            feature3 =self._fully_connected(feature2, 1)
            return feature3

    def _fully_connected(self, feature, o_size):
        return tcl.fully_connected(feature, o_size, activation_fn=tf.nn.selu)

    def _conv2d(self, feature, o_size, k_size):
        return tcl.conv2d(feature, o_size, k_size, activation_fn=tf.nn.selu)

    def _max_pool(self, feature, k_size):
        return tf.nn.max_pool(feature, ksize=[1,k_size,k_size,1],strides=[1,k_size,k_size,1],padding='SAME')