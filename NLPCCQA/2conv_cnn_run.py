#encoding=utf-8
import tensorflow as tf
import conv_cnn_2 as cnn
import time,os
import numpy as np
import pickle

#输入数据维度
input_length = 100
word2vec_dimension = 50
#1层卷积参数
conv1_kernel_size = 3
conv1_filter_number = 32
#2层卷积参数
conv2_kernel_size = 3
conv2_filter_number = 64
#全连接层参数
fc_1_w = 25
fc_2_w = 1
#学习率
learning_rate = 0.001

max_step = 2000
batch_size = 500
keep_prob_n = 0.6

#全局数据index
data_index = 0

data_path= './data/'
model_path='./model/'

def load_data(filename,data_num):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= data_num:
                line_s = line.split('\t')[:-1]
                vectors.append(line_s)
    vectors = np.array(vectors, dtype = np.float32).reshape([len(vectors),100,1,1])
    print vectors.shape
    return vectors

def load_label(filename,data_num):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= data_num:
                ## TODO tanh use, sigmoid need change
                if int(line) == 0:
                    vectors.append(-1)
                else:
                    vectors.append(1)
    vectors = np.array(vectors, dtype = np.float32)
    print vectors.shape
    return vectors

def load_fromdump(filename,input_length,word2vec_dimension):
    pkl_file = open(filename, 'rb')
    data_vec = pickle.load(pkl_file)
    data_vec = np.array(data_vec, dtype=np.float32)
    print data_vec[0]
    data_vec = data_vec.reshape([len(data_vec),input_length,word2vec_dimension,1])
    print data_vec[0]
    return data_vec

def generate_batch(batch_size,Q_data,A_data,Y_data):
    global data_index
    batch_q_data = np.ndarray(shape=[batch_size, input_length, word2vec_dimension, 1], dtype=np.float32)
    batch_a_data = np.ndarray(shape=[batch_size, input_length, word2vec_dimension, 1], dtype=np.float32)
    batch_y_data = np.ndarray(shape=[batch_size],dtype=np.float32)
    for i in range(batch_size):
        batch_q_data[i] = Q_data[data_index]
        batch_a_data[i] = A_data[data_index]
        batch_y_data[i] = Y_data[data_index]
        data_index = (data_index + 1) % len(Y_data)
    return batch_q_data,batch_a_data,batch_y_data

def predict(sess,Q_data,Q_placeholder,A_data,A_placeholder,Keep_placehloder,logist,step):
    y_pre = sess.run(logist, feed_dict={Q_placeholder: Q_data,A_placeholder:A_data,Keep_placehloder:1})
    print 'out similarity score size: ',str(len(y_pre))
    file = open('./cnn/'+str(word2vec_dimension)+'/cnn2_'+str(step)+'_pre.txt','w')
    for y in y_pre:
        # print y[0]
        file.write(str(y[0])+'\n')
    return y_pre

def run_training(Q,A,L,T_q,T_a):
    global data_index
    with tf.Graph().as_default():
        q_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        a_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        y_data = tf.placeholder(tf.float32,shape=[None])
        keep_prob = tf.placeholder(tf.float32)

        logits = cnn.inference(q_data,a_data,word2vec_dimension,
                               conv1_kernel_size,conv1_filter_number,
                               conv2_kernel_size,conv2_filter_number,fc_1_w,fc_2_w,keep_prob)

        loss = cnn.loss(logits,y_data)
        train_op = cnn.training(loss,learning_rate)

        init = tf.global_variables_initializer()
        # saver = tf.train.Saver()

        sess = tf.Session()
        sess.run(init)
        summary = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter('./cnn/'+str(word2vec_dimension)+'/', sess.graph)
        for step in xrange(max_step):
            start_time = time.time()
            batch_q_data, batch_a_data, batch_y_data = generate_batch(batch_size,Q,A,L)
            feed_dict = {q_data:batch_q_data,
                         a_data:batch_a_data,
                         y_data:batch_y_data,
                         keep_prob: keep_prob_n}
            _, loss_value = sess.run([train_op, loss],
                                     feed_dict=feed_dict)
            duration = time.time() - start_time
            if step % 10 == 0:
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                summary_str = sess.run(summary, feed_dict=feed_dict)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()
                print data_index
                # compute_accuracy(sess, Q[(step+2)*100:(step+3)*100], q_data, A[(step+2)*100:(step+3)*100], a_data, L[(step+2)*100:(step+3)*100], y_data, logits)

            if step % 500 == 0 or (step + 1) == max_step:
                # checkpoint_file = os.path.join(model_path,'model.ckpt')
                # saver.save(sess, checkpoint_file, global_step=step)
                predict(sess,Q[-1000:],q_data,A[-1000:],a_data,keep_prob,logits,step)

# Q_data = load_data(data_path+'nlpcc2016-q.training-data',np.inf)
# A_data = load_data(data_path+'nlpcc2016-a.training-data',np.inf)
L_data = load_label(data_path+'lpcc-iccpol-2016-label.dbqa.training-data',np.inf)
# T_Q_data = load_data(data_path+'nlpcc2016-q.test-data',np.inf)
# T_A_data = load_data(data_path+'nlpcc2016-a.test-data',np.inf)
input_length = 100
word2vec_dimension = 50

Q_data = load_fromdump(data_path+'nlpcc2016-q-w2v.training-data',input_length,word2vec_dimension)
A_data = load_fromdump(data_path+'nlpcc2016-a-w2v.training-data',input_length,word2vec_dimension)


run_training(Q_data,A_data,L_data,None,None)