import tensorflow as tf
import numpy as np

matrix = np.random.randint(10, size=[3,4])

print matrix
print matrix.shape
print matrix.ndim
maxvec = tf.argmax(matrix,1)
with tf.Session() as sess:
    print sess.run(maxvec)