zoo-segment 中文分词python分词
=================
思想
------------------------
*正向最大匹配  
*逆向最大匹配  
*词典树  
*正则预分词  


中文拼音支持
---------------------
:::python
          
          p = pinyin()  
          print p.pinyin_segment('12上帝3aa') #12 shang di 3aa 会自动提取汉字进行转换  
          print p.zh2pinyin('我爱a') # wo ai 6 不会自动转换不是汉字  


