zoo-segment 中文分词python分词
=================
思想
------------------------
*正向最大匹配  
*逆向最大匹配  
*词典树  
*正则预分词  
:::python

       from ZooSegment import * 
       seg = FMM("dict/dict.txt")  
       print " ".join(seg.segment(  "如果不肯换位体验，能不能让他们失去位子？！否则他们永远不会懂得权力来自人民。 //@人 民日报:【想听真话摸实情，不如换位体验】网友建议：请民航部门领导以普通乘客身份  ，体验飞机晚点的烦恼…...感同身受，换位思考，还有哪些地方需要领导去体验？欢迎补充〜")  )  #



中文拼音支持
---------------------
:::python
          
          p = pinyin()  
          print p.pinyin_segment('12上帝3aa') #12 shang di 3aa 
          print p.pinyin_segment('12上帝3aa' ,'#') #  'shang#di#3aa  
          会自动提取汉字进行转换  
          print p.zh2pinyin('我爱a') # wo ai a 不会自动转换不是汉字  
          print p.zh2pinyin('我爱a' , '#') # wo#ai#a


