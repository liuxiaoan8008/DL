#encoding=utf-8
import tokenizer as token
import jieba
import re
import tttest as hsj

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

data_path = './train&testdata/'
fenci_path = './fenci/'
statistic_path = './statistic/'
feature_path = './feature/'
source_path = '/Users/liuxiaoan/Desktop/DBQA/'
dic_path = './dic/'
test2017_pre_path = '/Users/liuxiaoan/ML/nlpcc2017/MLP/log_3_8_30w_17all/'

FEA_PATH = '/Users/liuxiaoan/Desktop/FEA/2017test/cut10999/'
FEA2_path = '/Users/liuxiaoan/Desktop/FEA/2017test/cut11000/'
FEAtrain_path = '/Users/liuxiaoan/Desktop/FEA/2016traintest/'

"""
# 方法：问题和答案数字匹配程度特征
# 环境配置：无
# 输入参数说明：in_file：问题、答案对文件，out_file：特征保持文件
# 其他：使用了词频，也可以改成one hot。并且加入了去重操作
"""

def catchbynum(in_file, out_file):
    with open(in_file) as in_file:
        out_file = open(out_file, 'w')
        num_pattern = re.compile(r'\d+')
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            line_q = line_s[1].strip().split('\t')
            line_a = line_s[2].strip().split('\t')

            match_num = 0
            num_dic = {}
            for q_word in line_q:
                if num_pattern.match(q_word.strip()):
                    if q_word.strip() in num_dic:
                        num_dic[q_word.strip()] += 1
                    else:
                        num_dic[q_word.strip()] = 1
            for a_word in line_a:
                if a_word.strip() in num_dic.keys():
                    print a_word.strip()
                    match_num += 1
            out_file.write(str(match_num)+'\n')
        out_file.close()

"""
# 方法：读取映射词字典
# 环境配置：无
# 输入参数说明：in_file：映射词字典文件 一对多
# 输出参数说明：words_dic:映射词字典
# 其他：
"""
def buildmapwords(in_file):
    words_dic = {}
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split(' ')
            words_dic[line_s[0]] = line_s[1:]
            # for w in words_dic[line_s[0]]:
            #     print w
    return words_dic

def readfile(in_file,out_file):
    in_file = open(in_file)
    out_file = open(out_file,'w')
    for line in in_file:
        print line
        out_file.write(line.encode('utf-8'))
    out_file.close()
    in_file.close()

"""
# 方法：根据问题获取关键词对应对映射词和同义词
# 环境配置：无
# 输入参数说明：key_words：关键词，key_dic：映射词词典
# 输出参数说明：map_words:映射词
# 其他：使用了词频，也可以改成one hot。
"""
def getmapwordfeature(key_words,key_dic):
    map_words = set()
    for word in key_words:
        # print word
        if word in key_dic.keys():
            for map in key_dic[word]:
                map_words.add(map)
        # TODO get similar words from hsj
    print 'map_words:'
    mapwords_str = '\t'.join(map_words)
    print mapwords_str
    return map_words

"""
# 方法：构建疑问词列表
# 环境配置：无
# 输入参数说明：in_file：疑问词字典
# 输出参数说明：question_words:疑问词列表
# 其他：
"""
def buildqword(in_file):
    question_words = []
    with open(in_file) as questionwords:
        for word in questionwords:
            if word.strip() not in question_words:
                question_words.append(word.strip())
    return question_words

def exstopword(qa_list):
    new_list = []
    # 停用词和标点符号表
    stopwords = ['是', '的', '与', '中', '了', '后', '有', '对', '就', '出', '都', '到', '会']  # 第作为停用词实验
    biaodian = ['·', '》', '《', '：', '，', '“', '”', '（', '）', '-', '+', '～', '(', ')', '!', '×', '·', ',', '，', '、', '*',
                '？', '是', '的', '与', '中', '了', '后', '有', '对', '就', '出', '都', '到', '会']
    for word in qa_list:
        if word not in biaodian:
            new_list.append(word)
    return new_list

