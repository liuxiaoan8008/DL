# coding=UTF-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#构建疑问词列表
question_words=[]
questionwords=open('E:/Data/NLPCC2017/question_word.txt')
for word in questionwords:
    if word.strip() not in question_words:
        question_words.append(word.strip())

#停用词和标点符号表
stopwords = ['是', '的', '与',  '中', '了', '后', '有', '对', '就', '出','都','到','会']#第作为停用词实验
biaodian=['·','》','《','：','，','“','”','（','）','-','+','～','(',')','!','×','·',',','，','、','*','？','是', '的', '与',  '中', '了', '后', '有', '对', '就', '出','都','到','会']

path='E:/Data/NLPCC2017/Fen_Ci/test2017/'
outpath='E:/Data/NLPCC2017/TEST2017/NLPCC2017/DBQA/saerchKeyWord/'
QL=open(path+'ques1')
CAL=open(path+'ans1')

allQ=''
allQlist=[]
allAlist=[]
#将每个问题和答案去掉停用词存入list
for ql,al in zip(QL,CAL):
    qline =  ql.split()
    qlist=[]
    for w in qline:
        if w not in biaodian:
            qlist.append(w)
    allQlist.append(qlist)
    allAlist.append(al.split())

#构建每个问题的关键词表，疑问词左右各两个词
# all_qw=[]
all_keyword=[]
all_keyw=''


def getkeywordlist(Ql,question_words):
    keyword = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
    QWlist = []
    if list(set(Ql).intersection(set(question_words))):
        for i in range(0, len(Ql)):
            if Ql[i] in question_words:
                qw = Ql[i]
                # q_w[0] = i
                # q_w[1] = len(Ql)
                # q_w[2] = Ql[i]
                QWlist.append(Ql[i])
                # all_qw.append(q_w)
                if len(QWlist) == 1:
                    if i == 0:
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
    print keyword
    return keyword


for Ql in allQlist:
    getkeywordlist()
    #把所有的关键词存入文件
    # all_keyw+=qw+' '+keyword[0]+' '+keyword[1]+' '+keyword[2]+' '+keyword[3]+keyword[4]+' '+keyword[5]+' '+keyword[6]+' '+keyword[7]+'\n'
    # 把所有的关键词存入list  all_keyword
    all_keyword.append(keyword)
# with open('E:/Data\NLPCC2017/saerchKeyWord/hsj/KeyWordV2','w') as keyfile:
#     keyfile.write(all_keyw)
all_search_ky=[]
allsearchkw=''
two_three=''
one_two_three=''
one_two_three_four=''
six_seven=''
five_six_seven=''
two_three_six_seven=''
five_six_seven_eight=''
one_two_three_four_five_six_seven_eight=''
#使用关键词去答案中检索，并计分
for kw ,al in zip(all_keyword,allAlist):
    search_kw=[0]*8
    for i in range(0,8):
        for aw in al:
            if aw==kw[i]:
                search_kw[i]+=1
    for n in search_kw:
        allsearchkw+=str(n)+' '
    allsearchkw +='\n'

    two_three+=str(search_kw[1]+search_kw[2])+'\n'
    one_two_three+=str(search_kw[0]+search_kw[1]+search_kw[2])+'\n'
    one_two_three_four+=str(search_kw[0]+search_kw[1]+search_kw[2]+search_kw[3])+'\n'
    six_seven+=str(search_kw[5]+search_kw[6])+'\n'
    five_six_seven +=str(search_kw[4]+search_kw[5]+search_kw[6])+'\n'
    two_three_six_seven +=str(search_kw[1]+search_kw[2]+search_kw[5]+search_kw[6])+'\n'
    five_six_seven_eight += str(search_kw[4]+search_kw[5]+search_kw[6]+search_kw[7]) + '\n'
    one_two_three_four_five_six_seven_eight +=str(search_kw[0]+search_kw[1]+search_kw[2]+search_kw[3]+search_kw[4]+search_kw[5]+search_kw[6]+search_kw[7])+'\n'
    all_search_ky.append(search_kw)

with open(outpath+'saerchKeyWordV1','w')as wo:
    wo.write(allsearchkw)
with open(outpath+'saerchKeyWordV1_2+3','w')as wo1:
    wo1.write(two_three)
with open(outpath+'saerchKeyWordV1_1+2+3','w')as wo2:
    wo2.write(one_two_three)
with open(outpath + 'saerchKeyWordV1_1+2+3+4', 'w')as wo3:
    wo3.write(one_two_three_four)
with open(outpath+'saerchKeyWordV1_6+7','w')as wo4:
    wo4.write(six_seven)

with open(outpath+'saerchKeyWordV1_5+6+7','w')as wo5:
    wo5.write(five_six_seven)
with open(outpath+'saerchKeyWordV1_5+6+7+8','w')as wo6:
    wo6.write(five_six_seven_eight)
with open(outpath+'saerchKeyWordV1_1+2+3+4+5+6+7+8','w')as wo7:
    wo7.write(one_two_three_four_five_six_seven_eight)
with open(outpath+'saerchKeyWordV1_2+3+6+7','w')as wo8:
    wo8.write(two_three_six_seven)
QL.close()
CAL.close()