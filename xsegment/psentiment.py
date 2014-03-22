#coding=utf-8
#!/usr/bin/env python



from Trie import Trie

def singleton(cls, *args, **kw):   
    instances = {}   
    def singleton_instance():   
        if cls not in instances:   
            instances[cls] = cls(*args, **kw)   
        return instances[cls]   
    return singleton_instance



@singleton
class SentimentTrie(object):


	__sentiment_trie = Trie()

	def __init__(self , dict_path = './dict/sentiment_word.txt' , split_word = '\t'):
		self.__load(dict_path , split_word)



	def __load(self , dict_path , split_word = '\t'):
		print 'load'
		with open(dict_path) as __file_handle:
			for line in __file_handle.readlines():
				line = line.strip()
				sentiment_word = line.split(split_word)
				if len(sentiment_word) >= 2:
					self.__sentiment_trie.add(sentiment_word[0].decode('utf-8') , float(sentiment_word[1]))


	def get_word_sentiment(self , word):
		if word:
			if not isinstance(word, (str , unicode)):
				word = word.decode('utf-8')
		__value =  self.__sentiment_trie.find(word.decode('utf-8'))
		if __value and isinstance(__value , float):
			return __value
		else:
			return 0.


	def get_words_sentiment(self , word_list = []):
		__sentiment_list = []
		if word_list and len(word_list) > 0:
			__sentiment_list.extend([(word , self.get_word_sentiment(word)) for word in word_list ])
		return __sentiment_list


	def get_sentence_sentiment(self , word_list = []):
		sentiment_point = 0.
		for __point in self.get_words_sentiment(word_list):
			sentiment_point += __point[1]
		return sentiment_point





if __name__ == '__main__':
	sentiment = SentimentTrie()
	print sentiment.get_word_sentiment('断章取义')
	print sentiment.get_word_sentiment('不')
	print sentiment.get_words_sentiment(['我' , '喜欢' , '你'])
	print sentiment.get_sentence_sentiment(['我' , '喜欢' , '你'])
	print sentiment.get_sentence_sentiment(['我' , '不' , '恨' , '你'])