"""
# 方法：获取一个问题的疑问词和关键词
# 环境配置：无
# 输入参数说明：Ql：问题词list，question_words：疑问词列表
# 输出参数说明：QWlist:某个问题的疑问词list，keyword：某个问题的关键词列表
# 其他：keyword有占位，没有关键词的位置为'null'
"""
def getkeywordlist(Ql,question_words):
    keyword = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
    QWlist = []
    if list(set(Ql).intersection(set(question_words))):
        for i in range(0, len(Ql)):
            if Ql[i] in question_words:
                qw = Ql[i]
                QWlist.append(Ql[i])
                if len(QWlist) == 1:
                    if i == 0 and len(Ql)>=2:
                        keyword[2] = Ql[i + 1]
                        if len(Ql) >= 3:
                            keyword[3] = Ql[i + 2]

                    elif i == 1:
                        keyword[1] = Ql[i - 1]
                        if len(Ql) == 3:
                            keyword[2] = Ql[i + 1]
                        elif len(Ql) >= 4:
                            keyword[2] = Ql[i + 1]
                            keyword[3] = Ql[i + 2]
                    elif i >= 2:
                        keyword[0] = Ql[i - 2]
                        keyword[1] = Ql[i - 1]
                        if len(Ql) - 1 - i >= 2:
                            keyword[2] = Ql[i + 1]
                            keyword[3] = Ql[i + 2]
                        elif len(Ql) - 1 - i == 1:
                            keyword[2] = Ql[i + 1]
                elif len(QWlist) == 2:
                    if i >= 2:
                        keyword[4] = Ql[i - 2]
                        keyword[5] = Ql[i - 1]
                        if len(Ql) - 1 - i >= 2:
                            keyword[6] = Ql[i + 1]
                            keyword[7] = Ql[i + 2]
                        elif len(Ql) - 1 - i == 1:
                            keyword[6] = Ql[i + 1]
    else:
        keyword[2] = Ql[len(Ql) - 2]
        keyword[3] = Ql[len(Ql) - 1]
    print '---------------------keyword-------------------------'
    keyword_str = '\t'.join(keyword)
    print keyword_str
    return QWlist,keyword

def getkeywordlistv2(Ql,question_words):
    keyword = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
    QWlist = []#存疑问词以及其下标组成的list，[疑问词,下标]
    qwlist=[]
    if list(set(Ql).intersection(set(question_words))):
        #抽取每个句子的疑问词
        for m in range(0, len(Ql)):
            if Ql[m] in question_words:
                qwlist.append(Ql[m])
                QWlist.append([Ql[m],m])
        # for i in range(0, len(Ql)):
        if len(QWlist) == 1:
            i=QWlist[0][1]
            if i==0 and len(Ql)>=2:
                keyword[2]=Ql[i+1]
                if len(Ql)>=3:
                    keyword[3] = Ql[i + 2]

            elif i==1 :
                keyword[1] = Ql[i -1]
                if len(Ql) == 3:
                    keyword[2] = Ql[i + 1]
                elif len(Ql) >=4:
                    keyword[2] = Ql[i + 1]
                    keyword[3] = Ql[i + 2]
            elif i>=2:
                keyword[0] = Ql[i - 2]
                keyword[1] = Ql[i - 1]
                if len(Ql)-1-i>=2:
                    keyword[2] = Ql[i + 1]
                    keyword[3] = Ql[i + 2]
                elif len(Ql) - 1 - i ==1:
                    keyword[2] = Ql[i + 1]

        elif len(QWlist) == 2:
            i = QWlist[0][1]
            j=QWlist[1][1]
            if i+1>2:
                keyword[0] = Ql[i - 2]
                keyword[1] = Ql[i - 1]
                if len(Ql)-j>2:
                    keyword[6] = Ql[j + 1]
                    keyword[7] = Ql[j + 2]
                    if j-i>4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j-i==4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j-i==3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j-i==2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql) - j == 2:
                    keyword[6] = Ql[j + 1]
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql)-j==1:
                    if j-i>4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j-i==4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j-i==3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j-i==2:
                        keyword[2] = Ql[i + 1]
            if i + 1 == 2:
                keyword[1] = Ql[i - 1]
                if len(Ql) - j > 2:
                    keyword[6] = Ql[j + 1]
                    keyword[7] = Ql[j + 2]
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql) - j == 2:
                    keyword[6] = Ql[j + 1]
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql) - j == 1:
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
            if i + 1 ==1:
                if len(Ql) - j > 2:
                    keyword[6] = Ql[j + 1]
                    keyword[7] = Ql[j + 2]
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql) - j == 2:
                    keyword[6] = Ql[j + 1]
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]
                elif len(Ql) - j == 1:
                    if j - i > 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                        keyword[5] = Ql[j - 1]
                    elif j - i == 4:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                        keyword[4] = Ql[j - 2]
                    elif j - i == 3:
                        keyword[2] = Ql[i + 1]
                        keyword[3] = Ql[i + 2]
                    elif j - i == 2:
                        keyword[2] = Ql[i + 1]

    else:
        keyword[2] = Ql[len(Ql) - 2]
        keyword[3] = Ql[len(Ql) - 1]
    print '---------------------keyword-------------------------'
    keyword_str = '\t'.join(keyword)
    print keyword_str
    print qwlist
    return qwlist,keyword
