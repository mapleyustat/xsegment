# coding=utf-8
#!/usr/bin/env python


import re
from collections import defaultdict


class TextRank(object):

    split_regx = re.compile('\\s+').split

    def __init__(self):
        pass

    def extractWord(self, sententce):
        if sententce and len(sententce) > 0:
            if isinstance(sententce, (str, unicode)):
                sententce = self.split_regx(sententce)
            elif not isinstance(sententce, (list, tuple)):
                raise Exception, 'type erro'
        word_map = self.__create_word_map(sententce)
        word_len = len(set(word_map))  # 词数
        word_arry = TextRank.createList(word_len , word_len)
        for i in range(1, len(sententce)):
        	word_arry[word_map[sententce[i]]][word_map[sententce[i-1]]] += 1
        print word_arry
            

    def __create_word_map(self, sententce):
        word_map = {}
        index = 0
        for word in sententce:
            if word_map.has_key(word):
                continue
            word_map[word] = index
            index = index + 1
        return word_map

    @staticmethod
    def createList(row, line, value=0):
        if not (row > 0 and line > 0):
            raise Exception, 'row > 0 , line > 0'
        l = list()
        for i in range(row):
        	l.append([])
        	for j in range(line):
        		l[i].append(value)
        return l


if __name__ == '__main__':
    x = TextRank()
    print TextRank.createList(3, 4)[2][1]
    x.extractWord('我 说 你 应该  知道 我')
