
source_path = '/Users/liuxiaoan/Desktop/FEA/2017test/'
# 2016_2017_all_test_train_feature/2016trainfeature

def confiles(page_file,QAtopic_file,search_file,querylike_file,
             mapword_file,num_file,simword_file,word2vec_file,out_file):
    page_file = open(page_file)
    QAtopic_file = open(QAtopic_file)
    search_file = open(search_file)
    querylike_file = open(querylike_file)
    word2vec_file = open(word2vec_file)
    mapword_file = open(mapword_file)
    num_file = open(num_file)
    simword_file = open(simword_file)

# mapword_file,num_file,simword_file,
    out_file = open(out_file,'w')
    for f1,f2,f3,f4,f5,f6,f7,f8 in zip(page_file,QAtopic_file,search_file,querylike_file,
                                    word2vec_file,mapword_file,num_file,simword_file):
        out_file.write(f1.strip()+'\t'+f2.strip()+'\t'+f3.strip()+'\t'+f4.strip()+'\t'
                       +f5.strip()+'\t'+f6.strip()+'\t'+f7.strip()+'\t'+f8.strip()+'\n')
    out_file.close()
    page_file.close()
    QAtopic_file.close()
    search_file.close()
    querylike_file.close()
    mapword_file.close()
    num_file.close()
    simword_file.close()

def getlabels(in_file,out_file):
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('\t')
            out_file.write(line_s[2]+'\n')
    out_file.close()


confiles(source_path+'Pagecossim.txt',
         source_path + 'QAtopic_score.txt',
         source_path + 'saerchKeyWordV1_1+2+3+4',
         source_path + 'search-sV1.5.txt',
         source_path + 'mapword_feature.txt',
         source_path + 'num_feature.txt',
         source_path + 'simword_feature.txt',
         source_path + 'word2vecalignscore.txt',
         source_path + 'feature_8.txt')

# getlabels(source_path,data_path + 'train2016_label.txt')

