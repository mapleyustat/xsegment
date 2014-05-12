# coding=utf-8
#!/usr/bin/env python


import re
from collections import defaultdict


split = re.compile("\\s+" , re.I).split

class TextRank(object):

    split_regx = re.compile('\\s+').split

    def __init__(self):
        pass

    def extractWord(self, sententce):
        if sententce and len(sententce) > 0:
            if isinstance(sententce, (str, unicode)):
                sententce = self.split_regx(sententce)
            elif not isinstance(sententce, (list, tuple)):
                raise Exception, 'type erro'
        word_map = self.__create_word_map(sententce)
        word_len = len(set(word_map))  # 词数
        word_arry = TextRank.createList(word_len , word_len)
        for i in range(1, len(sententce)):
        	word_arry[word_map[sententce[i]]][word_map[sententce[i-1]]] += 1


        #生成初始化矩阵
        for j in range(word_len):
        	noZero = 0
        	for i in range(word_len):
        		if word_arry[i][j] != 0:
        			noZero += 1
        	if noZero !=0:
        		for i in range(word_len):
        			word_arry[i][j] /= float(noZero)
        print word_arry

    def __create_word_map(self, sententce):
        word_map = {}
        index = 0
        for word in sententce:
            if word_map.has_key(word):
                continue
            word_map[word] = index
            index = index + 1
        return word_map

    @staticmethod
    def createList(row, line, value=0):
        if not (row > 0 and line > 0):
            raise Exception, 'row > 0 , line > 0'
        l = list()
        for i in range(row):
        	l.append([])
        	for j in range(line):
        		l[i].append(value)
        return l

class TextRank1(object):
	"""docstring for TextRank1"""
	def __init__(self):
		pass
	@staticmethod
	def create_word_window(sentence , window_size):
		if sententce and len(sententce) > 0 :
			if isinstance(sententce , (str , unicode)):
				sententce = split(sententce)
			elif not isinstance(sententce , (list , tuple)):
				raise Exception,'%s is type erro!' % sententce
			word_window = defaultdict(set)
			#这里没有处理 ， 窗口与字符串长度判断
			for i in range(window_size , len(sententce)):
				for j in range(i -window_size , i):
				    word_window[sententce[i]].add(sententce[j])
			return word_window
		return None
		

if __name__ == '__main__':
    x = TextRank()
    print TextRank.createList(3, 4)[2][1]
    x.extractWord('我 说 你 应该  知道 我 , 你 说 你 知道 什么')
    from xsegment.hmm import HSegment
    h = HSegment()
    print TextRank1.create_word_window(h.segment("""   新华网内罗毕5月11日电（记者张艺 俞铮）国务院总理李克强11日上午在内罗毕国家宫与肯尼亚总统肯雅塔、乌干达总统穆塞韦尼、卢旺达总统卡加梅、南苏丹总统基尔等东非地区国家领导人，以及坦桑尼亚、布隆迪、非洲开发银行代表共同出席肯尼亚蒙巴萨至内罗毕铁路项目中肯共同融资协议签字仪式并讲话。该项目将由中国公司承建。
　　李克强说，很高兴在内罗毕同各国领导人相聚一堂共商大计。你们专程前来出席此次签字仪式，表明各国支持建设东非铁路网的共同意愿。国家要发展，交通基础设施要先行。中方愿同各方分享铁路建设方面的技术和经验，积极开展设计、建设、装备、管理、人才培训、项目融资等合作。
　　李克强表示，东非地区乃至非洲实现互联互通，将对非洲国家经济发展起到重要支撑作用。蒙内铁路是中非从次区域合作起步，共同建设非洲高速铁路、高速公路和区域航空三大网络的重大项目，中方将与相关国家及非盟加强沟通协作，充分发挥中非金融机构的融资功能，也欢迎域外第三方机构积极参与，实现互利共赢。
　　东非国家领导人表示，蒙内铁路是肯尼亚近百年来新建的第一条铁路，将进一步完善东非铁路网，增加东非国家的运力，推进东非地区的互联互通和一体化建设，促进各国经济发展。各国感谢中国的帮助和支持，将与中方齐心协力尽早建好这一铁路，造福本地区人民。""") , 3)