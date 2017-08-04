#coding=utf-8
import os
from gensim.models import word2vec
import thulac
from bs4 import BeautifulSoup
import chardet
import time

data_path = '/var/data/wiki/wikiex/AA/in/'
model_path = './model/'

def sentence_pre_process(line):
    line = BeautifulSoup(line, 'lxml').get_text()
    return line

class MySentences(object):
    def __init__(self, dirname,thu1):
        self.dirname = dirname
        self.thu1 = thu1
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line = thu1.cut(line,text=True) # preprocess
                words = line.split()
                yield words
# Set values for various parameters
num_features = 50    # Word vector dimensionality
min_word_count = 40   # Minimum word count
num_workers = 6       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words
model_name = 'w2c_wiki_50.model'


def train_model():
    global thu1
    # load sentence from the directory
    thu1 = thulac.thulac()
    sentences = MySentences(data_path, thu1)  # a memory-friendly iterator
    print
    print 'train word2vec ...'
    model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count,
                              window=context, sample=downsampling)
    print
    print 'save model...'
    model.save(model_path + model_name)
    print
    print 'finish.'

start = time.time()
train_model()
end = time.time()
elapsed = end - start
print 'The time token for training gensim-SG model : ',elapsed/60,'min'
# load trained model
# print 'loading model ...'
# model = word2vec.Word2Vec.load(model_path+model_name)
# # word_vectors = model.wv.syn0 # word2vec vocab numpy matirx
# vocab_list = model.wv.index2word # wrod2vec vocab list
# print len(vocab_list)
# for vo in vocab_list[:100]:
#     print vo



# with open(data_path+'wiki_test') as wiki:
#     for line in wiki:
#         if len(line.strip()) == 0:
#             continue
#         print line
#         print chardet.detect(line)
#         print thu1.cut('猜想以及從選定的公理及定義中建立起嚴謹推導出的定理')
#         # print thu1.cut(line.decode('utf-8'))


