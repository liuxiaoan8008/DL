from sklearn.cluster import KMeans
from gensim.models import word2vec
import globalvec as g
import time

# loading word2vec model
print 'loading word2vec model...'
model = word2vec.Word2Vec.load(g.m_path+'300features_40minwords_10context')
start = time.time()
model_vector = model.wv.syn0 # word2vec vocab numpy matirx
vocab = model.wv.index2word # wrod2vec vocab list
print model_vector.shape
# print model.wv.vocab #out put vacab learned by model

