import tensorflow as tf
import numpy as np
import time

def weight_variable(shape,name='weight'):
    inital = tf.truncated_normal(shape,dtype=tf.float32,stddev=0.1,name=name)
    return tf.Variable(inital)

def bias_variable(shape,name='bias'):
    inital = tf.constant(0.1,shape=shape,dtype=tf.float32,name=name)
    return tf.Variable(inital)

def load_data(filename,data_num):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            # time += 1
            # if time <= data_num:
            line_s = line.split('\t')
            vectors.append(line_s)
    vectors = np.array(vectors, dtype = np.float32)
    print vectors.shape
    return vectors

def load_label(filename,data_num):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            # time += 1
            # if time <= data_num:
            if int(line) == 1:
                vectors.append([0,1])
            else:
                vectors.append([1,0])
    vectors = np.array(vectors, dtype = np.float32)
    print vectors.shape
    return vectors

h_l_neural = 3
learning_rate = 0.005
batch_size = 1000
data_size = 304433
test_size = 181524
input_size = 8
log_path = './log_3_add_top20_17all/'
# 122531

train_data_path = '/Users/liuxiaoan/Desktop/FEA/2016traintest/'
test_data_path = '/Users/liuxiaoan/Desktop/FEA/2017test/'

# test_size = 82531
#graph
X = tf.placeholder(tf.float32,[None,input_size])
Y_= tf.placeholder(tf.float32,[None,2])

#hidder layer
w1= weight_variable([input_size,h_l_neural])
b1= bias_variable([h_l_neural])

#out layer
w2= weight_variable([h_l_neural,2])
b2= bias_variable([2])

global_step = tf.Variable(0, name='global_step', trainable=False)
init = tf.global_variables_initializer()

#model
Y1 = tf.nn.sigmoid(tf.matmul(X,w1)+b1)
Y = tf.nn.softmax(tf.matmul(Y1,w2)+b2)

#loss
loss = -tf.reduce_sum(Y_*tf.log(Y))
# loss = tf.reduce_mean(tf.reduce_sum(tf.square(Y_ - Y),
#                                     reduction_indices=[1]))
tf.summary.scalar('loss', loss)
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train_step = optimizer.minimize(loss,global_step=global_step)

#read data
x_data = load_data(train_data_path+'feature_8_add10.txt',data_size)
x_label = load_label(train_data_path+'label_add20.txt',data_size)

t_data = load_data(test_data_path+'feature_8.txt',test_size)
# t_label = load_label(test_data_path+'label.txt',test_size)

#lunch
with tf.Session() as sess:
    sess.run(init)
    summary = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter(log_path, sess.graph)
    batch = 0
    step = 0
    for i in range(20000):
        start_time = time.time()
        batch_X = x_data[batch*batch_size:(batch+1)*batch_size]
        batch_Y = x_label[batch*batch_size:(batch+1)*batch_size]
        batch += 1
        if (batch+1)*batch_size > data_size:
            batch = 0
        train_data = {X: batch_X, Y_: batch_Y}
        _,loss_value = sess.run([train_step,loss], feed_dict=train_data)
        duration = time.time() - start_time
        if step % 500 == 0:
            print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
            summary_str = sess.run(summary, feed_dict=train_data)
            summary_writer.add_summary(summary_str, step)
            summary_writer.flush()
        step += 1
        if step % 1000 == 0:
            # test_data = {X: x_data[-80000:], Y_: x_label[-80000:]}
            test_data = {X:t_data}
            y_pre = sess.run(Y,feed_dict=test_data)
            file1 = open(log_path+'mlp_' + str(step) + '_1_pre.txt', 'w')
            file0 = open(log_path+'mlp_' + str(step) + '_0_pre.txt', 'w')
            print step
            print len(y_pre)
            for y in y_pre:
                # print y
                file1.write(str(y[1]) + '\n')
                file0.write(str(y[0]) + '\n')


