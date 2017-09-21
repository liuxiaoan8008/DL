#! /usr/bin/env python
# coding: utf
import re
import sys

reload(sys)
sys.setdefaultencoding('utf')

file = open('G:\matchfile\dbqa10000+20737.txt')

matchscore = ''

pat1 = "(..)*(获得什么|什么奖项)(..)*"  # 两个..表示一个中文字

pat2 = "\d{1,4}年(..){0,4}获得(..){1,20}"  # 两个..表示一个中文字
pat3 = "(..){1,20}获(..){1,50}奖(..){1,60}"
pat4 = "\d{1,4}年荣获(..){1,22}"
pat5 = "\d{1,4}年(..){1,25}奖"
pat6 = "(..){1,25}获得(..){1,20}"
pat7 = "(..)*(获|年)(..){0,25}奖(..)*"
pat8 = "(..){1,30}奖(..){0,7}"

for line in file:
    numflag = 0
    res1 = re.search(pat1.encode('utf'), line.encode('utf'))
    res2 = re.search(pat2.encode('utf'), line.encode('utf'))
    res3 = re.search(pat3.encode('utf'), line.encode('utf'))
    res4 = re.search(pat4.encode('utf'), line.encode('utf'))
    res5 = re.search(pat5.encode('utf'), line.encode('utf'))
    res6 = re.search(pat6.encode('utf'), line.encode('utf'))
    res7 = re.search(pat7.encode('utf'), line.encode('utf'))
    res8 = re.search(pat8.encode('utf'), line.encode('utf'))

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

    if numflag > 0:
        matchscore += '1' + '\n'
    else:
        matchscore += '0' + '\n'
print matchscore
