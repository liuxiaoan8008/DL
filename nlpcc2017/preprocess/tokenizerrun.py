#encoding=utf-8
import tokenizer as token
import jieba

data_path = './train&testdata/'
fenci_path = './fenci/'
statistic_path = './statistic/'


# 方法：问题去重并统计各问题答案数量
# 环境配置：
# 使用：
def getcontent(in_file,out_file1,out_file2):
    with open(in_file) as in_file:
        out_file1 = open(out_file1,'w')
        out_file2 = open(out_file2, 'w')
        dic = {}
        line_d = []
        for line in in_file:
            if line in dic.keys():
                dic[line] += 1
            else:
                dic[line] = 1
                line_d.append(line)
        for key in line_d:
            out_file1.write(key)
            out_file2.write(str(dic[key]) + '\n')

        out_file1.close()
        out_file2.close()


# 方法：统计句子长度大于100的数量
# 环境配置：
# 使用：
def getlength100(in_file,max):
    count = 0
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split(' : ')
            if int(line_s[0]) > max:
                count = count + int(line_s[1])
    print count

# 方法：词频统计
# 环境配置：
# 使用：
def statisticword(in_file,out_file):
    all_word = 0
    word_dic = {}
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split('\t')
            for word in line_s:
                if word in word_dic.keys():
                    word_dic[word] += 1
                else:
                    word_dic[word] = 1
                    all_word += 1
        out_file = open(out_file,'w')
    for word in word_dic.keys():
        out_file.write(word + '\t' + str(word_dic[word])+'\n')
    print all_word

# 方法：问题恢复和答案一样的长度
# 环境配置：
# 使用：
def buildquestions(in_file_q,in_file_count,out_file):
    in_file_count = open(in_file_count)
    in_file_q = open(in_file_q)
    out_file = open(out_file,'w')
    for line in in_file_q:
        count = int(in_file_count.readline())
        print count
        for i in range(count):
            out_file.write(line)
    out_file.close()
    in_file_count.close()
    in_file_q.close()





token.wordcutzhcn(data_path+'nlpcc-iccpol-2016.dbqa.training-data',
                  fenci_path+'lpcc-iccpol-2016-question-s.dbqa.fenci_search.training-data',
                  fenci_path + 'lpcc-iccpol-2016-answer-s.dbqa.fenci_search.training-data',
                  fenci_path + 'lpcc-iccpol-2016-label.dbqa.training-data')
#
# token.exstopwords(fenci_path+'lpcc-iccpol-2016-answer.dbqa.fenci_search.training-data',
#                     fenci_path+'lpcc-iccpol-2016-answer-s.dbqa.fenci_search.training-data'
#                   )
#
# getcontent(fenci_path+'lpcc-iccpol-2016-question.dbqa.fenci.training-data',
#             fenci_path+'lpcc-iccpol-2016-question-one.dbqa.fenci.training-data',
#            fenci_path+'lpcc-iccpol-2016-question-count.dbqa.training-data')
#
# getlength100(statistic_path+'AA_all_lenght.txt',80)
#
# statisticword(fenci_path+'lpcc-iccpol-2016-question-one.dbqa.fenci.training-data',
#               statistic_path+'question_wordcount.txt')
#
# buildquestions(fenci_path+'nlpcc2017-question-seq.dbqa.training-data',
#                fenci_path+'lpcc-iccpol-2016-question-count.dbqa.training-data',
#                fenci_path+'nlpcc2017-question-seq-all.dbqa.training-data')