"""
# 方法：获取答案的映射词匹配特征，同义词匹配特征
# 环境配置：无
# 输入参数说明：qa_file：问题答案对文件,q_words_dic：疑问词词典文件,map_word_dic：映射词词典文件,
              out_file1：映射词特征保存文件名,out_file2：同义词特征保存文件名
# 输出参数说明：
# 其他：keyword有占位，没有关键词的位置为'null'
"""
def getkeywordfeature(qa_file,q_words_dic,map_word_dic,out_file1,out_file2):
    print '加载疑问词字典...'
    question_words = buildqword(q_words_dic)

    print '加载映射词字典...'
    map_words = buildmapwords(map_word_dic)

    print '加载同义词字典...'
    doc_all = []  # previous dictionary.-special format
    old_dictionary = {}  # previous dictionary
    new_dictionary = {}  # an empty dictionary.
    hsj.index_setup(dic_path+'hagongda-6_1.txt',old_dictionary,new_dictionary, doc_all)

    with open(qa_file) as qa_file:
        out_file1 = open(out_file1,'w')
        out_file2 = open(out_file2,'w')
        step = 0
        temp = ''
        for line in qa_file:
            # step += 1
            # if step == 4:
            #     break
            line_s = line.split('JSSGNHSJLXA')
            line_q = line_s[1].strip().split('\t')
            line_a = line_s[2].strip().split('\t')

            line_q = exstopword(line_q)
            line_a = exstopword(line_a)

            if temp is not line_s[1]:
                temp = line_s[1]
                Qwlist,keywords = getkeywordlistv2(line_q,question_words)

                # print Qwlist
                no_null_keywords = []
                for key_word in keywords:
                    if key_word is not 'null':
                        no_null_keywords.append(key_word)
                # get question words and key words
                all_keywords = Qwlist+no_null_keywords
                q_map_words = getmapwordfeature(all_keywords,map_words)

                q_sim_words = hsj.synonym_generator(old_dictionary, new_dictionary, all_keywords)

                print 'sim words:'
                # print '\t'.join(q_sim_words)
            a_map_words = 0
            a_sim_words = 0
            if len(q_map_words) != 0 or len(q_sim_words) != 0:
                for word in line_a:
                    # print q_map_words
                    # print q_sim_words
                    # print word.strip()
                    # print q_sim_words
                    # for wor in q_sim_words:
                    #     print '---'+wor
                    #     break
                    if word in q_map_words:
                        print '--match--'
                        print word
                        a_map_words += 1
                    if unicode(word, "utf8") in q_sim_words:
                        print '--match_sim--'
                        print word
                        a_sim_words += 1
            else:
                print 'set is null'
            out_file1.write(str(a_map_words)+'\n')
            out_file2.write(str(a_sim_words)+'\n')
        out_file1.close()
        out_file2.close()


