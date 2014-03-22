# coding:utf-8
#!/usr/bin/env python


from collections import defaultdict
import math


class TFIDF(object):

    '''
    __word_tf_idf = { word : {'idf' : 0. , 'docs' : 100 }}



    '''
    __word_tf_idf = defaultdict(dict)
    __doc_count = 1

    def add_docunment(self, doc=[]):
        __word_freq, _ = self.get_word_freq(doc)
        for word in __word_freq.keys():
            word_num = 1
            if self.__word_tf_idf[word].has_key('docs'):
                word_num += self.__word_tf_idf[word]['docs']
            self.__word_tf_idf[word]['docs'] = word_num
        self.__doc_count += 1

    def tf_idf(self, doc, word=None):
    	self.add_docunment(doc)
        word_freq, word_count = self.get_word_freq(doc)
        ti = [(word , (float(freq) / float(word_count)) * math.log(float(self.__doc_count) / float(self.__word_tf_idf[word]['docs'] + 1)))
              for word, freq in word_freq.items()]
        return sorted(ti , key = lambda x:x[1] ,reverse = True)

    @staticmethod
    def get_word_freq(doc=[], split_word=''):
        word_bag = defaultdict(int)
        count = 0
        for word in doc:
            word_bag[word] += 1
            count += 1
        return word_bag, count


if __name__ == '__main__':
    t = TFIDF()
    t.add_docunment(['a', 'b', 'a'])
    t.add_docunment(['y', 'c', 'a'])
    t.add_docunment(['c', 'b', 'a'])
    t.add_docunment(['c', 'b', 'a'])
    print t.tf_idf(['a', 'b', 'z'])
