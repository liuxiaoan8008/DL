#encoding=utf-8

import pandas as pd
import globalvec as g
import preprocessing as pre
import nltk.data
import logging
from gensim.models import word2vec
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def loadGloveModel(gloveFile):
    print "Loading Glove Model..."
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    print "Done.",len(model)," words loaded!"
    return model

def review_to_sentences(review,tokenizer, remove_stopword=False):
    raw_sentences = tokenizer.tokenize(review.strip().decode('utf-8'))
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            # print pre.review_to_words(raw_sentence,remove_stopword)
            sentences.append(pre.review_to_words(raw_sentence,remove_stopword))
    return sentences

def makeFeatureVec(words,model,num_features):
    featureVec = np.zeros((num_features,),dtype='float32')
    nwords = 0
    index2word_set = set(model.keys())
    for word in words:
        if word in index2word_set:
            nwords += 1
            featureVec = np.add(featureVec,model[word])
    if nwords != 0:
        featureVec = np.divide(featureVec,nwords)
    else:
        print 'find a empty sentence!'
    return featureVec

def getReAvgFeatureVecs(reviews,model,num_features):
    num_review = len(reviews)
    counter = 0
    reviewFeatureVec = np.zeros((num_review,num_features))
    for review in reviews:
        if counter % 1000 == 0:
            print 'avg_feature of Review %d of %d' % (counter,num_review)
        reviewFeatureVec[counter] = makeFeatureVec(review,model,num_features)
        counter += 1
    return reviewFeatureVec

# train = pd.read_csv(g.path+'labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)[:100]
# test = pd.read_csv(g.path+'testData.tsv', header=0, delimiter='\t', quoting=3)
# unlabeled_train = pd.read_csv(g.path+'unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
#
# # Verify the number of reviews that were read (100,000 in total)
# print "Read %d labeled train reviews, %d labeled test reviews, " \
#      "and %d unlabeled reviews\n" % (train["review"].size,
#      test["review"].size, unlabeled_train["review"].size )
#
# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#
# print 'Parsing sentence from training set'
# sentences = []
# for review in train['review']:
#     sentences += review_to_sentences(review,tokenizer)
#
# print 'Parsing sentence from unlabeled set'
# for review in unlabeled_train['review']:
#     sentences += review_to_sentences(review,tokenizer)
#
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
# # Set values for various parameters
num_features = 300    # Word vector dimensionality
min_word_count = 40   # Minimum word count
num_workers = 6       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words
#
# print 'Training model...'
# model = word2vec.Word2Vec(sentences,workers=num_workers,size=num_features,min_count=min_word_count,
#                           window=context,sample=downsampling)
# model.init_sims(replace=True)

# model_name = g.m_path+'300features_40minwords_10context'
# model.save(model_name)

# model = word2vec.Word2Vec.load(model_name)
# for word, vocab_obj in model.wv.vocab.items():
#     print word, vocab_obj
# print model.doesnt_match("man woman child cat".split())
# print model.most_similar("man")
# print model.most_similar("awful")
# print model['flower']

model = loadGloveModel(g.m_path+'glove.6B.300d.txt')

# prepare train data
print 'prepare train data....'
train = pd.read_csv(g.path+'labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
num_reivews = train['review'].size
clean_review = []
for i in xrange(0,num_reivews):
    if (i+1)%1000 == 0:
        print 'Review %d of %d\n' % (i+1,num_reivews)
    clean_review.append(pre.review_to_words(train['review'][i]))
trainDataVecs = getReAvgFeatureVecs(clean_review,model,num_features)

# prepare test data
print 'prepare test data...'
test = pd.read_csv(g.path+'testData.tsv', header=0, delimiter='\t', quoting=3)
test_reiviews = len(test['review'])
clean_test_review = []
for i in xrange(0,test_reiviews):
    if (i+1)%1000 == 0:
      print 'Review %d of %d\n' % (i+1,test_reiviews)
    clean_test_review.append(pre.review_to_words(test['review'][i]))
testDataVecs = getReAvgFeatureVecs(clean_test_review,model,num_features)

# train a random forest model
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(trainDataVecs,train['sentiment'])

# predict
result = forest.predict(testDataVecs)
output = pd.DataFrame(data={'id':test['id'],'sentiment':result})
output.to_csv(g.path+'glove_model_result.csv',index=False,quoting=3)



