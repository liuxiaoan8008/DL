#encoding=utf-8
import tensorflow as tf
import conv_cnn_2 as cnn
import time,os
import numpy as np

#输入数据维度
input_length = 100
word2vec_dimension = 1
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
batch_size = 50
data_num = 100000

data_path= '/Users/liuxiaoan/ML/nlpcc2017/preprocess/fenci/'
model_path='/Users/liuxiaoan/ML/nlpcc2017/cnn/model/'

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
    print vectors.shape
    return vectors
def load_label(filename):
    vectors=[]
    with open(filename, 'r') as fp:
        time = 0
        for line in fp:
            time += 1
            if time <= data_num:
                if int(line) == 0:
                    vectors.append(-1)
                else:
                    vectors.append(1)
    vectors = np.array(vectors, dtype = np.float32)
    print vectors.shape
    return vectors

def compute_accuracy(sess,Q_data,Q_placeholder,A_data,A_placeholder,L_data,L_placeholder,Keep_placehloder,logist,step):
    y_pre = sess.run(logist, feed_dict={Q_placeholder: Q_data,A_placeholder:A_data,Keep_placehloder:1})
    print len(y_pre)
    file = open('./cnn_10w_xulie_entropy/cnn2_'+str(step)+'_pre.txt','w')
    for y in y_pre:
        # print y[0]
        file.write(str(y[0])+'\n')
    return y_pre

def run_training(Q,A,L):
    with tf.Graph().as_default():
        q_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        a_data = tf.placeholder(tf.float32, shape=[None, input_length, word2vec_dimension, 1])
        y_data = tf.placeholder(tf.float32)
        keep_prob = tf.placeholder(tf.float32)

        logits = cnn.inference(q_data,a_data,word2vec_dimension,
                               conv1_kernel_size,conv1_filter_number,
                               conv2_kernel_size,conv2_filter_number,fc_1_w,fc_2_w,keep_prob)

        loss = cnn.loss(logits,y_data)
        train_op = cnn.training(loss,learning_rate)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

        sess = tf.Session()
        sess.run(init)
        summary = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter('./cnn_2_xulie_log/', sess.graph)
        batch = 0
        for step in xrange(max_step):
            start_time = time.time()
            feed_dict = {q_data:Q[batch*batch_size:(batch+1)*batch_size],
                         a_data:A[batch*batch_size:(batch+1)*batch_size],
                         y_data:L[batch*batch_size:(batch+1)*batch_size],keep_prob: 0.6}
            _, loss_value = sess.run([train_op, loss],
                                     feed_dict=feed_dict)
            duration = time.time() - start_time
            batch += 1
            if batch ==900:
                batch = 0
            if step % 10 == 0:
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                summary_str = sess.run(summary, feed_dict=feed_dict)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()
                # compute_accuracy(sess, Q[(step+2)*100:(step+3)*100], q_data, A[(step+2)*100:(step+3)*100], a_data, L[(step+2)*100:(step+3)*100], y_data, logits)

            if (step + 1) % 100 == 0 or (step + 1) == max_step:
                # checkpoint_file = os.path.join(model_path,'model.ckpt')
                # saver.save(sess, checkpoint_file, global_step=step)
                compute_accuracy(sess,Q[-1000:],
                                 q_data,A[-1000:],
                                 a_data,L[-1000:],
                                 y_data,keep_prob,logits,step)

Q_data = load_data(data_path+'nlpcc2017-question-seq-all.dbqa.training-data').reshape([data_num,100,1,1])
A_data = load_data(data_path+'nlpcc2017-answer-seq.dbqa.training-data').reshape([data_num,100,1,1])
L_data = load_label(data_path+'lpcc-iccpol-2016-label.dbqa.training-data')


# Q_data = load_data(data_path+'nlpcc2017-question-seq-all.dbqa.training-data').reshape([100000,100,1,1])
# A_data = load_data(data_path+'nlpcc2017-answer-seq.dbqa.training-data').reshape([100000,100,1,1])
# L_data = load_label(data_path+'lpcc-iccpol-2016-label.dbqa.training-data')
run_training(Q_data,A_data,L_data)