#encoding=utf-8

source_path = '/Users/liuxiaoan/Desktop/DBQA/'

def addquestiontypeforqa(in_file,qa_type_file,out_file):
    print 'building q_type_dic...'
    qa_type_dic = {}
    with open(qa_type_file) as qa_type_file:
        for line in qa_type_file:
            line_s = line.split('JSSGNHSJLXA')
            qa_type_dic[line_s[2].strip()] = line_s[0].strip()
    out_file = open(out_file,'w')
    count = 0
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            if line_s[1].strip() in qa_type_dic.keys():
                count += 1
                print count
                out_file.write(qa_type_dic[line_s[1].strip()]+line)
            else:
                out_file.write(line)
    out_file.close()

def getatypequstion(in_file,qa_type_file,type,out_file):
    print 'building q_type_dic...'
    qa_type_dic = {}
    with open(qa_type_file) as qa_type_file:
        for line in qa_type_file:
            line_s = line.split('JSSGNHSJLXA')
            try:
                if int(line_s[0].strip())==type:
                    qa_type_dic[line_s[2].strip()] = line_s[0].strip()
            except:
                print line_s[2].strip()
                continue
    out_file = open(out_file, 'w')
    count = 0
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            if line_s[1].strip() in qa_type_dic.keys():
                count += 1
                print count
                out_file.write(line)
    out_file.close()

def addzero(in_file,out_file):
    out_file = open(out_file,'w')
    with open(in_file) as in_file:
        for line in in_file:
            line_s = line.split('JSSGNHSJLXA')
            if line_s[0].strip() is '':
                out_file.write('0'+line)
            else:
                out_file.write(line)

""""""
def addlabel(in_file1,in_file2,out_file):
    in_file1 = open(in_file1)
    in_file2 = open(in_file2)
    out_file = open(out_file,'w')
    for line1,line2 in zip(in_file1,in_file2):
        line1_s = line1.strip().split('JSSGNHSJLXA')
        if line1_s[0].strip() is '':
            out_file.write('0' + line2)
        else:
            out_file.write('1' + line2)
    out_file.close()
    in_file1.close()
    in_file2.close()


# addquestiontypeforqa(source_path+'/4/ques1+ans1',source_path+'question_type.txt',source_path+'/4/ques1+ans1+qtype')

# getatypequstion(source_path+'/4/ourlabel.txt',source_path+'question_type.txt',4,source_path+'/4/ques1+ans1+type4')
# addzero(source_path+'/4/ourlabel.txt',source_path+'/4/ourlabeladdzero')

# addlabel(source_path+'/4/ourlabel.txt',source_path+'/4/q_a_3w',source_path+'/4/q_a_3w_label')