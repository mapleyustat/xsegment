# coding=utf-8
#!/usr/bin/env python

from Trie import Trie
import re
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


class pinyin():

    __zh = re.compile(ur"([\u4E00-\u9FA5]+)")
    __dict = Trie()

    def __init__(self, dict_path=os.path.join(os.path.abspath(os.path.dirname(__file__)) , 'dict/word.data')):
        self.__load(dict_path)

    def __load(self, dict_path):
        with open(dict_path) as f:
            for line in f.readlines():
                pin_yin = line.strip().split('\t')
                if len(pin_yin) == 2:
                    self.__dict.add(pin_yin[0], pin_yin[1])

    def zh2pinyin(self, words ,split_word = ' '):
        if words:
            if not isinstance(words, unicode):
                words = words.decode('utf-8')
            return split_word.join([self.__dict.find('%X' % ord(word),'%sx' % word).split()[0][:-1].lower() for word in words])
        else:
            return ''

    def pinyin_segment(self, words , split_word = ' '):
        if words:
            if not isinstance(words, unicode):
                words = words.decode('utf-8')
            result = []
            for word in self.__zh.split(words):
                if self.__zh.match(word):
                    result.append(self.zh2pinyin(word.strip() , split_word))
                elif word:
                    result.append('%s' % word.strip())
            return split_word.join(result)
        return ''


if __name__ == '__main__':
    p = pinyin()
    print p.pinyin_segment(u'上帝 3aa','#')
    print p.zh2pinyin('上帝aa')
