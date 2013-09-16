# -*- coding: UTF-8 -*-


import re
#import filetutil
REGX_ARRY= [('URL' , ur"http://([a-z]{1,}\.){1,}[a-z]{1,}(/[a-zA-Z0-9]{1,}){0,}(\.[a-z0-9])?"),
            ('SIGN',r"[\.\=、，!！_?？\[\]【】：:。“”…\"〜]+"),
            ('AT',ur"(//)?@[\u4e00-\u9fa5a-z0-9]+"),
            ('FLOAT',ur"\d+\.\d+"),
            ('INTEGER',ur"[0-9]+"),
            ('ZN',ur"[\u4e00-\u9fa5]+"),
            ('EN',ur"[a-zA-Z]+")]

#WORD_EXTRACT_REGX =ur"(?P<URL>http://([a-z]{1,}\.){2}[a-z]{1,}(/[a-z0-9]{1,}){0,}\.[a-z0-9]{1,})"+ur"|(?P<SIGN>[\.\+\*\=、。，“”\"]+)"+ur"|(?P<ZN>[\u4e00-\u9fa5]+)"+ur"|(?P<EN>([a-z])+)"+ur"|(?P<FLOAT>\d+\.\d+)"+ur"|(?P<INTEGER>[0-9]+)"

#fileregx = [ regx.split("#")  for regx in filetutil.read_file_strip("wordregx.txt")]
WORD_EXTRACT_REGX = ur'|'.join(ur'(?P<%s>%s)' % pair for pair in REGX_ARRY)
WORD_EXTRACT = re.compile(WORD_EXTRACT_REGX,re.U).finditer
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


if __name__ == "__main__":
    statements ="""五一假期拼凑了[。]“一个Google Analytics自动标记工具，我在博客里对这个工具进行简单的功能介绍并分享给有需要的朋友们使用。文章结尾附有工具下载地址。希望帮助大家减轻Google Analytics代码定制时的工作量。

Read more: http://bluewhale.cc/tag/google-analytics#ixzz2cHtxfYjR""".decode("utf-8")
    for i in token(statements):
        print "%s\t\t%s" % (i[0],i[1])
    l = []
    l.append("。".decode("utf-8"))
    print l


        
