#encoding=utf-8
import collections # 词频统计用的
import math
import random
import zipfile # 解压缩用的
import time
import numpy as np
import tensorflow as tf

# Step 1: Read the data into a list of strings.
def read_data(filename):
  with zipfile.ZipFile(filename) as f:
    data = tf.compat.as_str(f.read(f.namelist()[0])).split()
  return data

# Step 2: Build the dictionary and replace rare words with UNK token.
def build_dataset(words, n_words):
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(n_words - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  unk_count = 0
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    else:
      index = 0
      unk_count += 1
    data.append(index)
  count[0][1] = unk_count
  reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
  return data, count, dictionary, reversed_dictionary

# Step 3: Function to generate a training batch for the skip-gram model.
def generate_batch(batch_size, num_skips, skip_window):
  global data_index
  assert batch_size % num_skips == 0
  assert num_skips <= 2 * skip_window
  batch = np.ndarray(shape=(batch_size), dtype=np.int32)
  labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
  span = 2 * skip_window + 1
  buffer = collections.deque(maxlen=span)
  for _ in range(span):
    buffer.append(data[data_index])
    data_index = (data_index + 1) % len(data)
  for i in range(batch_size // num_skips):
    target = skip_window
    targets_to_avoid = [skip_window]
    for j in range(num_skips):
      while target in targets_to_avoid:
        target = random.randint(0, span - 1)
      targets_to_avoid.append(target)
      batch[i * num_skips + j] = buffer[skip_window]
      labels[i * num_skips + j, 0] = buffer[target]
    buffer.append(data[data_index])
    data_index = (data_index + 1) % len(data)
  data_index = (data_index + len(data) - span) % len(data)
  return batch, labels

print 'Step 1: loading training set...'
graph_path = './graph/'
filename = 'text8.zip'
vocabulary_size = 50000
vocabulary = read_data(filename)
print 'Data size', len(vocabulary)
print
print 'Step 2: transfrom text into interger ...'
data, count, dictionary, reverse_dictionary = build_dataset(vocabulary,vocabulary_size)
del vocabulary  # Hint to reduce memory.
print 'Most common words (+UNK)', count[:5]
print 'Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]]
print
print 'Step 3: testing generate batch function ...'
data_index = 0
batch, labels = generate_batch(batch_size=8, num_skips=2, skip_window=1)
for i in range(8):
  print batch[i], reverse_dictionary[batch[i]],\
      '->', labels[i, 0], reverse_dictionary[labels[i, 0]]

# Step 4: Build and train a skip-gram model.
batch_size = 128
embedding_size = 128  # Dimension of the embedding vector.
skip_window = 1       # How many words to consider left and right.
num_skips = 2         # How many times to reuse an input to generate a label.

valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
num_sampled = 64    # Number of negative examples to sample.

num_steps = 1001

def skip_gram():
    train_inputs = tf.placeholder(shape=[batch_size],dtype=tf.int32)
    train_labels = tf.placeholder(shape=[batch_size,1],dtype=tf.int32)
    valid_dataset = tf.constant(valid_examples, dtype=tf.int32)
    with tf.device('/cpu:0'):
        with tf.variable_scope('word2cec_1') as word2cec_1:
            embeddings = tf.Variable(tf.random_uniform([vocabulary_size,embedding_size],-1.0,1.0))
            embed = tf.nn.embedding_lookup(embeddings,train_inputs)
        with tf.variable_scope('word2cec_2') as word2cec_2:
            nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size,embedding_size],
                                                              stddev=1.0 / math.sqrt(embedding_size)))
            nce_biases = tf.Variable(tf.zeros([vocabulary_size]))
        loss = tf.reduce_mean(
            tf.nn.nce_loss(weights=nce_weights,
                            biases=nce_biases,
                            labels=train_labels,
                            inputs=embed,
                            num_sampled=num_sampled,
                            num_classes=vocabulary_size))
        norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
        normalized_embeddings = embeddings / norm
        valid_embeddings = tf.nn.embedding_lookup(
                normalized_embeddings, valid_dataset)
        similarity = tf.matmul(
                valid_embeddings, normalized_embeddings, transpose_b=True)
    return train_inputs,train_labels,normalized_embeddings,loss,similarity

def run():
    print
    print 'Step 4: init training model ...'
    train_inputs, train_labels, normalized_embeddings,loss,similarity = skip_gram()
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print 'Initialized'
        average_loss = 0
        print
        print 'Step 5: training ...'
        for step in xrange(num_steps):
            batch_inputs, batch_labels = generate_batch(
                batch_size, num_skips, skip_window)
            feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
            _, loss_val = sess.run([optimizer,loss],feed_dict)
            average_loss += loss_val

            if step % 1000 == 0:
                if step > 0:
                    average_loss /= 1000
                print 'loss at iter ',step,': ',average_loss
                average_loss = 0

            if step % 10000 == 0:
                sim = similarity.eval()
                for i in xrange(valid_size):
                    valid_word = reverse_dictionary[valid_examples[i]]
                    top_k = 8  # number of nearest neighbors
                    nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                    log_str = 'Nearest to %s:' % valid_word
                    for k in xrange(top_k):
                        close_word = reverse_dictionary[nearest[k]]
                        log_str = '%s %s,' % (log_str, close_word)
                    print(log_str)
            final_embedding = normalized_embeddings.eval()
    return final_embedding
start = time.time()
final_embedding = run()
end = time.time()
elapsed = end - start
print
print 'training finish!'
print 'Time taken for training the skip-gram model : ',elapsed,'seconds.'
















