#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pypinyin

convert = dict()
initial = dict()
final = dict()

with open('table/convert') as f:
    lines = [x.strip() for x in f.readlines()]
    for line in lines:
        buf = line.split(' ')
        convert[buf[0]] = buf[1]

with open('table/initial') as f:
    lines = [x.strip() for x in f.readlines()]
    for index in range(len(lines)):
        initial[lines[index]] = index

with open('table/final') as f:
    lines = [x.strip() for x in f.readlines()]
    for index in range(len(lines)):
        final[lines[index]] = index

def collect(string, buf):
    for init in pypinyin.pinyin(string, style=pypinyin.INITIALS, errors='ignore'):
        k = convert[init[0]] if init[0] in convert else init[0]
        if k in initial:
            buf[initial[k]] += 1

    for init in pypinyin.pinyin(string, style=pypinyin.FINALS, errors='ignore'):
        k = convert[init[0]] if init[0] in convert else init[0]
        if k in initial:
            buf[final[k] + len(initial)] += 1

def score(str1, str2):
    key = [0] * 39
    usr = [0] * 39

    collect(str1, key)
    collect(str2, usr)

    same = 0
    for i in range(len(key)):
        same += 1 if key[i] + usr[i] == 0 or key[i] * usr[i] > 0 else -1
    print 'loosy jaccard {}'.format(same * 1.0 / (len(key) * 2 - same))

if __name__ == '__main__':
    score(u'癌症', u'癌症')
    score(u'癌症', u'癌')
    score(u'癌症', u'症')
    score(u'癌', u'症')
    score(u'癌症', u'症癌症')
    score(u'耳朵', u'心脏病')
    score(u'心脏', u'心脏病')
    score(u'心', u'心脏病')