"""
# 方法：统计每个问题和问题的答案数量
# 环境配置：无
# 输入参数说明：in_file:问题答案对文件，out_file：问题和答案数量字典
# 输出参数说明：无
# 其他：
"""
def getQandnum(in_file,out_file):
    q_num_dic = []
    q_index = {}
    last_index = 0
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('\t')
            if line_s[0] in q_index.keys():
                q_num_dic[q_index[line_s[0]]][1] += 1
            else:
                q_num_dic.append([line_s[0],1])
                q_index[line_s[0]] = last_index
                last_index += 1
    out_file = open(out_file,'w')
    for q_num in q_num_dic:
        out_file.write(q_num[0]+'\t'+str(q_num[1])+'\n')
    out_file.close()

"""
问题分类
1。正常
2。复述
3。傻b
4。2个疑问词
"""
def addorederfordata(in_file,out_file):
    with open(in_file) as in_file:
        out_file = open(out_file, 'w')
        order = 1
        for line in in_file:
            out_file.write(str(order)+'\t'+line)
            order+=1
        out_file.close()
""""""
def getQandnumorder(in_file,out_file):
    q_num_dic = []
    q_index = {}
    last_index = 0
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('JSSGNHSJLXA')
            if line_s[1] in q_index.keys():
                q_num_dic[q_index[line_s[1]]][1].append(line_s[0])
            else:
                q_num_dic.append([line_s[1],[line_s[0]]])
                q_index[line_s[1]] = last_index
                last_index += 1
    out_file = open(out_file,'w')
    order = 1
    for q_num in q_num_dic:
        q_order_list_str = '\t'.join(q_num[1])
        print q_order_list_str
        out_file.write('JSSGNHSJLXA'+str(order)+'JSSGNHSJLXA'+q_order_list_str+'\n')
        order += 1
    out_file.close()

"""
# 方法：提取问题和答案内容相同的行
# 环境配置：无
# 输入参数说明：in_file：问题、答案对文件，out_file：保存文件
"""
def getfushu(in_file,out_file):
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        temp_quesition = ''
        for line in in_file:
            line_s = line.split('\t')
            # print line_s[1].strip().replace('。','')
            if line_s[0].strip().replace('.？','').replace('？','')==line_s[1].strip().replace('。',''):
                print line_s[0]+'LXA'+line_s[1]
                if temp_quesition is not line_s[0]:
                    out_file.write(line_s[0]+'LXA'+line_s[1])
                    temp_quesition = line_s[0]
    out_file.close()

def gettwoquestion(in_file,q_words_dic,out_file):
    print '加载疑问词字典...'
    question_words = buildqword(q_words_dic)
    with open(in_file) as qa_file:
        out_file = open(out_file,'w')
        temp = ''
        for line in qa_file:
            line_s = line.split('JSSGNHSJLXA')
            if temp is not line_s[2]:
                line_q = line_s[2].strip().split('\t')
                line_q = exstopword(line_q)
                temp = line_s[2]
                Qwlist, keywords = getkeywordlist(line_q, question_words)
                if len(Qwlist) >= 2:
                    print Qwlist
                    out_file.write('JSSGNHSJLXA'+line_s[1]+'JSSGNHSJLXA'+line_s[2])
        out_file.close()

