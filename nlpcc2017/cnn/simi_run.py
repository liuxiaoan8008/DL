import tensorflow as tf
import simi_cnn as cnn

input_l = 845
word2vec_d = 50
conv1_w = 4
conv1_filter = 12
learning_rate = 0.5
step = 2000
lam = 0.0000001

def run_training():
    with tf.Graph().as_default():
        q_data = tf.placeholder(tf.float32, shape=[None, input_l, word2vec_d, 1])
        a_data = tf.placeholder(tf.float32, shape=[None, input_l, word2vec_d, 1])
        a_data_F = tf.placeholder(tf.float32, shape=[None, input_l, word2vec_d, 1])
        y_data = tf.placeholder(tf.float32)

        sim_T,sim_F,sim_M = cnn.inference(q_data,a_data,a_data_F)
        loss = cnn.loss(sim_T,sim_F,sim_M,lam)
        train_op = cnn.training(loss,learning_rate)

        # init = tf.global_variables_initializer()

        sess = tf.Session()
        summary = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter('./logs/', sess.graph)
        # sess.run(init)
        # for i in range(step):
run_training()