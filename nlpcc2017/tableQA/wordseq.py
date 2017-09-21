#encoding=utf-8
import jieba

data_path = './data/'
statistic_path = './statistic/'

#词频统计
def wordcount(in_file,out_file,min_fre):
    import collections
    word_box = []
    word_file = open(in_file)
    for line in word_file:
        # print line
        words = line.strip().split(' ')
        for word in words:
            # print word.replace('\n', '').replace(' ','')
            try:
                word_box.extend(word.replace('\n', '').replace(' ','').encode('utf-8'))
            except:
                print word
    word_file.close()
    word_map = collections.Counter(word_box)
    out_file = open(out_file, 'w')
    for word in word_map:
        if word_map[word] >= min_fre:
            out_str = word + '\t' + str(word_map[word])
            print out_str
            out_file.write(out_str + '\n')
    out_file.close()

def wordcountforeng(in_file,out_file,min_fre):
    word_dic = {}
    with open(in_file) as in_file:
        for line in in_file:
            words = line.strip().split(' ')
            for word in words:
                word = word.strip().replace('\n', '').replace(' ','')
                if word in word_dic.keys():
                    word_dic[word] += 1
                else:
                    word_dic[word] = 1
    with open(out_file,'w') as out_file:
        count = 0
        for word in word_dic.keys():
            out_file.write(word+'\n')
            count += 1
    print count




#建立seq字典
def buildworseq(dic_file,out_file):
    with open(dic_file) as dic_file:
        word_index = 1
        out_file = open(out_file,'w')
        for line in dic_file:
            line_s = line.split('\t')
            new_word = line_s[0].strip().replace('\n', '')
            if new_word is not '':
                out_file.write(new_word+'\t'+str(word_index)+'\n')
                word_index += 1
        out_file.close()

#将问题和答案转换成seq
#参数说明：已分词文本文件，wordseq字典，序列化之后的文件，序列化输入长度，超过序列化长度的文件
def getwordseq(in_file,dic_file,out_file,length,out_file1):
    with open(in_file) as in_file:
        # loading word seqence dictionary
        dic_file_temp = open(dic_file)
        dic = {}
        index = 1
        for line in dic_file_temp:
            line_s = line.split('\t')
            dic[line_s[0]] = int(line_s[1])
            index += 1
        # print index
        dic_file_temp.close()
        dic_file = open(dic_file,'a')
        # word to seqence
        # print dic
        time = 0
        out_file = open(out_file,'w')
        out_file1 = open(out_file1,'w')
        for line in in_file:
            seq = []
            line_s = line.split(' ')
            for word in line_s:
                # print word
                word_new = word.strip().replace('\n', '').replace(' ','')
                if word_new is not '':
                    try:
                        seq.append(dic[word_new])
                    except:
                        print word
                        seq.append(index)
                        dic[word] = index
                        dic_file.write(word_new+'\t'+str(index)+'\n')
                        index += 1
            if len(seq) < length:
                for i in range(length-len(seq)):
                    seq.append(0)
            else:
                out_file1.write(str(time)+'\t'+line)
            time += 1
            print 'time:%d   seq:%d' %(time,len(seq))
            seq_str = ''
            for i in range(length):
                seq_str = seq_str + str(seq[i])+'\t'
            seq_str = seq_str +str(seq[length-1])
            out_file.write(seq_str+'\n')
        out_file1.close()
        out_file.close()

# wordcountforeng(data_path+'train_question.txt',statistic_path+'table_wordcount.txt',1)
# buildworseq(statistic_path+'table_wordcount.txt',statistic_path+'word_seq.txt')
getwordseq(data_path+'train_description.txt',
           statistic_path+'word_seq.txt',
           data_path + 'train_description_seq.txt',48,
           statistic_path+'train_description_morethan100.txt')
