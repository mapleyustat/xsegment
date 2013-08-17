#coding=utf-8
#!/usr/bin/env python

from Trie import Trie
import filetutil
from segment import PreSegment


class Segment(object):
    
    
    def segment(self,words):
        pass


class SMM(Segment):
    
    _dict = Trie()
    
    def __init__(self , dictpath , maxlength=5):
        self.dictpath = dictpath
        self.maxlength = maxlength
        self._load_word_dict()
    
    def _load_word_dict(self ):
        contents = filetutil.read_file_strip(self.dictpath)
        for word in contents:
            wordarry = word.split()
            self._dict.add(wordarry[0], wordarry[1])
    
    
    def signal_word_in(self,words):
        count = 0
        for word in words:
            if len(word) == 1:
                count = count + 1
        return count
    
    def segment(self,words):
        _segmentwords = " "
        for word in PreSegment.token(words):
            print word
            _segmentwords = _segmentwords +" " +self._segment(word)
        return _segmentwords
    
    #解析中文分词 
    def _znsegment(self,words):
        pass
    
    #
    def _segment(self,words):
        if words:
            if words[1] == 'ZN':
                return self._znsegment(words[0])
            else:
                return  words[0]
        return  ""
        
             
        
        
class FMM(SMM):
    

        
    def _znsegment(self, words):
        _result = []
        if words and len(words):
            substring = words.decode("utf-8")
            while len(substring):
                subindex = self.maxlength
                if subindex >len(substring):
                    subindex = len(substring)
                token = substring[:subindex]
                rindex = len(token)
                while  rindex > 1:
                    if self._dict.search(token[:rindex]):
                        break
                    rindex = rindex - 1 
                _result.append(token[:rindex])
                substring = substring[len(token[:rindex]):]
        return " ".join(_result)


class RMM(SMM):
    
    def _znsegment(self, words):
        _result = []
        if words and len(words):
            substring = words.decode("utf-8")
            while len(substring):
                subindex = self.maxlength
                if subindex >len(substring):
                    subindex = len(substring)
                token = substring[-subindex:]
                lindex = 0
                while  lindex < (len(token) - 1):
                    if self._dict.search(token[lindex:]):
                        break
                    lindex = lindex + 1
                _result.append(token[lindex:])
                substring = substring[:-len(token[lindex:])]
            _result.reverse()
            
        return " ".join(_result)

class BMM(SMM):
    
    _fm = None
    _rm = None
    
    def __init__(self,dictpath=5, maxlength=5):
        SMM.__init__(self, dictpath, maxlength)
        self._fm = FMM(dictpath,maxlength)
        self._rm = RMM(dictpath,maxlength)
        
        
    def segment(self, words):
        fwords = self._fm.segment(words)
        rwords = self._rm.segment(words)
        minlen = len(fwords) - len(rwords)
        if minlen > 0:
            return rwords
        elif minlen < 0:
            return fwords
        else:
            diff_signal_word_num = self.signal_word_in(fwords) -  self.signal_word_in(rwords)
            if diff_signal_word_num > 0:
                return rwords
            elif diff_signal_word_num < 0:
                return fwords
            else:
                return rwords
    

        
            
        
        
        
        
if __name__ == "__main__":
    seg = BMM("dict.txt")
    
    print seg.segment("如果数据确定是gbk或gb2312的话, 你可以参考:http://blog.csdn.net/heiyeshuwu/archive/2007/01/20/1488900.aspx")
        