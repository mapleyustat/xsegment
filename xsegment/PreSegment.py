# coding=utf-8
#!/usr/bin/env python

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



REGX_ARRY = [(
    'URL', ur"((https?|ftp|news):\/\/)?([a-z]([a-z0-9\-]*[\.。])+([a-z]*)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&]*)?)?(#[a-z][a-z0-9_]*)?"),
    ('SIGN', r"[\.\=、，!！_?？\[\]【】：:。“”…\"〜]+"),
    ('AT', ur"(//)?@[\u4e00-\u9fa5a-z0-9]+"),
    ('IP' , ur'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'),
    ('FLOAT', ur"\d+\.\d+"),
    ('INTEGER', ur"[0-9]+"),
    ('ZN', ur"[\u4e00-\u9fa5]+"),
    ('EN', ur"[a-zA-Z]+"),
    ('MAIL',ur'[a-z]([a-z0-9]*[-_]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[.][a-z]{2,3}([.][a-z]{2})?'),
    ]


WORD_EXTRACT_REGX = ur'|'.join(ur'(?P<%s>%s)' % (pair[0],pair[1]) for pair in REGX_ARRY)
WORD_EXTRACT = re.compile(WORD_EXTRACT_REGX, re.U|re.IGNORECASE).finditer




def getWordSign(d):
    if isinstance(d, dict):
        for _key, _val in d.items():
            if _val != None:
                return (_val, _key)
    return None


def token(words):
    for token in WORD_EXTRACT(words):
        yield getWordSign(token.groupdict())


if __name__ == "__main__":
    statements = """五一假期拼凑了[。]“一个Google Analytics自动标记工具，我在博客里对这个工具进行简单的功能介绍并分享给有需要的朋友们使用。文章结尾附有工具下载地址。希望帮助大家减轻Google Analytics代码定制时的工作量。192.168.33

Read more: http://bluewhale.cc/tag/google-analytics#ixzz2cHtxfYjR""".decode("utf-8")
    for i in token(statements):
        print "%s\t\t%s" % (i[0], i[1])
    l = []
    l.append("。".decode("utf-8"))
    print l
