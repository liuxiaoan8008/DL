#coding=utf-8
import os
from gensim.models import word2vec
import thulac
from bs4 import BeautifulSoup
import chardet

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
                line = thu1.cut(line) # preprocess
                words = line.split()
                yield words


# Set values for various parameters
num_features = 300    # Word vector dimensionality
min_word_count = 40   # Minimum word count
num_workers = 6       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words
model_name = 'word2vec_wiki2017page_article.model'

# load sentence from the directory
thu1 = thulac.thulac()
sentences = MySentences(data_path,thu1) # a memory-friendly iterator
print 'train word2vec ...'
model = word2vec.Word2Vec(sentences,workers=num_workers,size=num_features,min_count=min_word_count,
                          window=context,sample=downsampling)
print 'save model...'
model.save(model_path+model_name)
print 'finish.'
# load trained model
# model = word2vec.Word2Vec.load(model_name)


# with open(data_path+'wiki_test') as wiki:
#     for line in wiki:
#         if len(line.strip()) == 0:
#             continue
#         print line
#         print chardet.detect(line)
#         print thu1.cut('猜想以及從選定的公理及定義中建立起嚴謹推導出的定理')
#         # print thu1.cut(line.decode('utf-8'))


