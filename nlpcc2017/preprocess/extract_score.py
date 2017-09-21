#encoding=utf-8
path = '/Users/liuxiaoan/Desktop/FEA/2017test/data/'
f_path = '/Users/liuxiaoan/Desktop/FEA/2017test/'

def getindex(subset,set,out_file):
    index_list = []
    subset_list = []
    subset = open(subset)
    print 'start building subset_list...'
    for line in subset:
        line_s = line.split('\t')
        subset_list.append(line_s[1])
    subset.close()
    print 'building subset_list finish!'
    with open(set) as set:
        set_index = 1
        next_index = 0
        for line in set:
            line_s = line.split('\t')
            for i in range(next_index,len(subset_list)):
                if line_s[0].strip() == subset_list[i].strip():
                    next_index = i+1
                    index_list.append(set_index)
                    print line
                    break
            set_index += 1
        print 'get index finish!'
        print len(index_list)
    out_file = open(out_file,'w')
    for i in range(len(index_list)):
        out_file.write(str(index_list[i])+'\n')
    out_file.close()
    print 'index file build finish!'

def getsubscore(index_file,feature_file,out_file):
    index_list = []
    with open(index_file) as index_file:
        for line in index_file:
            index_list.append(int(line.strip()))
    print len(index_list)
    out_file = open(out_file, 'w')
    with open(feature_file) as feature_file:
        set_index = 1
        next_index = 0
        for line in feature_file:
            if set_index == index_list[next_index]:
                next_index += 1
                out_file.write(str(line.strip()+'\n'))
                print set_index
            set_index += 1
        print 'get score finish!'
    out_file.close()

def getnewfile(in_file,out_file):
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('\t')
            out_file.write(line_s[1]+'\t'+line_s[2]+'\t'+line_s[0]+'\n')
    out_file.close()
# getindex(path+'dbqa.txt',path+'nlpcc-2017.dbqa.testset',path+'index.txt')
getsubscore(path+'index.txt',f_path+'mlp_30w_20000_1_pre.txt',f_path+'testdata/ml_30w.txt')
# getnewfile(f_path+'testdata/dbqa.txt',f_path+'testdata/ndbqa.txt')
