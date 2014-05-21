#coding=utf-8
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from collections import defaultdict



import re


split = re.compile(ur'[^\u4E00-\u9FA5a-zA-Z0-9]+').split

def recognition(file_name , window = 3):
    word_count = defaultdict(int)
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) > 0 :
                line = line.decode('utf-8')
                for word in split(line):
                    for i in range(window,len(word)+ 1):
                        word_count[word[i - window : i]] += 1
    return sorted(word_count.items(), key = lambda x : x[1] , reverse = True)                        





if __name__ == '__main__':
    for i in recognition('/home/lixuze/12.txt' , window = 2)[:100]:
        print i[0] , i[1]
