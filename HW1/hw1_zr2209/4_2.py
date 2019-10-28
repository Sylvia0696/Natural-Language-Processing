#! /usr/bin/python

import math

with open('ner_rare.counts') as f:
    lines = f.readlines()
    
ydict = {'I-ORG' : 0, 'B-ORG' : 0, 'I-PER' : 0, 'B-PER' : 0, 'I-LOC' : 0, 'B-LOC' : 0, \
            'I-MISC' : 0, 'B-MISC' : 0, 'O' : 0}



for line in lines:
    part = line.strip().split(" ")
    if part[1] != 'WORDTAG':
        break
    else:
        ydict[part[2]] = int(part[0]) + ydict[part[2]]


pairdict = {}


for line in lines:
    part = line.strip().split(" ")
    if part[1] != 'WORDTAG':
        break
    else:
        fre = float(part[0]) / ydict[part[2]]
        if pairdict.has_key(part[3]):
            pairdict[part[3]][fre] = part[2]
        else:
            pairdict[part[3]] = {fre : part[2]}
print pairdict['_RARE_']

# print pairdict['Nations']
# print pairdict['Nations']
# print pairdict['CRICKET']



with open('ner_dev.dat') as ner:
    nerlines = ner.readlines()


maxcn = 0
for k, v in pairdict['_RARE_'].iteritems():
    if k > maxcn:
        maxcn = k
mle = math.log(maxcn)
y = pairdict['_RARE_'][maxcn]
rarest = ' ' + y + ' ' + str(mle) + ' ' + '\n'



raref = open('4_2.txt', mode='w')




for nerline in nerlines:
    nerline = nerline.strip().split()
    if nerline:
        if pairdict.has_key(nerline[0]):
            maxcn = 0
            for k, v in pairdict[nerline[0]].iteritems():
                if k > maxcn:
                    maxcn = k
            mle = math.log(maxcn)
            y = pairdict[nerline[0]][maxcn]
            st = nerline[0] + ' ' +  y + ' ' + str(mle) + '\n'
        else:
            st = nerline[0] + rarest
        # if nerline[0] == "Nations":
        #     print st
        raref.write(st)
    else:
        raref.write("" + '\n')
