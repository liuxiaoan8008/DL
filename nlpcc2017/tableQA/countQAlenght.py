# coding=UTF-8
import re

print '=============start============='
print '=============get qa full string  lenght============='
fenci_path = './data/'
statistic_path = './statistic/'
# QL = open(fenci_path+'lpcc-iccpol-2016-question-one.dbqa.fenci.training-data')
CAL = open(fenci_path+'train_cells.txt')
LL=CAL
linelenght1={}
linelenght2={}
for lline in LL :
    llist = lline.split('_||_')
    llen=len(llist)
    if llen not in linelenght1:
        linelenght1[llen]=1
    else:
        linelenght1[llen] = linelenght1[llen]+1

    lline_stop = re.sub('[\W]|[\d]|\n', ' ', lline)
    llen_stop=len(lline_stop.split())
    if llen_stop not in linelenght2.keys():
        linelenght2[llen_stop]= 1
    else:
        linelenght2[llen_stop] += 1


print '所有词句子长度大小',len(linelenght1)
print '所有词句子长度最小',min(linelenght1.items(), key=lambda x: x[1])
print '所有词句子长度最大',max(linelenght1.items(), key=lambda x: x[1])


print '去掉符号和数字句子长度大小',len(linelenght2)
print '去掉符号和数字句子长度最小',min(linelenght2.items(), key=lambda x: x[1])
print '去掉符号和数字句子长度最大',max(linelenght2.items(), key=lambda x: x[1])
len1=''
len2=''
with open(statistic_path+'att_all_lenght.txt','w') as wo1:
    for llen in linelenght1:
        len1=len1+str(llen)+' : '+str(linelenght1[llen])+'\n'
    wo1.write(len1)
with open(statistic_path+'att_no_symbol_lenght.txt','w') as wo2:
    for llen in linelenght2:
        len2=len2+str(llen)+' : '+str(linelenght2[llen])+'\n'
    wo2.write(len2)