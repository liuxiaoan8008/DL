# -*- coding: utf-8 -*-
# 主要完成以下三个功能：
# (1). 建立索引：首先输入100行字符串，用于构建倒排索引，每行字符串由若干不含标点符号的、全部小写字母组成的单词构成，每个单词之间以空格分隔。
# 依次读入每个单词，并组成一个由<</span>单词, 每个单词出现的行号集合>构成的字典，其中行号从1开始计数。
#
# (2). 打印索引：按照字母表顺序依次输出每个单词及其出现的位置，每个单词出现的位置则按行号升序输出。
# 例如，如果“created”出现在第3, 20行，“dead”分别出现在14, 20, 22行。则输出结果如下（冒号和逗号后面都有一个空格，行号不重复）：
# …
# created: 3, 20
# dead: 14, 20, 22
# …
#
# (3). 检索：接下来输入查询(Query)字符串，每行包含一个查询，每个查询由若干关键字(Keywords)组成，每个关键字用空格分隔且全部为小写字母单词。
# 要求输出包含全部单词行的行号（升序排列），每个查询输出一行。若某一关键字在全部行中从没出现过或没有一行字符串包含全部关键字，则输出“None”。
# 遇到空行表示查询输入结束。
# 如对于上面创建的索引，当查询为“created”时，输出为“3, 20”；当查询为“created dead”时，输出为“20”；当查询为“abcde dead”时，输出为“None”；
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')

'''''Part 1 : Setup index'''

doc_all = []  # previous dictionary.-special format
old_dictionary = {}  # previous dictionary
new_dictionary = {}  # an empty dictionary.

# with open("hagongda-6_1.txt") as file:
# 建立原索引
#     for line in file:
#         line = line.decode('utf8')
#         dictionary_list = line.split(" ")
#         line_set = []
#         line_set.append(dictionary_list[0])
#         line_set.append(line.replace(dictionary_list[0] + " ", "").replace("\r\n", ""))
#         doc_all.append(line_set)
#
#         old_dictionary[dictionary_list[0]] = line.replace(dictionary_list[0] + " ", "").replace("\r\n", "")
#
#
# # print old_dictionary
# # print doc_all;
#
# 建立倒排索引
# for line in doc_all:
#
#     line_words = line[1].split()
#     # split the information inputed into lines by ' '
#
#     for word in line_words:  # Judge every word in every lines .
#
#         # If the word appear the first time .
#         if word not in new_dictionary:
#             item = set()  # set up a new set .
#             item.add(line[0])  # now rows
#             new_dictionary[word] = item  # Add now rows into keys(item).
#
#         # The word has appeared before .
#         else:
#             new_dictionary[word].add(line[0])  # Add now rows into keys(item).
#
# # print new_dictionary  # we can get the information dictionary.

'''''Part 5 :上述方法1的封装——根据词典文件生成原索引和新倒排索引'''


def index_setup(src, dict1, dict2, dict_format):
    # 建立原索引
    with open(src) as dic_file:
        for line in dic_file:
            line = line.decode('utf8')
            dictionary_list = line.split(" ")
            line_set = []
            line_set.append(dictionary_list[0])
            line_set.append(line.replace(dictionary_list[0] + " ", "").replace("\r\n", ""))
            dict_format.append(line_set)
            dict1[dictionary_list[0]] = line.replace(dictionary_list[0] + " ", "").replace("\r\n", "")

    # print old_dictionary
    # print doc_all;

    # 建立倒排索引
    for line in dict_format:

        line_words = line[1].split()
        # split the information inputed into lines by ' '

        for word in line_words:  # Judge every word in every lines .

            # If the word appear the first time .
            if word not in dict2:
                item = set()  # set up a new set .
                item.add(line[0])  # now rows
                dict2[word] = item  # Add now rows into keys(item).

            # The word has appeared before .
            else:
                dict2[word].add(line[0])  # Add now rows into keys(item).

                # print dict2  # we can get the information dictionary.

# index_setup("hagongda-6_1.txt", old_dictionary, new_dictionary, doc_all)

'''''Part 2 : Print index'''
#
# word_list = dictionary.items()  # Get dict's items .
#
# word_list.sort(key=lambda items: items[0])  # Sort by word in dict.
#
# for word, row in word_list:  # Ergodic word and row in word_list .
#
#     list_row = dictionary(row)
#     list_row.sort()
#
#     # Change int row into string row .
#     for i in range(0, len(list_row)):
#         list_row[i] = str(list_row[i])
#
#         # print result the part 2 needed .
#     print word + ':', ', '.join(list_row)
#
# print dictionary
# with open("test_index.txt", "w") as f:
#     for i in dictionary:
#         f.write(i)
#         for j in dictionary[i]:
#             f.write(" "+str(j))
#         f.write("\n")

''''' Part 3 : Query '''


# define judger to judger if all querys are in dict.
def judger(dict, query):
    list_query = query.split()
    for word in list_query:
        if word not in dict:
            return 0  # for every query ,if there is one not in dict,return 0
    return 1  # all query in dict .


query_list = []

# # for input , meet '' ,stop input.
# i = 0
# while i < 2:
#     i += 1
#     query = raw_input()
#     query = query.decode("utf8")
#     if query == '':
#         break
#     elif len(query) != 0:
#         query_list.append(query)  # append query inputed to a list query_list .
#
# # Ergodic every query in query_list.
# for list_query in query_list:
#
#     # if judger return 0.
#     a = list_query.decode("utf8")
#     if judger(new_dictionary, a) == 0:
#         print 'None'
#
#     else:
#         list_query = list_query.split()
#         query_set = set()  # get a empty set
#
#         # union set to get rows .
#         for isquery in list_query:
#             query_set = query_set | new_dictionary[isquery]
#
#             # intersection to get common rows .
#         for isquery in list_query:
#             query_set = query_set & new_dictionary[isquery]
#
#             # if intersection == 0
#         if len(query_set) == 0:
#             print 'None'
#
#         else:
#             query_result = list(query_set)
#             query_result.sort()
#             for m in range(len(query_result)):
#                 query_result[m] = str(query_result[m])
#
#             print ', '.join(query_result)
#             synonyms = []
#
#             for synonym in query_result:
#                 synonyms.append(old_dictionary[synonym])
#                 # print old_dictionary[synonym]
#                 # print "\n"
#             print synonyms


''''' Part 4 : 上述方法3的封装——搜索倒排索引 '''


def synonym_generator(dict1, dict2, q_a_list):
    # dict1-原同近义词典，dict2-倒排索引
    synonyms_all = set()  # an empty set
    for q_a in q_a_list:
        a = q_a.decode("utf8")
        # if judger return 0
        if judger(dict2, a) == 0:
            print "None"
        else:
            query_set = set()  # get a empty set
            query_set = dict2[a]

            if len(query_set) == 0:
                print 'None'
            else:
                query_result = list(query_set)
                query_result.sort()
                for m in range(len(query_result)):
                    query_result[m] = str(query_result[m])

                # print ', '.join(query_result)
                synonyms_small = set()  # 一个关键词的同义词集合

                for synonym in query_result:
                    try:
                        synonyms_small.add(dict1[synonym])
                    except:
                        print synonym.replace('root:﻿','').strip()
                        # logging.warn(synonym)
                        # exit(0)

                synonyms_small_split = set()
                for i in synonyms_small:
                    i_split = i.split(" ")
                    for i_i in i_split:
                        synonyms_small_split.add(i_i.strip())

            synonyms_all = synonyms_all | synonyms_small_split
    return synonyms_all

# synonym_generator(old_dictionary, new_dictionary, ["思念", "真挚"])