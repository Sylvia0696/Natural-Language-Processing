#! /usr/bin/python

with open('ner.counts') as f:
    lines = f.readlines()
    
ydict = {'I-ORG' : 0, 'B-ORG' : 0, 'I-PER' : 0, 'B-PER' : 0, 'I-LOC' : 0, 'B-LOC' : 0, \
            'I-MISC' : 0, 'B-MISC' : 0, 'O' : 0}

cntdict = {}

for line in lines:
    part = line.strip().split(" ")
    if part[1] != 'WORDTAG':
        break
    else:
        ydict[part[2]] = int(part[0]) + ydict[part[2]]


xydict = {}


for line in lines:
    part = line.split()
    if part:
        if part[1] != 'WORDTAG':
            break
        else:
            xydict[part[3]] = float(part[0]) / ydict[part[2]]
            if cntdict.has_key(part[3]):
                cntdict[part[3]] = int(part[0]) + cntdict[part[3]]
            else:
                cntdict[part[3]] = int(part[0])




with open('ner_train.dat') as tr:
    trlines = tr.readlines()

raretr = open('ner_train_rare.dat', mode='w')


# trpart = trlines[0].split()
# print trpart
# print trpart[0]
# print cntdict[trpart[0]]
for trline in trlines:
    trpart = trline.split()
    if trpart:
        if cntdict[trpart[0]] < 5:
            st = '_RARE_ ' + trpart[1] + '\n'
            raretr.write(st)
        else:
            raretr.write(trline)
    else:
        raretr.write('\n')
