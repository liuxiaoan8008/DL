#encoding=utf-8
import tensorflow as tf
import cnn1_att1 as cnn
import time,os
import numpy as np

#输入数据维度
input_length = 48
word2vec_dimension = 50

learning_rate = 0.01

max_step = 2000
batch_size = 50
data_num = 1000

data_path= '/Users/liuxiaoan/ML/nlpcc2017/tableQA/data/'

model_path='/Users/liuxiaoan/ML/nlpcc2017/cnn/model/'
log_path = '/Users/liuxiaoan/ML/nlpcc2017/tableQA/cnn1_att1_log/'

pre_path = '/Users/liuxiaoan/ML/nlpcc2017/tableQA/cnn1_att1_pre/'

def load_data(filename):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= data_num:
                line_s = line.split('\t')[:-1]
                vectors.append(line_s)
    vectors = np.array(vectors, dtype = np.float32)
    print 'loading %s succeed!  data shape:%s' %(filename.split('/')[-1],str(vectors.shape))
    return vectors

def load_label(filename):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= data_num:
                # TODO it's for classfication = 2
                if int(line) == 0:
                    vectors.append([0,1])
                else:
                    vectors.append([1,0])
    vectors = np.array(vectors, dtype = np.float32)
    print 'loading %s succeed!  data shape:%s' % (filename.split('/')[-1], str(vectors.shape))
    return vectors

def get_prescore(sess,feed_dic,logist,file_path,step):
    y_pre = sess.run(logist, feed_dict=feed_dic)
    y_pre_index = tf.argmax(y_pre, 1)
    print len(y_pre)
    print y_pre_index
    file = open(file_path+str(step)+'_pre.txt','w')
    for y in range(len(y_pre)):
        file.write(str(y_pre[y][y_pre_index[y]])+'\n')
    return y_pre

def run_training(Q,D,A,L,log_path,pre_path):
    with tf.Graph().as_default():
        q_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        d_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        a_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        y_data = tf.placeholder(tf.float32,shape=[None, 2]) # one hot
        keep_prob = tf.placeholder(tf.float32)

        logits = cnn.inference(q_data,d_data,a_data,input_length,word2vec_dimension,keep_prob,batch_size)
        loss = cnn.loss(logits, y_data)
        train_op = cnn.training(loss, learning_rate)

        init = tf.global_variables_initializer()
        sess = tf.Session()
        summary = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter(log_path, sess.graph)
        # sess.run(init)

Q_data = load_data(data_path+'train_label.txt')
D_data = load_data(data_path+'train_label.txt')
A_data = load_data(data_path+'train_label.txt')
L_data = load_label(data_path+'train_label.txt')
# .reshape([data_num,input_length,word2vec_dimension,1])

run_training(Q_data,D_data,A_data,L_data,log_path,pre_path)


