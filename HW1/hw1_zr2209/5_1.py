#! /usr/bin/python
import math
import sys


with open('ner_rare.counts') as f:
    lines = f.readlines()


two_gram = {}
trf = open('5_1.txt', mode='w')
tri_gram = {}

for line in lines:
    part = line.strip().split(" ")
    if part[1] == "2-GRAM":
        st = part[2] + ' ' + part[3]
        two_gram[st] = int(part[0])
        # print st
    if part[1] == "3-GRAM":
        # print two_gram
        twost = part[2] + ' ' + part[3]
        # print twost
        if two_gram.has_key(twost):
            # print type(v)
            fre = float(part[0]) / two_gram[twost]
            fre = math.log(fre)
            tri_gram[part[2],part[3],part[4]] = fre
        else:
            tri_gram[part[2],part[3],part[4]] = -sys.maxint




with open('trigrams.txt') as tf:
    tlines = tf.readlines()


for tline in tlines:
    tpart = tline.strip().split()
    if tpart:
        if tri_gram.has_key((tpart[0], tpart[1], tpart[2])):
            trf.write(tpart[0] + ' ' + tpart[1] + ' ' + tpart[2] + ' ' + str(tri_gram[tpart[0], tpart[1], tpart[2]]) + '\n')
        else:
            trf.write(tpart[0] + ' ' + tpart[1] + ' ' + tpart[2] + ' ' + str(-sys.maxint) + '\n')
    else:
        trf.write('\n')