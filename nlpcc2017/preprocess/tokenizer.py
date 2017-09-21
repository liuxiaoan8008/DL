#encoding=utf-8
import jieba
# 中文文本预处理，使用时先复写
# 环境配置：
# 使用：

def lineprocess(line):

    return line

# 中文分词方法，结巴分词
# 环境配置：pip install jieba
# 使用：import jieba


def wordcutzhcn(in_file,out_file1,out_file2,out_file3):

    with open(in_file) as in_file:
        out_file1 = open(out_file1,'w')
        out_file2 = open(out_file2, 'w')
        out_file3 = open(out_file3, 'w')

        for line in in_file:
            line_split = line.split('\t')
            seg_list1 = jieba.cut_for_search(line_split[0])
            seg_list2 = jieba.cut_for_search(line_split[1])
            out_string1 = '\t'.join(seg_list1)
            out_string2 = '\t'.join(seg_list2)
            out_file1.write(out_string1.encode('utf-8')+'\n')
            out_file2.write(out_string2.encode('utf-8') + '\n')
            out_file3.write(str(line_split[2]))
            print out_string1
            print out_string2

        out_file1.close()
        out_file2.close()
        out_file3.close()

# 去停用词方法
# 环境配置：
# 使用：

def exstopwords(in_file,out_file,stop_file='stopwords.dat'):
    with open(in_file) as in_file:
        out_file = open(out_file, 'w')
        # 加载停用词词典
        stop_file = open(stop_file)
        stop_dic = set()
        for line in stop_file:
            stop_dic.add(line) 
        stop_file.close()
        # 去停用词
        for line in in_file:
            ex_words = []
            words = line.split('\t')
            for word in words:
                if word not in stop_dic:
                    ex_words.append(word)
            ex_str = '\t'.join(ex_words)
            # print ex_str
            if len(ex_words) <= 3:
                print ex_str
                ex_str = '\n'
            out_file.write(ex_str)
        out_file.close()

# 中文分词方法（去停用词版），结巴分词
# 环境配置：pip install jieba
# 使用：import jieba

def wordcutzhcnstop(in_file,out_file,stop_file='stopwords.dat'):
    with open(in_file) as in_file:
        out_file = open(out_file, 'w')
        # 加载停用词词典
        stop_file = open(stop_file)
        stop_dic = set()
        for line in stop_file:
            stop_dic.add(line)
        stop_file.close()
        for line in in_file:
            ex_words = []
            seg_list = jieba.cut(line)
            for seg in seg_list:
                if seg not in stop_dic:
                    ex_words.append(seg)
            ex_str = '\t'.join(ex_words)
            print ex_str
            out_file.write(ex_str)
        out_file.close()

# 英文分词方法：
# 环境配置：
# 使用：

def wordcuteng(in_file,out_file):
    return 0

# 词频统计方法
# 环境配置：
# 使用：import collections

def wordcount(in_file,out_file,min_fre):
    import collections
    word_box = []
    word_file = open(in_file)
    for line in word_file:
        # print line
        word_box.extend(line.strip().split(','))
    word_file.close()
    word_map = collections.Counter(word_box)
    out_file = open(out_file, 'w')
    for word in word_map:
        if word_map[word] >= min_fre:
            out_str = word + '\t' + str(word_map[word])
            print out_str
            out_file.write(out_str + '\n')
    out_file.close()

"""
"""
def wordcutzhcnq(in_file,out_file1):
    with open(in_file) as in_file:
        out_file1 = open(out_file1,'w')
        for line in in_file:
            line_split = line.split('LXA')
            seg_list1 = jieba.cut(line_split[0].replace(' ','').replace('第','').replace('是','').replace('有','').strip())
            out_string1 = '\t'.join(seg_list1)
            out_file1.write(out_string1.encode('utf-8')+'\n')
        out_file1.close()

#
def wordcutzhcnstop(in_file,out_file,stop_file='stopwords.dat'):
    with open(in_file) as in_file:
        out_file = open(out_file, 'w')
        # 加载停用词词典
        stop_file = open(stop_file)
        stop_dic = set()
        for line in stop_file:
            stop_dic.add(line)
        stop_file.close()
        for line in in_file:
            ex_words = []
            seg_list = jieba.cut(line)
            for seg in seg_list:
                if seg not in stop_dic:
                    ex_words.append(seg)
            ex_str = '\t'.join(ex_words)
            print ex_str
            out_file.write(ex_str)
        out_file.close()