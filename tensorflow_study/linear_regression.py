import tensorflow as tf

logdir = './log'

g = tf.Graph()
with g.as_default():
    a = 2
    b = 3
    x = tf.add(a, b)
    y = tf.multiply(a, b)
    useless = tf.multiply(x, a,name='useless')
    z = tf.pow(y, x)
    with tf.Session(graph=g) as sess:
        writer = tf.summary.FileWriter(logdir,g)
        z = sess.run(z)
    writer.close()
