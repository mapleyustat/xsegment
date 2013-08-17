# -*- coding: UTF-8 -*-


import re
#import filetutil

WORD_EXTRACT_REGX =ur"(?P<URL>http://([a-z]{1,}\.){2}[a-z]{1,}(/[a-z0-9]{1,}){0,}\.[a-z0-9]{1,})|(?P<SIGN>[\.\+\*=、。，“”\"]+)|(?P<ZN>[\u2e80-\uffff]+)|(?P<EN>([a-z])+)|(?P<FLOAT>\d+\.\d+)|(?P<INTEGER>[0-9]+)"

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


 
statements ="你这个症状和我捡的流浪猫一模一样，刚醒的时候眼睛分泌物过多产生大量眼屎，发黄发臭，睁不开，是不是？这就是上火了，有炎症，轻者瞎眼，重者脑残，你这明显影响大脑了，穿衣服都不利索了，脖子咋从T恤嘎鸡窝那伸过去了呢？抓紧上医院治一治吧，拖下去生活不能自理也是分分钟的事，病好了再来打分。"

for i in token(statements):
    print "%s\t\t%s" % (i[0],i[1])


        
