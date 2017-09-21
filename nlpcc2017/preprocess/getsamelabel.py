#encoding=utf-8
import tokenizer as token
import jieba

data_path = './train&testdata/'
fenci_path = './fenci/'
statistic_path = './statistic/'
"""
# 方法：提取问题和答案内容相同的行
# 环境配置：无
# 输入参数说明：in_file：问题、答案对文件，out_file：保存文件
"""
def getsamelabel(in_file,out_file):
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            if line_s[0].strip() is line_s[1].strip():
                print line_s
                out_file.write(line)
    out_file.close()

"""
# 方法：提取人工标记的结果
# 环境配置：无
# 输入参数说明：in_file：问题、答案对文件，out_file1：label保存文件，out_file2:问题和label保存文件
# 需要对没有标记正确答案对问题进行去除
"""

def getlabels(in_file,out_file1,out_file2):
    with open(in_file) as in_file:
        out_file1 = open(out_file1, 'w')
        out_file2 = open(out_file2, 'w')
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            if line_s[0] == '1':
                out_file1.write('1'+'\n')
                out_file2.write(line_s[1]+'JSSGNHSJLXA' + '1\n')
            else:
                out_file1.write('0'+'\n')
                out_file2.write(line_s[1] + 'JSSGNHSJLXA' + '0\n')
        out_file1.close()
        out_file2.close()

"""
# 方法：提取人工标记的结果
# 环境配置：无
# 输入参数说明：in_file：问题、答案对文件，out_file1：label保存文件，out_file2:问题和label保存文件
# 需要对没有标记正确答案对问题进行去除
"""
# def get1data(in_file,out_file):


# getsamelabel(data_path+'nlpcc-iccpol-2016.dbqa.testing-data',statistic_path+'q_a_same.txt')

getlabels(data_path+'ourlabel.txt',data_path+'our_label.txt',data_path+'our_qalabel.txt')

