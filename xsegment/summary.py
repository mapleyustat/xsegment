#coding=utf-8
#!/usr/bin/env python




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

class worditem(object):

    def __init__(self , word , tag , weight , isKeyWord):
        self.word = word 
        self.tag = tag 
        self.weight = weight 
        self.isKeyWord = isKeyWord

class sentence(object):
    '''
    句子对象 ：
    oristring 原始句内容
    index 原始句的位置
    loc 段落中的位置
    items 分词信息
    keywords 关键词数目
    score 关键句打分
    '''

    def __init__(self , oristring , index , loc = None , items = None, keywords = None , score = 0.):
        self.index = index 
        self.items = items
        self.score = score
        self.keywords = keywords
        self.oristring = oristring
        self.loc = loc


class Summary():


    def __init__(self):
        pass



    def summary(self , content , title):
        pass


    def segment(self , content):
        pass


    def extractKeyWord(self , content , topN):
        pass


    def score_sententce(self , sentenceitem):
        pass


    def sentences_filter(self , sentences ,socre):
        if sentences:
            if isinstance(sententce , list) and len(sententces) > 0:
                return sorted([ for sentence in sententces if sentence.score > score ] , lambda x : x.index )
        raise TypeError,'sentences must be list and item is sententce'


