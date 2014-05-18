# coding=utf-8
#!/usr/bin/env python

import sys
from ZooSegment import FMM
from tag import HSpeech
reload(sys)
sys.setdefaultencoding('utf-8')

'''
自动摘要 编写
'''


def enum(args, start=0):
    class Enum(object):
        __slots__ = args.split()

        def __init__(self):
            for i, key in enumerate(Enum.__slots__, start):
                setattr(self, key, i)

    return Enum()

ITEM_LOCATION = enum('BEGIN MEDIM END NONE')


class WordItem(object):

    def __init__(self, word, tag, isKeyWord=False):
        self.word = word
        self.tag = tag
        self.isKeyWord = isKeyWord

    def __str__(self):
        msg = []
        for __key, __val in self.__dict__.items():
            msg.append('[%s %s]' % (__key, __val))
        return ' '.join(msg)


class Sentence(object):

    '''
    句子对象 ：
    oristring 原始句内容
    index 原始句的位置
    loc 段落中的位置
    items 分词信息
    keywords 关键词数目
    score 关键句打分
    '''

    def __init__(self, oristring, index, loc, words=None, items=None, keywords=None, score=0.):
        self.index = index
        self.items = items
        self.score = score
        self.keywords = keywords
        self.oristring = oristring
        self.loc = loc
        self.words = words

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __str__(self):
        msg = []
        for __key, __val in self.__dict__.items():
            msg.append('[%s %s]' % (__key, __val))
        return ' '.join(msg)


class Summary():

    __segment = None
    __tag = None

    def __init__(self):
        pass

    def summary(self, content, title):
        sentences = self.split_sentence(content)
        sentences.extend(self.split_sentence(title))
        self.segment(sentences)
        for sen in sentences:
            print sen.items

    def split_sentence(self, content):
        if content:
            if isinstance(content, str):
                content = content.decode('utf-8')
            sentences = []
            index = 0
            for pagraph in content.split('\n'):
                loc = ITEM_LOCATION.MEDIM
                split_last = 0
                save_sentences_len = len(sentences)
                for i in range(len(pagraph)):
                    if content[i] in ['!', '！', '?', '？', ';', '；']:
                        index = index + 1
                        sentences.append(
                            Sentence(pagraph[split_last: i + 1], index, loc))
                        split_last = i + 1
                    if content[i] == '。':
                        if i > 1:
                            if content[i - 1] in ['１', '２', '３', '４', '５', '６', '７', '８', '９', '０']:
                                if ((i + 1) < len(pagraph)) and content[i + 1] in ['１', '２', '３', '４', '５', '６', '７', '８', '９', '０']:
                                    continue
                        index = index + 1
                        sentences.append(
                            Sentence(pagraph[split_last: i + 1], index, loc))
                        split_last = i + 1
                if split_last != len(pagraph):
                    sentences.append(
                        Sentence(pagraph[split_last:], index, ITEM_LOCATION.END))
                if len(sentences) > save_sentences_len:
                    sentences[save_sentences_len].loc = ITEM_LOCATION.BEGIN
                if len(sentences) > (save_sentences_len + 1):
                    sentences[-1].loc = ITEM_LOCATION.END
            return sentences
        return []

    def segment(self, sentences):
        '''
        content : 每个要分词
        返回值：
        '''
        pass

    def extractKeyWord(self, sentences, topN=20):
        '''
        抽取关键词接口
        '''
        pass

    def score_sententce(self, sentenceitem):
        '''
        每个句子单独打分
        '''
        pass

    def sentences_filter(self, sentences, order=None):
        '''
        sentences : 每个文档的句子集合
        score : 阈值
        返回值: sententces
        '''
        if sentences:
            if isinstance(sententce, list) and len(sententces) > 0:
                return sorted(sentences, lambda x: x[order])
        raise TypeError, 'sentences must be list and item is sententce'



class SimpleSummary(Summary):

    __segment = FMM()
    __tag = HSpeech()


    def segment(self ,sentences):
        for i in range(len(sentences)):
            sentences[i].words = self.__segment.segment(sentences[i].oristring)
            items = []
            for __word in self.__tag.tag(sentences[i].words):
                items.append(WordItem(__word[0] , __word[1]))
            sentences[i].items = items





if __name__ == '__main__':
    s = SimpleSummary()
    for i in s.summary('我说你的问题 。3.16 我不知道啊啊！怎么了？ 说哈！这个问题;' , '测试'):
        print i
