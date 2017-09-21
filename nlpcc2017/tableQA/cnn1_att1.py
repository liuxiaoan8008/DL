#encoding=utf-8
import math
import tensorflow as tf
import numpy as np


#输入数据维度
input_length = 48
word2vec_dimension = 50

#1层卷积参数
conv1_kernel_size = 4
conv1_filter_number = 32

#2层卷积参数
conv2_kernel_size = 4
conv2_filter_number = 64

#全连接层参数
fc_1_w = 1024
fc_2_w = 2

#学习率
learning_rate = 0.01


def weight_variable(shape,name='weight'):
    inital = tf.truncated_normal(shape,dtype=tf.float32,stddev=0.1,name=name)
    return tf.Variable(inital)

def bias_variable(shape,name='bias'):
    inital = tf.constant(0.1,shape=shape,dtype=tf.float32,name=name)
    return tf.Variable(inital)

def conv2d(x, W,padding='VALID'):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding=padding)

def max_att_pooling(x,height,width):
    return tf.nn.max_pool(x,ksize=[1,height,width,1],strides=[1,1,1,1],padding='VALID')

def inference(Q,D,A,input_length,word2vec_dimension,keep_prob,batch_size):
    # conv1
    with tf.name_scope('q_conv1'):
        q_W_conv1 = weight_variable([conv1_kernel_size, word2vec_dimension, 1, conv1_filter_number])  # patch 5*5 insize=1,outsize 32
        q_b_conv1 = bias_variable([conv1_filter_number])
        q_h_conv1 = tf.nn.tanh(conv2d(Q, q_W_conv1,padding='SAME') + q_b_conv1)
        tf.summary.histogram('q_conv1/q_h_pool1', q_h_conv1)

    with tf.name_scope('d_conv1'):
        d_W_conv1 = weight_variable([conv1_kernel_size, word2vec_dimension, 1, conv1_filter_number])  # patch 5*5 insize=1,outsize 32
        d_b_conv1 = bias_variable([conv1_filter_number])
        d_h_conv1 = tf.nn.tanh(conv2d(D, d_W_conv1,padding='SAME') + d_b_conv1)
        tf.summary.histogram('q_conv1/q_h_pool1', d_h_conv1)

    with tf.name_scope('a_conv1'):
        a_W_conv1 = weight_variable([conv1_kernel_size, word2vec_dimension, 1, conv1_filter_number])  # patch 5*5 insize=1,outsize 32
        a_b_conv1 = bias_variable([conv1_filter_number])
        a_h_conv1 = tf.nn.tanh(conv2d(A, a_W_conv1,padding='SAME') + a_b_conv1)
        tf.summary.histogram('q_conv1/q_h_pool1', a_h_conv1)

    with tf.name_scope('q_d_attention'):
        matrix_q_d_1 = weight_variable([conv1_filter_number,word2vec_dimension,word2vec_dimension])
        tan_ma = []
        for i in range(batch_size):
            temp_q_u = tf.matmul(tf.transpose(q_h_conv1[i], perm=[2, 0, 1]), matrix_q_d_1)
            temp_q_u_d = tf.matmul(temp_q_u,tf.transpose(d_h_conv1[i],perm=[2,1,0]))
            tan_ma.append(temp_q_u_d)
        tan_matrix_q_d = tf.nn.tanh(tan_ma)
        tan_matrix_q_d = tf.transpose(tan_matrix_q_d, perm=[0, 2, 3, 1])
        q_d_pool1_g = max_att_pooling(tan_matrix_q_d, 1, input_length)
        tf.summary.histogram('q_conv1/q_h_pool1_g', q_d_pool1_g)
        d_h_pool1_g = tf.transpose(max_att_pooling(tan_matrix_q_d, input_length, 1), perm=[0, 2, 3, 1])
        tf.summary.histogram('q_conv1/d_h_pool1_g', d_h_pool1_g)

    with tf.name_scope('q_a_attention'):
        matrix_q_a_1 = weight_variable([conv1_filter_number, word2vec_dimension, word2vec_dimension])
        tan_ma_a = []
        for i in range(batch_size):
            temp_q_u = tf.matmul(tf.transpose(q_h_conv1[i], perm=[2, 0, 1]), matrix_q_a_1)
            temp_q_u_a = tf.matmul(temp_q_u, tf.transpose(a_h_conv1[i], perm=[2, 1, 0]))
            tan_ma_a.append(temp_q_u_a)
        tan_matrix_q_a = tf.nn.tanh(tan_ma_a)
        tan_matrix_q_a = tf.transpose(tan_matrix_q_a, perm=[0, 2, 3, 1])
        q_a_pool1_g = max_att_pooling(tan_matrix_q_a, 1, input_length)
        tf.summary.histogram('q_conv1/q_h_pool1_g', q_a_pool1_g)
        a_h_pool1_g = tf.transpose(max_att_pooling(tan_matrix_q_a, input_length, 1), perm=[0, 2, 3, 1])
        tf.summary.histogram('q_conv1/d_h_pool1_g', a_h_pool1_g)
    # fc1
    with tf.name_scope('MLP_1'):
        q_pool1_flat = tf.reshape(q_d_pool1_g, [-1, input_length * 1 * conv1_filter_number])
        d_pool1_flat = tf.reshape(d_h_pool1_g, [-1, input_length * 1 * conv1_filter_number])
        q_add_d_flat = tf.concat(1, [q_pool1_flat, d_pool1_flat])

        qa_pool1_flat = tf.reshape(q_a_pool1_g, [-1, input_length * 1 * conv1_filter_number])
        aq_pool1_flat = tf.reshape(d_h_pool1_g, [-1, input_length * 1 * conv1_filter_number])
        q_add_a_flat = tf.concat(1, [qa_pool1_flat, aq_pool1_flat])

        q_d_a_flat = tf.concat(1, [q_add_d_flat, q_add_a_flat])

        W_fc1 = weight_variable([4*input_length * 1 * conv1_filter_number, fc_1_w])
        b_fc1 = bias_variable([fc_1_w])
        mut_fc1 = tf.matmul(q_d_a_flat, W_fc1) + b_fc1
        mut_fc1_drop = tf.nn.dropout(mut_fc1, keep_prob)
        h_fc1 = tf.nn.tanh(mut_fc1_drop)
        tf.summary.histogram('MLP_1/outputs', h_fc1)

    with tf.name_scope('softmax'):
        W_fc2 = weight_variable([fc_1_w, 2])
        b_fc2 = bias_variable([2])
        h_fc2 = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)
        tf.summary.histogram('softmax/outputs', h_fc2)
    return h_fc2

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
