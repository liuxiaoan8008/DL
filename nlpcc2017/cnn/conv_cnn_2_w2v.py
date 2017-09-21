#encoding=utf-8
import math
import tensorflow as tf

#输入数据维度
input_length = 100
word2vec_dimension = 1

#1层卷积参数
conv1_kernel_size = 4
conv1_filter_number = 12

#2层卷积参数
conv2_kernel_size = 4
conv2_filter_number = 12

#全连接层参数
fc_1_w = 25
fc_2_w = 1

#学习率
learning_rate = 0.5

def weight_variable(shape,name='weight'):
    inital = tf.truncated_normal(shape,dtype=tf.float32,stddev=0.1,name=name)
    return tf.Variable(inital)

def bias_variable(shape,name='bias'):
    inital = tf.constant(0.1,shape=shape,dtype=tf.float32,name=name)
    return tf.Variable(inital)

def conv2d(x, W,padding='VALID'):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding=padding)

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def inference(q_data,a_data,word2vec_dimension,
              conv1_kernel_size,conv1_filter_number,
              conv2_kernel_size,conv2_filter_number,
              fc_1_w,fc_2_w,keep_prob):
    # conv1
    with tf.name_scope('q_conv1'):
        q_W_conv1 = weight_variable([conv1_kernel_size, word2vec_dimension, 1, conv1_filter_number])  # patch 5*5 insize=1,outsize 32
        q_b_conv1 = bias_variable([conv1_filter_number])
        q_h_conv1 = tf.nn.tanh(conv2d(q_data, q_W_conv1) + q_b_conv1)
        q_h_pool1 = max_pool_2x2(q_h_conv1)
        tf.summary.histogram('q_conv1/q_h_pool1', q_h_pool1)
    with tf.name_scope('a_conv1'):
        a_W_conv1 = weight_variable([conv1_kernel_size, word2vec_dimension, 1, conv1_filter_number])  # patch 5*5 insize=1,outsize 32
        a_b_conv1 = bias_variable([conv1_filter_number])
        a_h_conv1 = tf.nn.tanh(conv2d(a_data, a_W_conv1) + a_b_conv1)
        a_h_pool1 = max_pool_2x2(a_h_conv1)
        tf.summary.histogram('q_conv1/a_h_pool1', a_h_pool1)

    #conv2
    with tf.name_scope('q_conv2'):
        q_W_conv2 = weight_variable([conv2_kernel_size, 1, conv1_filter_number , conv2_filter_number])  # patch 5*5 insize=1,outsize 32
        q_b_conv2 = bias_variable([conv2_filter_number])
        q_h_conv2 = tf.nn.tanh(conv2d(q_h_pool1,q_W_conv2,padding='SAME') + q_b_conv2)
        q_h_pool2 = max_pool_2x2(q_h_conv2)
        tf.summary.histogram('q_conv2/q_h_pool2', q_h_pool2)

    with tf.name_scope('a_conv2'):
        a_W_conv2 = weight_variable([conv2_kernel_size, 1, conv1_filter_number , conv2_filter_number])  # patch 5*5 insize=1,outsize 32
        a_b_conv2 = bias_variable([conv2_filter_number])
        a_h_conv2 = tf.nn.tanh(conv2d(a_h_pool1, a_W_conv2,padding='SAME') + a_b_conv2)
        a_h_pool2 = max_pool_2x2(a_h_conv2)
        tf.summary.histogram('a_conv2/a_h_pool2', a_h_pool2)

    #fc1
    with tf.name_scope('MLP_1'):
        q_pool2_flat = tf.reshape(q_h_pool2, [-1, 25 * 1 * conv2_filter_number])
        a_pool2_flat = tf.reshape(a_h_pool2, [-1, 25 * 1 * conv2_filter_number])
        q_add_a = tf.concat(1,[q_pool2_flat,a_pool2_flat])
        W_fc1 = weight_variable([25 * 1 * conv2_filter_number*2, fc_1_w*conv2_filter_number])
        b_fc1 = bias_variable([fc_1_w*conv2_filter_number])
        mut_fc1 = tf.matmul(q_add_a, W_fc1) + b_fc1
        mut_fc1_drop = tf.nn.dropout(mut_fc1,keep_prob)
        h_fc1 = tf.nn.tanh(mut_fc1_drop)
        tf.summary.histogram('MLP_1/outputs', h_fc1)

    with tf.name_scope('MLP_2'):
        W_fc2 = weight_variable([fc_1_w*conv2_filter_number, fc_2_w * conv2_filter_number])
        b_fc2 = bias_variable([fc_2_w * conv2_filter_number])
        mut_fc2 = tf.matmul(h_fc1, W_fc2) + b_fc2
        mut_fc2_drop = tf.nn.dropout(mut_fc2, keep_prob)
        h_fc2 = tf.nn.tanh(mut_fc2_drop)
        tf.summary.histogram('MLP_2/outputs', h_fc2)

    with tf.name_scope('softmax'):
        W_fc3 = weight_variable([fc_2_w * conv2_filter_number, 1])
        b_fc3 = bias_variable([1])
        h_fc3 = tf.nn.sigmoid(tf.matmul(h_fc2, W_fc3) + b_fc3)
        tf.summary.histogram('softmax/outputs', h_fc3)
    return h_fc3

def loss(logits,labels):
    with tf.name_scope('loss'):
        # loss = tf.reduce_mean(tf.reduce_sum(tf.square(labels - logits),
        #                                     reduction_indices=[1]))
       loss = tf.reduce_mean(-tf.reduce_sum(labels * tf.log(logits),
                                            reduction_indices=[1]))
    return loss

def training(loss, learning_rate):
    tf.summary.scalar('loss', loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    with tf.name_scope('train'):
        train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op

def evaluation(logits, labels):
  correct = tf.nn.in_top_k(logits, labels, 1)
  return tf.reduce_sum(tf.cast(correct, tf.int32))