def getmormalquestion(in_file1,fushu_file,twoword_file,out_file):
    fushu_file = open(fushu_file)
    twoword_file = open(twoword_file)
    fushu_dic = set()
    for line in fushu_file:
        fushu_dic.add(line.strip())
    fushu_file.close()
    twoword_dic = set()
    for line in twoword_file:
        line_s = line.strip().split('JSSGNHSJLXA')
        twoword_dic.add(line_s[2].strip())
    twoword_file.close()
    out_file = open(out_file,'w')
    in_file1 = open(in_file1)
    for line in in_file1:
        line_s = line.split('JSSGNHSJLXA')
        print line_s[2]
        # for fushu in fushu_dic:
        #     print fushu
        #     break
        if line_s[2].strip() in fushu_dic:
            print '-------------'
            print line[2]
            continue
        if line_s[2].strip() in twoword_dic:
            print '-------------'
            print line[2]
            continue
        out_file.write('JSSGNHSJLXA'+line_s[1]+'JSSGNHSJLXA'+line_s[2])
    out_file.close()
    in_file1.close()

def buildfile(q_file1,a_file,out_file):
    q_file1 = open(q_file1)
    a_file = open(a_file)
    out_file = open(out_file,'w')
    for q,a in zip(q_file1,a_file):
        out_file.write('JSSGNHSJLXA'+q.strip()+'JSSGNHSJLXA'+a.strip()+'\n')
    out_file.close()
    q_file1.close()
    a_file.close()

def getmeteorfeature(q_file,a_file,out_file):
    import commands
    path = '/Users/liuxiaoan/Downloads/meteor-1.5/'
    # stdout.write('i have a dream')
    command = 'java -Xmx2G -jar ' + path + 'meteor-1.5.jar ' \
              + q_file + a_file +' -l en -norm'
    # os.system('java -Xmx2G -jar /Users/liuxiaoan/Downloads/meteor-1.5/meteor-1.5.jar /Users/liuxiaoan/Downloads/meteor-1.5/example/xray/system1.hyp /Users/liuxiaoan/Downloads/meteor-1.5/example/xray/reference -l en -norm')
    status, output = commands.getstatusoutput(command)
    file = open(out_file, 'w')
    for line in output:
        file.write(line)
    file.close()

def confile(file1,file2,out_file):
    file1 = open(file1)
    file2 = open(file2)
    out_file = open(out_file,'w')
    for line1,line2 in zip(file1,file2):
        score = int(line1) + int(line2)
        out_file.write(str(score)+'\n')
    out_file.close()
    file1.close()
    file2.close()

