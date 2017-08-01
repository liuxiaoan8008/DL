#encoding=utf-8
import re
import sys
import codecs
from zhon import hanzi,pinyin
import chardet

def myfun(input_file):
    '''
    繁体转简体后，一些符号修正。
    :param input_file:
    :return: new file
    '''
    p1 = re.compile(ur'-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
    p2 = re.compile(ur'[（\(][，；。？！\s]*[）\)]')
    p3 = re.compile(ur'[「『]')
    p4 = re.compile(ur'[」』]')
    outfile = codecs.open('std_' + input_file, 'w', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            line = p1.sub(ur'\2', line)
            line = p2.sub(ur'', line)
            line = p3.sub(ur'“', line)
            line = p4.sub(ur'”', line)
            outfile.write(line)
    outfile.close()
    print 'finish file :',input_file

def getline(input_file):
    '''
    去掉标点符号，形成word2vec的输入
    :param input_file:
    :return:
    '''
    outfile = codecs.open('in_' + input_file, 'w', 'utf-8')
    punc = re.compile(ur'[，；。？！＃＄％＆＇（）＊＋，·－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.\s]')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            if len(line.strip()) == 0:
                continue
            sublines = re.findall(hanzi.sentence,line)
            for l in sublines:
                l = punc.sub(' ',l) # 去标点符号
                l = re.sub('[ ]+',' ',l) # 去掉重复掉空格
                if len(l.strip()) == 0:
                    continue
                else:
                    outfile.write(l.strip()+'\n')

# getline('./data/wiki_test')
getline('std_zh_wiki_00')
getline('std_zh_wiki_01')
getline('std_zh_wiki_02')
# myfun('wiki_00')
# myfun('wiki_01')
# myfun('wiki_02')




