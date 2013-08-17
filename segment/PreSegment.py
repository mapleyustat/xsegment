# -*- coding: UTF-8 -*-


import re
#import filetutil

WORD_EXTRACT_REGX =ur"(?P<URL>http://([a-z]{1,}\.){2}[a-z]{1,}(/[a-z0-9]{1,}){0,}\.[a-z0-9]{1,})"+ur"|(?P<SIGN>[\.\+\*\=、。，“”\"]+)"+ur"|(?P<ZN>[\u4e00-\u9fa5]+)"+ur"|(?P<EN>([a-z])+)"+ur"|(?P<FLOAT>\d+\.\d+)"+ur"|(?P<INTEGER>[0-9]+)"

#fileregx = [ regx.split("#")  for regx in filetutil.read_file_strip("wordregx.txt")]
#WORD_EXTRACT_REGX = ur'|'.join(ur'(?P<%s>%s)' % (pair[0],pair[1]) for pair in fileregx)
WORD_EXTRACT = re.compile(WORD_EXTRACT_REGX.encode("utf-8"),re.UNICODE).finditer
print WORD_EXTRACT_REGX


def getWordSign(d):
    if isinstance(d, dict):
        for _key,_val in d.items():
            if _val != None:
                return (_val,_key)
    return None


def token(words):
    for token in WORD_EXTRACT(words):
        yield getWordSign(token.groupdict())


 
statements ="今，。天他妈的热的1b"

for i in token(statements):
    print "%s\t\t%s" % (i[0],i[1])


        
