# coding=utf-8
#!/usr/bin/env python

import sys
from ZooSegment import FMM
from tag import HSpeech
from textrank import TextRank1
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
            if isinstance(__val, (list, tuple)):
                msg.append('%s %s' %
                           (__key, ' '.join([str(__v) for __v in __val])))
            else:
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

    def __init__(self, oristring, index, loc, words=None, items=None, keywords=None, wordLen=0, score=0.):
        self.index = index
        self.items = items
        self.score = score
        self.keywords = keywords
        self.oristring = oristring
        self.loc = loc
        self.words = words
        self.wordLen = wordLen

    def __str__(self):
        msg = []
        for __key, __val in self.__dict__.items():
            if isinstance(__val, (list, tuple)):
                msg.append('[ %s %s ]' %
                           (__key, ' '.join([str(__v) for __v in __val])))
            else:
                msg.append('[ %s %s ]' % (__key, __val))
        return '\n'.join(msg)


class Summary():

    def __init__(self):
        pass

    def summary(self, content, title, sentence_len=5):
        sentences = self.split_sentence(content)
        # return sentences
        sentences.extend(self.split_sentence(title))
        self.segment(sentences)
        self.extractKeyWord(sentences, topN=30)
        self.score_sententces(sentences)
        sentences = self.sentences_filter(sentences, 'score', reverse=True)
        if len(sentences) > sentence_len:
            sentences = sentences[: sentence_len]
        sentences = self.sentences_filter(sentences, 'index')
        return sentences

    def split_sentence(self, content):
        '''
        对输入的文本切分句子

        '''
        if content:
            if isinstance(content, str):
                content = content.decode('utf-8')
            sentences = []
            index = 0
            for pagraph in content.split('\r\n'):
                loc = ITEM_LOCATION.MEDIM
                split_last = 0
                save_sentences_len = len(sentences)
                pagraph = pagraph.strip()
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
                            Sentence(pagraph[split_last: i + 1].strip(), index, loc))
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

    def score_sententces(self, sentences):
        '''
        每个句子单独打分
        '''
        for i in range(len(sentences)):
            sentences[i].score = self.score(sentences[i])

    def score(self, sentence):
        '''
        单句打分
        '''
        pass

    def sentences_filter(self, sentences, order=None, reverse=False):
        '''
        sentences : 每个文档的句子集合
        score : 阈值
        返回值: sententces
        '''
        if sentences:
            if isinstance(sentences, list) and len(sentences) > 0:
                return sorted(sentences, key=lambda x: getattr(x, order), reverse=reverse)
        raise TypeError, 'sentences must be list and item is sententce'


class SimpleSummary(Summary):

    __segment = FMM()
    __tag = HSpeech()

    def __init__(self):
        pass

    def segment(self, sentences):
        for i in range(len(sentences)):
            sentences[i].words = self.__segment.segment(sentences[i].oristring)
            sentences[i].wordLen = len(sentences[i].words)
            sentences[i].items = [WordItem(__word[0], __word[1])
                                  for __word in self.__tag.tag(sentences[i].words)]
            #     items.append(WordItem(__word[0] , __word[1]))
            # sentences[i].items = items

    def extractKeyWord(self, sentences, topN=20):
        content = []
        for i in range(len(sentences)):
            content.extend(
                [item.word for item in sentences[i].items if item.tag in ['n', 'r', 'v'] and len(item.word) > 1])
        __window = TextRank1.create_word_window(content, 5, weight=True)
        __score_map = TextRank1.textrank(__window, 100)
        keywords = [i[0] for i in TextRank1.sort_score(__score_map, topN)]
        for i in range(len(sentences)):
            keyWordsLen = 0
            for j in range(len(sentences[i].items)):
                if sentences[i].items[j].word in keywords:
                    sentences[i].items[j].isKeyWord = True
                    keyWordsLen = keyWordsLen + 1
            sentences[i].keywords = keyWordsLen

    def score(self, sentence):
        __score = 0.
        if sentence.loc == ITEM_LOCATION.BEGIN:
            __score += 8
        if sentence.loc == ITEM_LOCATION.END:
            __score += 4
        __score = sentence.keywords * 60.0 / sentence.wordLen
        if sentence.oristring[-1] in [ '?' ,'!' , '?' ,'!']:
            __score -= 3
        return __score


if __name__ == '__main__':
    s = SimpleSummary()
    x = None
    with open('/home/lixuze/test.txt') as f:
        x = ''.join([line for line in f.readlines() if line.strip() != ''])
    for i in s.summary(x, '测试'):
        print i.oristring
