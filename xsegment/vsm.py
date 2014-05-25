#coding=utf-8
#!/usr/bin/env python





from collections import defaultdict
import math
'''
vsm 空间向量模型
我们要计算td-idf 值　这样统计每个词的权重
之后将每片文章都转换为按照词序号　排序的词向量空间模型
而我们可以利用这个模型计算两个文档基于权重的相似度
我们过去计算两个文档相似只会计算这两个文档的词相似与否
而加入了ｔｆ-idf 后我们会考虑加入权重的文档相似度

'''

class Vector(object):


    __vector = {} #词 - > 文档 -> 词频
    __doc = set() #ｄｏｃ　ｓｅｔ　只为了防止重复加入新的文档
    __word = {} #词序号信息 甚至我都可以不加入这个信息
    __index = 0 #这个只是配合词序号信息的记录值


    def __init__(self):
        pass

    def add_doc(self , doc_name , doc , split_word = ' '):
        if doc and doc_name and isinstance(doc_name , (str , unicode)) and len(doc_name)  > 0:
            if doc_name in self.__doc:
                raise TypeError , 'doc_name :' + doc_name + ' has exist in this Vector' 
            if isinstance(doc , (str , unicode)):
                doc = doc.split(split_word)
            elif not isinstance(doc , (list , tuple )):
                raise TypeError
            for word in doc:
                if not self.__vector.has_key(word):
                    self.__vector[word] =  defaultdict(int)
                    self.__word[word] = self.__index 
                    self.__index = self.__index + 1
                self.__vector[word][doc_name] += 1
            return 
        raise TypeError , 'doc is null or doc_name is null or doc_name isn\'t str '

    def toidf(self):
        doc_count = len(self.__doc)
        idf = defaultdict(float)
        for __word in self.__vector.keys():
            idf[__word] = 
        return tf_idf




if __name__ == '__main__':
    

    v = Vector()
    v.add_doc('a' , 'a b c d c a')
    v.add_doc('b' , 'a c d e f a')

