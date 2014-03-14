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
       print " ".join(seg.segment(  "如果不肯换位体验，能不能让他们失去位子？！否则他们永远不会懂得权力来自人民。 //@人 民日报:【想听真话摸实情，不如换位体验】网友建议：请民航部门领导以普通乘客身份  ，体验飞机晚点的烦恼…...感同身受，换位思考，还有哪些地方需要领导去体验？欢迎补充〜")  )  #如果 不肯 换位 体验 ， 能不能 让 他们 失去 位子 ？！ 否则 他们 永远 不会 懂得 权力 来自 人民 。 //@人民日报 :【 想 听 真话 摸 实情 ， 不如 换位 体验 】 网友 建议 ： 请 民航 部门 领导 以 普通 乘客 身份 ， 体验 飞机 晚点 的 烦恼 …... 感同身受 ， 换位 思考 ， 还有 哪些地方 需要 领导 去 体验 ？ 欢迎 补充 〜




中文拼音支持
---------------------
:::python
          
          p = pinyin()  
          print p.pinyin_segment('12上帝3aa') #12 shang di 3aa 
          print p.pinyin_segment('12上帝3aa' ,'#') #  'shang#di#3aa  
          会自动提取汉字进行转换  
          print p.zh2pinyin('我爱a') # wo ai a 不会自动转换不是汉字  
          print p.zh2pinyin('我爱a' , '#') # wo#ai#a


情感极性简单分析
---------------------
:::python


     from psentiment import SentimentTrie

     sentiment = SentimentTrie()
     print sentiment.get_word_sentiment('断章取义') # 返回值 -1.2 情感为负
     print sentiment.get_words_sentiment(['我' , '喜欢' , '你']) #[('\xe6\x88\x91', 1.7499999999999998), ('\xe5\x96\x9c\xe6\xac\xa2', 1.4310722100656499), ('\xe4\xbd\xa0', -0.7)] 返回每个词的极值
     print sentiment.get_sentence_sentiment(['我' , '喜欢' , '你']) # 返回2.48107221007 情感为积极
     print sentiment.get_sentence_sentiment(['我' , '恨' , '你']) #-0.4392 情感为消极

+ 计算情感词的极值 ， 现在简单的实现
+ 必须要加入否定词概念 
+ 情感极性 ， 推荐svm训练

