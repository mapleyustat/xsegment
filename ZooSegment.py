#coding=utf-8
#!/usr/bin/env python

from Trie import Trie
import filetutil

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
        #wait
        
        
        
class FMM(SMM):
    
    def __init__(self , **kargss):
        pass
        
    def segment(self, words):
        pass


class RMM(SMM):
    
    def segment(self, words):
        _result = []
        if words and len(words):
            substring = words.decode("utf-8")
            
            while len(substring):
                subindex = self.maxlength
                if subindex >len(substring):
                    subindex = len(substring)
                token = substring[-subindex:]
                rindex = len(token)
                lindex = 0
                while (rindex - lindex) > 0:
                    _token = token[lindex:rindex]
                    if self._dict.search(_token):
                        _result.append(_token)
                        break
                    lindex = lindex + 1
                if lindex == rindex:
                    _result.append(token)
                    substring = substring[:len(substring) - subindex]
                else:
                    substring = substring[:len(substring) - (lindex + 1)]
            _result.reverse()
        return _result
    
if __name__ == "__main__":
    seg = RMM("dict.dat")
    print " ".join(seg.segment("我爱中国共产党"))
    