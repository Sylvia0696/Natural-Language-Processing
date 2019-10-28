#! /usr/bin/python

import math
import sys



#*****************   e    *************************
lines = []
with open('ner_rare.counts') as f:
    lines = f.readlines()
    
ydict = {'I-ORG' : 0, 'B-ORG' : 0, 'I-PER' : 0, 'B-PER' : 0, 'I-LOC' : 0, 'B-LOC' : 0, \
            'I-MISC' : 0, 'B-MISC' : 0, 'O' : 0}

# all y's sum
for line in lines:
    part = line.strip().split(" ")
    if part[1] != 'WORDTAG':
        break
    else:
        ydict[part[2]] = int(part[0]) + ydict[part[2]]


e = {}
xset = set()


for line in lines:
    part = line.strip().split(" ")
    if part[1] != 'WORDTAG':
        break
    else:
        xset.add(part[3])
        fre = float(part[0]) / ydict[part[2]]
        e[part[3], part[2]] = fre




#*******************   q   *********************
q = {}
two_gram = {}
for line in lines:
    part = line.strip().split(" ")
    if part[1] == '2-GRAM':
        two_gram[part[2], part[3]] = int(part[0])
    if part[1] == '3-GRAM':
        q[part[2], part[3], part[4]] = float(part[0]) / two_gram[part[2], part[3]]




#******************    def    **********************
def viterbi(txtf, sent):
    slist = ['I-ORG', 'B-ORG', 'I-PER', 'B-PER', 'I-LOC', 'B-LOC', 'I-MISC', 'B-MISC', 'O' ]
    s = slist
    n = len(sent)
    x_k = {i + 1 : sent[i] for i in range(0, len(sent))}
    pi = {}
    pi[0, '*', '*'] = 0
    bp = {}
    for k in range(1, n+1):
        s = slist
        if k - 1 == 0:
            s = ['*']
        for u in s:
            s = slist
            for v in s:
                if k - 2 <= 0:
                    s = ['*']
                pimax = -sys.maxint
                for w in s:
                    if not q.has_key((w, u, v)):
                        continue
                    modified_x = x_k[k]
                    if x_k[k] not in xset:
                        modified_x = '_RARE_'
                    if not e.has_key((modified_x, v)):
                        continue
                    if pimax < pi[k-1, w, u] + math.log(q[w, u, v]) + math.log(e[modified_x, v]):
                        pimax = pi[k-1, w, u] + math.log(q[w, u, v]) + math.log(e[modified_x, v])
                        bp[k, u, v] = w
                pi[k, u, v] = pimax


    s = slist
    pimax = -sys.maxint
    y_n = ''
    y_n_1 = ''
    if n - 1 == 0:
        s = ['*']
    for u in s:
        for v in slist:
            if not q.has_key((u, v, 'STOP')):
                continue
            if pimax < pi[n, u, v] + math.log(q[u, v, 'STOP']):
                pimax = pi[n, u, v] + math.log(q[u, v, 'STOP'])
                y_n_1, y_n = u, v


    ylist = []
    ylist.append(y_n)
    if n > 1:
        ylist.insert(0, y_n_1)
    for k in range(n-2, 0, -1):
        w_y = bp[k+2, ylist[0], ylist[1]]
        ylist.insert(0, w_y)


    value = []
    for k in range(n, 1, -1):
        value.insert(0, pi[k,ylist[k-2],ylist[k-1]])
    value.insert(0, pi[1, '*', ylist[0]])



    for k in range(1, n+1):
        txtf.write(x_k[k] + ' ' + ylist[k-1] + ' ' + str(value[k-1]) + '\n')







################# ba list bian cheng ju zi  ######################


txtf = open('5_2.txt', mode = 'w')

with open('ner_dev.dat') as nf:
    nlines = nf.readlines()

sent = []

for nline in nlines:
    nline = nline.strip().split()
    if nline:
        sent.append(nline[0])
    else:
        viterbi(txtf, sent)
        txtf.write('\n')
        sent = []