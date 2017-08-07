import thulac
import sys
from gensim.models import word2vec
import numpy as np
import pickle

data_path = './data/'
model_path = '/var/data/wiki/wikiex/AA/model/'
reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

# 分词
def wordcutzhcn(in_file, out_file1, out_file2, out_file3):
    thu1 = thulac.thulac(seg_only=True)
    with open(in_file) as in_file:
        out_file1 = open(out_file1, 'w')
        out_file2 = open(out_file2, 'w')
        out_file3 = open(out_file3, 'w')

        for line in in_file:
            line_split = line.split('\t')
            seg_text1 = thu1.cut(line_split[0],text=True)
            seg_test2 = thu1.cut(line_split[1],text=True)
            out_file1.write(seg_text1.strip()+ '\n')
            out_file2.write(seg_test2.strip()+ '\n')
            out_file3.write(str(line_split[2]))
            print seg_text1
            print seg_test2
        out_file1.close()
        out_file2.close()
        out_file3.close()

# 词序列转换成向量矩阵
def makeFeatureVec(words,model,num_features,sen_dim):
    featureVec = np.zeros((sen_dim,num_features),dtype='float32')
    zeroVec = np.zeros((num_features,),dtype='float32')
    index2word_set = set(model.keys())
    if len(words) < sen_dim:
        for word in words:
            if word in index2word_set:
                featureVec = np.add(featureVec, model[word])
            else:
                featureVec = np.add(featureVec, zeroVec)
        for _ in range(sen_dim-len(words)):
            featureVec = np.add(featureVec, zeroVec)
    else:
        for i in range(len(words)):
            if words[i] in index2word_set:
                featureVec = np.add(featureVec, model[words[i]])
            else:
                featureVec = np.add(featureVec, zeroVec)
    return featureVec


def loadwor2vec_model(file_name):
    print 'loading model ...'
    model = word2vec.Word2Vec.load(file_name)
    return model

def text2vec(in_file,model,w2v_dim,sen_dim,out_file):
    data_matrix = []
    with open(in_file) as in_file:
        for line in in_file:
            words = line.split()
            w2v_matrix = makeFeatureVec(words,model,w2v_dim,sen_dim)
            data_matrix.append(w2v_matrix)
    output = open('out_file', 'wb')
    pickle.dump(data_matrix, output)


# wordcutzhcn(data_path+'nlpcc-iccpol-2016.dbqa.training-data',
#             data_path+'nlpcc2016-q.training-data',
#             data_path + 'nlpcc2016-a.training-data',
#             data_path + 'nlpcc2016-l.training-data')
sen_dim = 100
w2v_dim = 50

model = loadwor2vec_model(model_path+'w2v_wiki_50.model')
text2vec(data_path+'nlpcc2016-q.training-data',model,w2v_dim,sen_dim,data_path+'nlpcc2016-q-w2v.training-data')

