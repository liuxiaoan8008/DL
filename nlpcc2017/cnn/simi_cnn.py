import math

import tensorflow as tf
import numpy as np

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

def inference(q_data,a_data_T,a_data_F):
    # conv1
    with tf.name_scope('q_conv1'):
        q_W_conv1 = weight_variable([conv1_w, word2vec_d, 1, conv1_filter])  # patch 5*5 insize=1,outsize 32
        q_b_conv1 = bias_variable([conv1_filter])
        q_h_conv1 = tf.nn.tanh(conv2d(q_data, q_W_conv1) + q_b_conv1)
        q_h_pool1 = max_pool_2x2(q_h_conv1)

    with tf.name_scope('a_T_conv1'):
        a_W_conv1 = weight_variable([conv1_w, word2vec_d, 1, conv1_filter])  # patch 5*5 insize=1,outsize 32
        a_b_conv1 = bias_variable([conv1_filter])
        a_h_conv1 = tf.nn.tanh(conv2d(a_data_T, a_W_conv1) + a_b_conv1)
        a_h_pool1 = max_pool_2x2(a_h_conv1)

    with tf.name_scope('a_F_conv1'):
        a_W_conv1_F = weight_variable([conv1_w, word2vec_d, 1, conv1_filter])  # patch 5*5 insize=1,outsize 32
        a_b_conv1_F = bias_variable([conv1_filter])
        a_h_conv1_F = tf.nn.tanh(conv2d(a_data_F, a_W_conv1_F) + a_b_conv1_F)
        a_h_pool1_F = max_pool_2x2(a_h_conv1_F)

    with tf.name_scope('similality'):
        same_matrix_M = tf.truncated_normal([-1,421,421],dtype=tf.float32,stddev=0.1,name='similarity_matrix')
        q_h_pool1_re = tf.reshape(q_h_pool1,[-1,421*1,12])
        temp = tf.matmul(tf.transpose(q_h_pool1_re,perm=[0,2,1]),same_matrix_M)
        a_h_pool1_re = tf.reshape(a_h_pool1,[-1,421,12])
        a_h_pool1_F_re = tf.reshape(a_h_pool1_F, [-1, 421, 12])
        similarity_T = tf.matmul(temp,a_h_pool1_re)
        similarity_F = tf.matmul(temp,a_h_pool1_F_re)
    return similarity_T,similarity_F,same_matrix_M

def loss(similarity_T,similarity_F,same_matrix_M,lam):
    with tf.name_scope('loss'):
        convex = tf.square((1-similarity_T+similarity_F))
        loss = tf.reduce_mean(convex, name='min_M') + lam / 2.0 * np.sum(tf.square(same_matrix_M,name='square'))
    return loss

def training(loss, learning_rate):
    tf.summary.scalar('loss', loss)
    optimizer = tf.train.AdadeltaOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    with tf.name_scope('train'):
        train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op

def evaluation(logits, labels):
  correct = tf.nn.in_top_k(logits, labels, 1)
  return tf.reduce_sum(tf.cast(correct, tf.int32))





