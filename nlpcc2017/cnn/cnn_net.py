import math

import tensorflow as tf

input_l = 845
word2vec_d = 50
conv1_w = 4
conv1_filter = 12
learning_rate = 0.5

def weight_variable(shape,name='weight'):
    inital = tf.truncated_normal(shape,dtype=tf.float32,stddev=0.1,name=name)
    return tf.Variable(inital)

def bias_variable(shape,name='bias'):
    inital = tf.constant(0.1,shape=shape,dtype=tf.float32,name=name)
    return tf.Variable(inital)

def conv2d(x, W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='VALID')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def inference(q_data,a_data):
    # conv1
    with tf.name_scope('q_conv1'):
        q_W_conv1 = weight_variable([conv1_w, word2vec_d, 1, conv1_filter])  # patch 5*5 insize=1,outsize 32
        q_b_conv1 = bias_variable([conv1_filter])
        q_h_conv1 = tf.nn.tanh(conv2d(q_data, q_W_conv1) + q_b_conv1)
        q_h_pool1 = max_pool_2x2(q_h_conv1)

    with tf.name_scope('a_conv1'):
        a_W_conv1 = weight_variable([conv1_w, word2vec_d, 1, conv1_filter])  # patch 5*5 insize=1,outsize 32
        a_b_conv1 = bias_variable([conv1_filter])
        a_h_conv1 = tf.nn.tanh(conv2d(a_data, a_W_conv1) + a_b_conv1)
        a_h_pool1 = max_pool_2x2(a_h_conv1)
    with tf.name_scope('similality'):
        same_matrix = tf.subtract(q_h_pool1,a_h_pool1)
        same_matrix_s = tf.multiply(same_matrix,same_matrix)

    with tf.name_scope('fc1'):
        h_pool2_flat = tf.reshape(same_matrix_s, [-1,421*421*conv1_filter])
        W_fc1 = weight_variable([421*421*conv1_filter, 1024])
        b_fc1 = bias_variable([1024])
        h_fc1 = tf.nn.tanh(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([1024, 2])
        b_fc2 = bias_variable([2])
        h_fc2 = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)
    return h_fc2

def loss(logits,labels):
    labels = tf.to_int64(labels)
    with tf.name_scope('loss'):
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=labels, logits=logits, name='xentropy')
    return tf.reduce_mean(cross_entropy, name='xentropy_mean')

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





