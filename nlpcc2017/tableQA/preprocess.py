#encoding=utf-8

def cutinfo(in_file,label_file,q_f,d_f,a_f,c_f):
    in_file = open(in_file)
    # label_file = open(label_file,'w')
    q_f = open(q_f,'w')
    d_f = open(d_f,'w')
    a_f = open(a_f,'w')
    c_f = open(c_f,'w')
    count = 0
    for line in in_file:
        count += 1
        print count
        line_s = line.split('\t')
        # label_file.write(line_s[0]+'\n')
        q_f.write(line_s[0]+'\n')
        d_f.write(line_s[1]+'\n')
        a_f.write(line_s[2]+'\n')
        c_f.write(line_s[3])
    # label_file.close()
    q_f.close()
    d_f.close()
    a_f.close()
    c_f.close()

data_path = './data/'
feature_path = './feature/'

# cutinfo(data_path+'nlpcc-2017.tbqa.testset',data_path+'train_label.txt',
#         data_path+'test_question.txt',data_path+'test_description.txt',
#         data_path+'test_attributes.txt',data_path+'test_cells.txt')

def getmeteorfeature(q_file,a_file,out_file):
    import commands
    path = '/Users/liuxiaoan/Downloads/meteor-1.5/'
    # stdout.write('i have a dream')
    command = 'java -Xmx2G -jar ' + path + 'meteor-1.5.jar ' \
              + q_file +' '+a_file +' -norm'
    # os.system('java -Xmx2G -jar /Users/liuxiaoan/Downloads/meteor-1.5/meteor-1.5.jar /Users/liuxiaoan/Downloads/meteor-1.5/example/xray/system1.hyp /Users/liuxiaoan/Downloads/meteor-1.5/example/xray/reference -l en -norm')
    status, output = commands.getstatusoutput(command)
    file = open(out_file, 'w')
    for line in output:
        file.write(line)
    file.close()

def getmetorscore(in_file,out_file):
    out_file = open(out_file, 'w')
    with open(in_file) as in_file:
        for line in in_file:
            if line.startswith('Segment'):
                line_s = line.split(':	')
                out_file.write(line_s[1])
    out_file.close()

getmeteorfeature(data_path+'test_question.txt',data_path+'test_attributes.txt',feature_path+'test_meteor_q_att.txt')
getmetorscore(feature_path+'test_meteor_q_att.txt',feature_path+'test_meteor_score_q_att.txt')