from sklearn.cluster import KMeans
from gensim.models import word2vec
import globalvec as g
import time
from sklearn.externals import joblib

# loading word2vec model
print 'loading word2vec model...'
model = word2vec.Word2Vec.load(g.m_path+'300features_40minwords_10context')
start = time.time()
word_vectors = model.wv.syn0 # word2vec vocab numpy matirx
vocab_list = model.wv.index2word # wrod2vec vocab list
# print model.wv.vocab #out put vacab learned by model

num_clusters = word_vectors.shape[0]/5

print 'training the kmeans model...'
kmeans_clustering = KMeans(n_clusters=num_clusters)
kmeans_model = kmeans_clustering.fit(word_vectors)
idx = kmeans_model.predict(word_vectors)
end = time.time()
elapsed = end - start
print 'Time taken for K Means Clustering:',elapsed,'seconds.'
word_centroid_map = dict(zip(vocab_list,idx))
joblib.dump(kmeans_model, g.m_path+'kmeans_model.pkl')
print 'save kmeans_model success!'
joblib.dump(word_centroid_map,g.m_path+'word_cent_map.pkl')
print 'task finish!'





