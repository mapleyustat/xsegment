#coding=utf-8



class SegmetException(Exception):
    
    def __init__(self,msg,code = None):
        self.msg = msg
        self.code = code
    
    
    def __str__(self, *args, **kwargs):
        if self.code:
            return self.msg
        return "%s,%s" % (self.msg , self.code)