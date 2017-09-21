# coding=UTF-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def getkeywordlist(Ql,question_words):
    keyword = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
    QWlist = []#存疑问词以及其下标组成的list，[疑问词,下标]
    qwlist=[]
    if list(set(Ql).intersection(set(question_words))):
        #抽取每个句子的疑问词
        for m in range(0, len(Ql)):
            if Ql[m] in question_words:
                qwlist.append(question_words)
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
    return qwlist,keyword
#构建疑问词列表
question_words=[]
questionwords=open('E:/Data/NLPCC2017/question_word.txt')
for word in questionwords:
    if word.strip() not in question_words:
        question_words.append(word.strip())
#停用词和标点符号表
biaodian=['·','》','《','：','，','“','”','（','）','-','+','～','(',')','!','×','·',',','，','、','*','？','是', '的', '与',  '中', '了', '后', '有', '对', '就', '出','都','到','会']
print '=============start============'
path='E:/Data/NLPCC2017/TEST2017/NLPCC2017/DBQA/FENCI/2/'
outpath='E:/Data/NLPCC2017/TEST2017/NLPCC2017/DBQA/saerchKeyWord/2/'
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
all_keyword=[]
all_keyw=''
for QLl in allQlist:
    keyword=getkeywordlist(QLl, question_words)
    all_keyword.append(keyword[1])

#使用关键词去答案中检索，并计分
two_three=''
one_two_three=''
one_two_three_four=''
six_seven=''
five_six_seven=''
two_three_six_seven=''
five_six_seven_eight=''
one_two_three_four_five_six_seven_eight=''
for kw ,al in zip(all_keyword,allAlist):
    search_kw=[0]*8
    for i in range(0,8):
        for aw in al:
            if aw==kw[i]:
                search_kw[i]+=1

    two_three+=str(search_kw[1]+search_kw[2])+'\n'
    one_two_three+=str(search_kw[0]+search_kw[1]+search_kw[2])+'\n'
    one_two_three_four+=str(search_kw[0]+search_kw[1]+search_kw[2]+search_kw[3])+'\n'
    six_seven+=str(search_kw[5]+search_kw[6])+'\n'
    five_six_seven +=str(search_kw[4]+search_kw[5]+search_kw[6])+'\n'
    two_three_six_seven +=str(search_kw[1]+search_kw[2]+search_kw[5]+search_kw[6])+'\n'
    five_six_seven_eight += str(search_kw[4]+search_kw[5]+search_kw[6]+search_kw[7]) + '\n'
    one_two_three_four_five_six_seven_eight +=str(search_kw[0]+search_kw[1]+search_kw[2]+search_kw[3]+search_kw[4]+search_kw[5]+search_kw[6]+search_kw[7])+'\n'


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