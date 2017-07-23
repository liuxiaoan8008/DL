#encoding=utf-8
import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
path = './data/'


def readdata(file_name):
    """
    header = 0 ：第一行为列名
    delimiter = '\t' :切分
    quoting = 3  表示3列？
    :param file_name:
    :return:
    """
    data_set = pd.read_csv(file_name, header=0, delimiter='\t', quoting=3)
    # print train.shape
    # print train.columns.values  # cloumns name
    # print train['review'][0]
    return data_set

def review_to_words(raw_review):
    """
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    :param raw_review:
    :return: word string
    """
    review_text = BeautifulSoup(raw_review,'lxml').get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    return " ".join(meaningful_words)

# prepare train data
train = pd.read_csv(path+'labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
num_reivews = train['review'].size

clean_review = []
for i in xrange(0,num_reivews):
    if (i+1)%1000 == 0:
        print 'Review %d of %d\n' % (i+1,num_reivews)
    clean_review.append(review_to_words(train['review'][i]))

vectorizer = CountVectorizer(analyzer='word',
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=None,
                             max_features=5000)
train_data_features = vectorizer.fit_transform(clean_review)
train_data_features = train_data_features.toarray()
# print train_data_features.shape
# print vectorizer.vocabulary_
# print vectorizer.stop_words_
# vocab = vectorizer.get_feature_names()
# print vocab
# dist = np.sum(train_data_features,axis = 0)
# for tag, count in zip(vocab,dist):
#     print count, tag


# train a random forest model
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_data_features,train['sentiment'])


# prepare test data
test = pd.read_csv(path+'testData.tsv', header=0, delimiter='\t', quoting=3)
test_reiviews = len(test['review'])
clean_test_review = []
for i in xrange(0,test_reiviews):
    if (i+1)%1000 == 0:
        print 'Review %d of %d\n' % (i+1,test_reiviews)
    clean_test_review.append(review_to_words(test['review'][i]))
test_data_features = vectorizer.transform(clean_test_review)
test_data_features = test_data_features.toarray()


# predict
result = forest.predict(test_data_features)
output = pd.DataFrame(data={'id':test['id'],'sentiment':result})
output.to_csv(path+'Bag_of_words_model.csv',index=False,quoting=3)

