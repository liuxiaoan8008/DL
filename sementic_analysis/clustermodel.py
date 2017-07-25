from sklearn.cluster import KMeans
from gensim.models import word2vec
import globalvec as g
import time
from sklearn.externals import joblib
import preprocessing as pre
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# loading word2vec model
print 'loading word2vec model...'
model = word2vec.Word2Vec.load(g.m_path+'300features_40minwords_10context')

word_vectors = model.wv.syn0 # word2vec vocab numpy matirx
vocab_list = model.wv.index2word # wrod2vec vocab list
# # print model.wv.vocab #out put vacab learned by model
num_clusters = word_vectors.shape[0]/5

def train_model(num_clusters,word_vectors,vocab_list):
    print 'training the kmeans model...'
    start = time.time()
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

# for cluster in xrange(0,10):
#     words = []
#     for i in xrange(0,len(word_centroid_map.values())):
#         if word_centroid_map.values()[i] == cluster:
#             words.append(word_centroid_map.keys()[i])
#     print words

def create_bag_of_centroids( wordlist, word_centroid_map ):
    num_centroids = max(word_centroid_map.values()) + 1
    bag_of_centroids = np.zeros(num_centroids, dtype="float32" )
    for word in wordlist:
        if word in word_centroid_map:
            index = word_centroid_map[word]
            bag_of_centroids[index] += 1
    #
    # Return the "bag of centroids"
    return bag_of_centroids


print 'loading word center map...'
word_centroid_map = joblib.load(g.m_path+'word_cent_map.pkl')
# prepare train data
print 'prepare train data....'
train = pd.read_csv(g.path+'labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
num_reivews = train['review'].size
clean_review = []
for i in xrange(0,num_reivews):
    if (i+1)%1000 == 0:
        print 'Review %d of %d\n' % (i+1,num_reivews)
    clean_review.append(pre.review_to_words(train['review'][i]))

# prepare test data
print 'prepare test data...'
test = pd.read_csv(g.path+'testData.tsv', header=0, delimiter='\t', quoting=3)
test_reiviews = len(test['review'])
clean_test_review = []
for i in xrange(0,test_reiviews):
    if (i+1)%1000 == 0:
      print 'Review %d of %d\n' % (i+1,test_reiviews)
    clean_test_review.append(pre.review_to_words(test['review'][i]))

# Pre-allocate an array for the training set bags of centroids (for speed)
train_centroids = np.zeros((train["review"].size, num_clusters), dtype="float32" )
counter = 0
for review in clean_review:
    train_centroids[counter] = create_bag_of_centroids( review,word_centroid_map )
    counter += 1

test_centroids = np.zeros((test["review"].size, num_clusters), dtype="float32" )
counter = 0
for review in clean_test_review:
    test_centroids[counter] = create_bag_of_centroids( review, word_centroid_map )
    counter += 1

# Fit a random forest and extract predictions
forest = RandomForestClassifier(n_estimators = 100)
# Fitting the forest may take a few minutes
print "Fitting a random forest to labeled training data..."
forest = forest.fit(train_centroids,train["sentiment"])
result = forest.predict(test_centroids)
# Write the test results
output = pd.DataFrame(data={"id":test["id"], "sentiment":result})
output.to_csv(g.m_path+"BagOfCentroids.csv", index=False, quoting=3 )