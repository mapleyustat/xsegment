# coding=utf-8
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

    __vector = {}  # 词 - > 文档 -> 词频
    __doc = set()  # ｄｏｃ　ｓｅｔ　只为了防止重复加入新的文档
    __tf_idf = None
    __idf = defaultdict(float)
    __newfish = False #

    def __init__(self):
        pass

    def add_doc(self, doc_name, doc, split_word=' '):
        if doc and doc_name and isinstance(doc_name, (str, unicode)) and len(doc_name) > 0:
            if doc_name in self.__doc:
                raise TypeError, 'doc_name :' + doc_name + ' has exist in this Vector'
            if isinstance(doc, (str, unicode)):
                doc = doc.split(split_word)
            elif not isinstance(doc, (list, tuple)):
                raise TypeError
            for word in doc:
                if not self.__vector.has_key(word):
                    self.__vector[word] = defaultdict(int)
                self.__vector[word][doc_name] += 1
            self.__doc.add(doc_name)
            self.__newfish = True
            return
        raise TypeError, 'doc is null or doc_name is null or doc_name isn\'t str '

    def __totfidf(self):
        doc_count = len(self.__doc)
        self.__tf_idf = {}
        for __word in self.__vector.keys():
            idf = math.log((1.0 + doc_count) / len(self.__vector[__word]), 2)
            self.__idf[word] = idf
            for __doc_name, __count in self.__vector[__word].items():
                if not self.__tf_idf.has_key(__doc_name):
                    self.__tf_idf[__doc_name] = defaultdict(float)
                self.__tf_idf[__doc_name][__word] = __count * idf
        self.__newfish = False
        return self.__tf_idf

    def similarty(self, doc_name1, doc_name2):
        if not (doc_name1 and doc_name2):
            raise TypeError
        if self.__newfish:
            self.__totfidf()

        if self.__tf_idf.has_key(doc_name1) and self.__tf_idf.has_key(doc_name2):
            __m1 = 0.
            for __val in self.__tf_idf[doc_name1].values():
                __m1 += __val * __val
            __m1 = math.sqrt(__m1)
            __m2 = 0.
            for __val in self.__tf_idf[doc_name2].values():
                __m2 += __val * __val
            __m2 = math.sqrt(__m2)
            word_set = set(self.__tf_idf[
                doc_name1].keys()) & set(self.__tf_idf[doc_name2].keys())
            __up = 0.
            for word in word_set:
                __up += (self.__tf_idf[doc_name1][
                         word] * self.__tf_idf[doc_name2][word])
            return __up / __m1 * __m2

    def query(self, doc):
        pass


if __name__ == '__main__':

    v = Vector()
    v.add_doc('a', 'a b c d c a')
    v.add_doc('b', 'a b c d c a')
    v.add_doc('c', 'c d f e r a c')
    print v.totfidf()
    print v.similarty('a', 'b')
