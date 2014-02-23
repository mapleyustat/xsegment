#coding=utf-8

import os

#文件操作类



class SegmetException(Exception):
    
    def __init__(self,msg,code = None):
        self.msg = msg
        self.code = code
    
    
    def __str__(self, *args, **kwargs):
        if self.code:
            return self.msg
        return "%s,%s" % (self.msg , self.code)

def _write(path,contents,mode):
    filehandle = open(path,mode)
    if not contents:
        raise SegmentException("DATA_IS_NONE",121)
    if isinstance(contents, list):
        for content in contents:
            filehandle.write(content)
    else:
        filehandle.write(contents)
    filehandle.close()
    
    
def append_write(path, contents):
    _write(path, contents, 'a')
    
def write_file(path,contents):
    _write(path, contents, 'w')
    
def clear_creat_write(path):
    _write(path,"")

def make_contents(contents):
    _contents = []
    if isinstance(contents, list):
        for content in contents:
            _contents.append("%s\n" % content.strip("\n"))
    return _contents

def make_dict_data(pattern,dictdata):
    if isinstance(dictdata, dict):
        restr = ''
        try:
            restr = pattern % dictdata
        except Exception,e:
            raise SegmentException("NO_RIGHT_PATTERN_%s" % e,109)
        return restr
    else:
        raise SegmentException("DATA_NO_DICT" ,110)
    

def _read(filepath):
    if not (os.path.isfile(filepath) and os.path.exists(filepath)):
        raise SegmentException("READ_FILE_WRONG_%s" % filepath , 111) 
    filehandle = open(filepath,"r")
    contents = filehandle.readlines()
    filehandle.close()
    return contents

def read_file_strip(filepath):
    _contents = _read(filepath)
    _newcontents = []
    for content in _contents:
        _newcontents.append(content.strip().encode('UTF-8'))
    return _newcontents

def read_file_line_format(filepath , formatfunction):
    _contents = _read(filepath)
    _newcontents = []
    for content in _contents:
        _newcontents.append(formatfunction(content))
    return _newcontents        



if __name__ == "__main__":
    pass