def departfile(in_file,out_file1,out_file2):
    out_file1 = open(out_file1,'w')
    out_file2 = open(out_file2,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('JSSGNHSJLXA')

def getaward(in_file,out_file):
    pat1 = "(..)*(获得什么|什么奖项)(..)*"  # 两个..表示一个中文字

    pat2 = "\d{1,4}年(..){0,4}获得(..){1,20}"  # 两个..表示一个中文字
    pat3 = "(..){1,20}获(..){1,50}奖(..){1,60}"
    pat4 = "\d{1,4}年荣获(..){1,22}"
    pat5 = "\d{1,4}年(..){1,25}奖"
    pat6 = "(..){1,25}获得(..){1,20}"
    pat7 = "(..)*(获|年)(..){0,25}奖(..)*"
    pat8 = "(..){1,30}奖(..){0,7}"
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.strip().split('\t')
            numflag = 0
            res1 = re.search(pat1.encode('utf'), line_s[0].encode('utf'))
            res2 = re.search(pat2.encode('utf'), line_s[1].encode('utf'))
            res3 = re.search(pat3.encode('utf'), line_s[1].encode('utf'))
            res4 = re.search(pat4.encode('utf'), line_s[1].encode('utf'))
            res5 = re.search(pat5.encode('utf'), line_s[1].encode('utf'))
            res6 = re.search(pat6.encode('utf'), line_s[1].encode('utf'))
            res7 = re.search(pat7.encode('utf'), line_s[1].encode('utf'))
            res8 = re.search(pat8.encode('utf'), line_s[1].encode('utf'))

            if res1 is not None:
                if res2 is not None:
                    numflag += 1
                elif res3 is not None:
                    numflag += 1
                elif res4 is not None:
                    numflag += 1
                elif res5 is not None:
                    numflag += 1
                elif res6 is not None:
                    numflag += 1
                elif res7 is not None:
                    numflag += 1
                elif res8 is not None:
                    numflag += 1
            print numflag
            if numflag > 0:
                out_file.write('1\n')
            else:
                out_file.write('0\n')
        out_file.close()

def gettop(in_file,top,out_file):
    out_file = open(out_file, 'w')
    with open(in_file) as in_file:
        score_map = []
        for line in in_file:
            line_s = line.split('\t')
            # print line_s[1]
            score_map.append([int(line_s[0]),float(line_s[1].strip())])
    score_map = sorted(score_map, key=lambda x: x[1],reverse=True)
    for score in score_map:
        if score[0] < 200000:
            out_file.write(str(score[0])+'\t'+str(score[1])+'\n')


# token.wordcutzhcnq(source_path+'ques1_fusu.txt',source_path+'ques1_fusu')

# 'ques1+ans1
# getQandnum(source_path+'nlpcc-2017.dbqa.testset',statistic_path+'question_num.txt')
# readfile(source_path+'key_test.txt',source_path+'key_test_utf.txt')
# buildqword(source_path+'key_key.txt')


# addorederfordata(source_path+'/4/ques1+ans1',source_path+'/4/order+ques1+ans1.txt')
# getQandnumorder(source_path+'/4/order+ques1+ans1.txt',source_path+'/4/order_q_a_map.txt')
# getfushu(source_path+'nlpcc-2017.dbqa.testset',source_path+'ques1_fusu.txt')
# gettwoquestion(source_path+'order+ques1.txt',dic_path+'question_word.txt',source_path+'ques1_2qword.txt')
# getmormalquestion(source_path+'order+ques1.txt',source_path+'ques1_fushu',
#                   source_path + 'ques1_2qword.txt',source_path+'order+ques1+normal.txt')
# confile(feature_path+'test2016_mapword_feature.txt',feature_path+'test2016_simword_feature.txt',
#         feature_path+'test2016_simmapword_feature.txt')
# getmeteorfeature(source_path+'2016TEST/ques1',source_path+'2016TEST/ans1',feature_path+'test2016_meteor')

# getaward(source_path+'nlpcc-2017.dbqa.testset',feature_path+'test_award_feature.txt')
# buildfile(source_path+'2016TRAIN/ques1',source_path+'2016TRAIN/ans1',source_path+'2016_train_q_a')
"""
计算数字特征和映射词、同近义词特征
"""
# catchbynum(source_path+'/4/ques1+ans1+type4+label',feature_path+'/type4/3w_num_feature.txt')
# getkeywordfeature(source_path+'/4/ques1+ans1+type4+label',dic_path+'question_word.txt',dic_path+'key_key.txt',
#                   feature_path+'/type4/3w_mapword_feature.txt',feature_path+'/type4/3w_simword_feature.txt')

"""
构建原始问题答案对索引文件
"""
def buildindexqa(in_file,out_file):
    q_num_dic = []
    q_index = {}
    last_index = 0
    with open(in_file) as in_file:
        line_num = 1
        for line in in_file:
            line_s = line.strip().split('\t')
            if line_s[0] in q_index.keys():
                q_num_dic[q_index[line_s[0]]][1].append(str(line_num))
            else:
                q_num_dic.append([line_s[0],[str(line_num)]])
                q_index[line_s[0]] = last_index
                last_index += 1
            line_num += 1
    out_file = open(out_file,'w')
    for q_num in q_num_dic:
        q_order_list_str = '\t'.join(q_num[1])
        out_file.write(q_num[0]+'JSSGNHSJLXA'+q_order_list_str+'\n')
    out_file.close()

"""
根据top10序号获取问题
"""
def getquestionbynum(in_file,cut_list):
    line_num = 1
    q_list = set()
    with open(in_file) as in_file:
        for line in in_file:
            if line_num in cut_list:
                line_s = line.strip().split('\t')
                q_list.add(line_s[0].strip())
                print line_s[0].strip()
            line_num += 1
    return q_list
"""
根据top10序号问题获取对应答案
"""
def getqalistbynum(in_file,q_list,cut_list):
    a_list = []
    l_list = []
    with open(in_file) as in_file:
        line_num = 1
        for line in in_file:
            line_s = line.strip().split('JSSGNHSJLXA')
            if line_s[0].strip() in q_list:
                line_a_li = line_s[1].strip().split('\t')
                for line_a_li_a in line_a_li:
                    a_list.append(int(line_a_li_a))
                    if int(line_a_li_a) in cut_list:
                        l_list.append(1)
                    else:
                        l_list.append(0)
            line_num += 1
    print len(a_list)
    return a_list,l_list

"""
根据答案list，将原始问题答案对对应对文件删除，feature删除
"""
def delqagetfea(in_normalfile,in_feafile,a_list,out_normalfile,out_feafile):
    cut_feature = []
    in_normalfile = open(in_normalfile)
    in_feafile = open(in_feafile)

    out_normalfile = open(out_normalfile,'w')
    out_feafile = open(out_feafile,'w')

    line_num = 1
    for normal,fea in zip(in_normalfile,in_feafile):
        if line_num in a_list:
            cut_feature.append(fea.strip())
        else:
            out_normalfile.write(normal)
            out_feafile.write(fea)
        line_num += 1
    out_normalfile.close()
    out_feafile.close()
    in_normalfile.close()
    in_feafile.close()
    return cut_feature

def addtrain(cut_feature,cut_label,fea_file,label_file,out_feafile,out_labelfile):
    out_feafile = open(out_feafile,'w')
    out_labelfile = open(out_labelfile, 'w')
    fea_file = open(fea_file)
    label_file = open(label_file)
    for fea_line,label_line in zip(fea_file,label_file):
        out_feafile.write(fea_line)
        out_labelfile.write(label_line)
    print len(cut_feature)
    for fea in cut_feature:
        out_feafile.write(fea.strip()+'\n')

    for label in cut_label:
        out_labelfile.write(str(label)+'\n')
    out_feafile.close()
    out_labelfile.close()
    fea_file.close()
    label_file.close()

# buildindexqa(FEA_PATH+'cut11000.txt',FEA_PATH+'q_a_index_del10.txt')

def addtraindeltest(del_normalfile,del_feafile,
                    q_a_indexfile,cut_list,
                    new_normalfile,new_feafile,
                    old_trainfile,new_trainfile,
                    old_labelfile,new_labelfile):
    q_list = getquestionbynum(del_normalfile,cut_list)
    a_list, l_list = getqalistbynum(q_a_indexfile, q_list,cut_list)
    cut_feature = delqagetfea(del_normalfile, del_feafile,
                              a_list, new_normalfile, new_feafile)
    addtrain(cut_feature, l_list,old_trainfile, old_labelfile,new_trainfile,new_labelfile)

# cut_list = [70435,45341,169781,92070,61736,154780,81598,93874,107138,144008]
# addtraindeltest(FEA_PATH+'cut11000.txt',FEA_PATH+'feature_8_del10.txt',
#                 FEA_PATH+'q_a_index_del10.txt',cut_list,
#                 FEA_PATH+'cut11100.txt',FEA_PATH+'feature_8_del20.txt',
#                 FEAtrain_path+'feature_8_add10.txt',FEAtrain_path+'feature_8_add20.txt',
#                 FEAtrain_path+'label_add10.txt',FEAtrain_path+'label_add20.txt')

"""
提取置信度高的问题序号。
"""
test2017_pre_path = '/Users/liuxiaoan/ML/nlpcc2017/MLP/log_3_add_top20/'
addorederfordata(test2017_pre_path+'mlp_20000_1_pre.txt',
                 test2017_pre_path+'mlp_20000_1_pre_order.txt')
gettop(test2017_pre_path+'mlp_20000_1_pre_order.txt',10,test2017_pre_path+'top10.txt')










