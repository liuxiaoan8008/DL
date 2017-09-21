#encoding=utf-8
from __future__ import print_function
import tensorflow as tf
import numpy as np

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result

def weight_variable(shape,name='weight'):
    inital = tf.truncated_normal(shape,dtype=tf.float32,stddev=0.1,name=name)
    return tf.Variable(inital)


def bias_variable(shape,name='bias'):
    inital = tf.constant(0.1,shape=shape,dtype=tf.float32,name=name)
    return tf.Variable(inital)

def conv2d(x, W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
    # strides 第一个和最后一个必须为1[1,x_move,y_move,1]
    # padding: valid 抽出来的会比输入小， same：抽出来的和原图像一样大，就是外边加0了呗


def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def load_data(filename):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= 100000:
                line_s = line.split('\t')[:-1]
                vectors.append(line_s)
    vectors = np.array(vectors, dtype = np.float32)
    print (vectors.shape)
    return vectors
data_path= '/Users/liuxiaoan/ML/nlpcc2017/preprocess/fenci/'

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 100]) # 28x28
xs_a = tf.placeholder(tf.float32, [None, 100]) # 28x28
ys = tf.placeholder(tf.float32)
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs,[-1,100,1,1]) #[sample,heigt,width,channel]
x_image_a = tf.reshape(xs,[-1,100,1,1]) #[sample,heigt,width,channel]

## conv1 layer ##
with tf.name_scope('conv1'):
    W_conv1 = weight_variable([4,1,1,32]) # patch 5*5 insize=1,outsize 32
    b_conv1 = bias_variable([32])
    tf.summary.histogram('conv1' + '/Weights', W_conv1)
    tf.summary.histogram('conv1' + '/bias', b_conv1)
    h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

## conv2 layer ##
with tf.name_scope('conv2'):
    W_conv2 = weight_variable([4,1,32,64]) # patch 5*5 insize=1,outsize 32
    b_conv2 = bias_variable([64])
    tf.summary.histogram('conv2' + '/Weights', W_conv2)
    tf.summary.histogram('conv3' + '/bias', b_conv2)
    h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

## func1 layer ##
with tf.name_scope('fc1'):
    W_fc1 = weight_variable([25*64,1024])
    b_fc1 = bias_variable([1024])
    tf.summary.histogram('fc1' + '/Weights', W_fc1)
    tf.summary.histogram('fc1' + '/bias', b_fc1)
    h_pool2_flat = tf.reshape(h_pool2,[-1,25*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)
    h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

## func2 layer ##
with tf.name_scope('fc2'):
    W_fc2 = weight_variable([1024,1])
    b_fc2 = bias_variable([1])
    tf.summary.histogram('fc2' + '/W_fc2', W_fc2)
    tf.summary.histogram('fc2' + '/b_fc2', b_fc2)
    prediction = tf.nn.sigmoid(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)


# the error between prediction and real data
with tf.name_scope('loss'):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                                  reduction_indices=[1]))
    tf.summary.scalar('loss', cross_entropy) # loss
with tf.name_scope('train'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

sess = tf.Session()
# important step
# tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12
init = tf.global_variables_initializer()

# saver = tf.train.Saver()

sess.run(init)
merged = tf.summary.merge_all()
writer = tf.summary.FileWriter('./demo_log/',sess.graph)

Q_data = load_data(data_path+'nlpcc2017-question-seq-all.dbqa.training-data').reshape([100000,100,1,1])
# A_data = load_data(data_path+'nlpcc2017-answer-seq.dbqa.training-data').reshape([10000,100,1,1])
L_data = load_data(data_path+'lpcc-iccpol-2016-label.dbqa.training-data')

for i in range(2000):
    _,loss_value = sess.run([train_step,cross_entropy], feed_dict={x_image: Q_data, ys: L_data, keep_prob: 0.5})
    if i % 10 == 0:
        print('Step %d: loss = %.2f ' % (i, loss_value))
        result = sess.run(merged,feed_dict={x_image: Q_data, ys: L_data, keep_prob: 1})
        writer.add_summary(result,i)

# model_file = open('./model/cnn.pkl','wb')
# pick.dump(W_conv1,model_file)
# pick.dump(b_conv1,model_file)
# pick.dump(W_conv2,model_file)
# pick.dump(b_conv2,model_file)
#
# pick.dump(W_fc1,model_file)
# pick.dump(b_fc1,model_file)
# pick.dump(W_fc2,model_file)
# pick.dump(b_fc2,model_file)

# save_path = saver.save(sess,'./model/cnn.ckpt')
# print ('save to path:'+save_path)
# not need init step

# W = tf.Variable(np.arange(5*5*1*32).reshape([5,5,1,32]))
# saver.restore(sess,'./model/cnn.ckpt')
# print ('weight:'+sess.run(W_conv1))
# print ('biases:'+sess.run(b_conv1))
