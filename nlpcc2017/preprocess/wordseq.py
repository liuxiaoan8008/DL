#encoding=utf-8
import tokenizer as token
import jieba

data_path = './train&testdata/'
fenci_path = './fenci/'
statistic_path = './statistic/'

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
def getwordseq(in_file,dic_file,out_file,out_file1):
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
            line_s = line.split('\t')
            for word in line_s:
                # print word
                word_new = word.strip().replace('\n', '')
                if word_new is not '':
                    try:
                        seq.append(dic[word_new])
                    except:
                        print word
                        seq.append(index)
                        dic[word] = index
                        dic_file.write(word_new+'\t'+str(index)+'\n')
                        index += 1
            if len(seq) < 100:
                for i in range(100-len(seq)):
                    seq.append(0)
            else:
                out_file1.write(str(time)+'\t'+line)
            time += 1
            print 'time:%d   seq:%d' %(time,len(seq))
            seq_str = ''
            for i in range(100):
                seq_str = seq_str + str(seq[i])+'\t'
            seq_str = seq_str +str(seq[99])
            out_file.write(seq_str+'\n')
        out_file1.close()
        out_file.close()


# buildworseq(statistic_path+'question_wordcount.txt',statistic_path+'word_seq.txt')
# getwordseq(fenci_path+'lpcc-iccpol-2016-answer.dbqa.fenci.training-data',
#            statistic_path+'word_seq.txt',
#            fenci_path+'nlpcc2017-answer-seq.dbqa.training-data',
#            statistic_path+'anwser_morethan100.txt')
