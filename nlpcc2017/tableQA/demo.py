import numpy as np
import tensorflow as tf

Q = [[1],[2],[3]]
U = [[1,1,1],[2,2,2],[3,3,3]]
Q1 = [[[1,1],[2,1],[3,1]],[[1,1],[2,1],[3,1]]]
U1 = [[[2,3],[2,3]]]
Q1 = np.array(Q1,dtype = np.float32)
U1 = np.array(U1,dtype = np.float32)
print Q1.shape
print U1.shape
with tf.Session() as sess:
    op = tf.matmul(Q1,U1)
    print sess.run(op)
