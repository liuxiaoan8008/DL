#encoding=utf-8
import os
from gensim.models import word2vec

data_path = './data/'
model_path = './model/'


def sentence_pre_process(line):
    return line

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line = sentence_pre_process(line) # preprocess
                words = line.split()
                yield words


# Set values for various parameters
num_features = 300    # Word vector dimensionality
min_word_count = 40   # Minimum word count
num_workers = 6       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words
model_name = 'xxxword2vec.model'

# load sentence from the directory
sentences = MySentences(data_path) # a memory-friendly iterator
model = word2vec.Word2Vec(sentences,workers=num_workers,size=num_features,min_count=min_word_count,
                          window=context,sample=downsampling)
model.save(model_path+model_name)

# load trained model
# model = word2vec.Word2Vec.load(model_name)





