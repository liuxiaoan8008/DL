#encoding=utf-8

import pandas as pd
import globalvec as g
import preprocessing as pre
import nltk.data
import logging
from gensim.models import word2vec

def review_to_sentences(review,tokenizer, remove_stopword=False):
    raw_sentences = tokenizer.tokenize(review.strip().decode('utf-8'))
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(pre.review_to_words(raw_sentence,remove_stopword))
    return sentences

train = pd.read_csv(g.path+'labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
test = pd.read_csv(g.path+'testData.tsv', header=0, delimiter='\t', quoting=3)
unlabeled_train = pd.read_csv(g.path+'unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)

# Verify the number of reviews that were read (100,000 in total)
print "Read %d labeled train reviews, %d labeled test reviews, " \
     "and %d unlabeled reviews\n" % (train["review"].size,
     test["review"].size, unlabeled_train["review"].size )

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

print 'Parsing sentence from training set'
sentences = []
for review in train['review']:
    sentences += review_to_sentences(review,tokenizer)

print 'Parsing sentence from unlabeled set'
for review in unlabeled_train['review']:
    sentences += review_to_sentences(review,tokenizer)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
# Set values for various parameters
num_features = 300    # Word vector dimensionality
min_word_count = 40   # Minimum word count
num_workers = 6       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words

print 'Training model...'
model = word2vec.Word2Vec(sentences,workers=num_workers,size=num_features,min_count=min_word_count,
                          window=context,sample=downsampling)
model.init_sims(replace=True)
model_name = g.m_path+'300features_40minwords_10context'
model.save(model_name)


