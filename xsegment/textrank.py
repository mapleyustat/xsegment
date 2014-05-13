# coding=utf-8
#!/usr/bin/env python


import re
from collections import defaultdict
import math

split = re.compile("\\s+", re.I).split
chinese = re.compile(ur"[\u4e00-\u9fa5]{2,}").match


class TextRank(object):

    split_regx = re.compile('\\s+').split

    def __init__(self):
        pass

    def extractWord(self, sententce):
    	'''
    	关键词抽取 ：
    	textrank 算法实现
    	'''
        if sententce and len(sententce) > 0:
            if isinstance(sententce, (str, unicode)):
                sententce = self.split_regx(sententce)
            elif not isinstance(sententce, (list, tuple)):
                raise Exception, 'type erro'
        sententce = [ word for word in sententce  if chinese(word.decode('utf-8'))]
        word_map = self.__create_word_map(sententce)
        word_len = len(set(word_map))  # 词数
        word_arry = TextRank.createList(word_len, word_len)
        for i in range(1, len(sententce)):
                # 建立窗口 ， 一个词投给另个词
            word_arry[word_map[sententce[i]]][word_map[sententce[i - 1]]] += 1

        # 生成初始化矩阵
        # for j in range(word_len):
        #     noZero = 0
        #     for i in range(word_len):
        #         if word_arry[i][j] != 0:
        #             noZero += 1
        #     if noZero != 0:
        #         for i in range(word_len):
        #             word_arry[i][j] /= float(noZero)
        score = self.dopagerank(word_arry)
        text_rank = [(__key, score[__val])
                     for __key, __val in word_map.items()]
        return sorted(text_rank, key=lambda x: x[1], reverse=True)

    def dopagerank(self, word_arry, iter=30, d = 0.85, diff=0.0001):
        max_diff = 0.
        score = [0.1 for _ in range(len(word_arry))]
        score_back = [0.1 for _ in range(len(word_arry))]
        for count in range(iter):
            for c in range(len(score)):
                score_back[c] = score[c]
            for i in range(len(word_arry)):
                __point = 0.
                for j in range(len(word_arry[i])):
                    __out = 0.  # 出链数
                    if word_arry[i][j] != 0.:
                        for o in range(len(word_arry)):
                            __out += word_arry[o][j]
                        if __out != 0.:
                        	__point += score[i] / __out
                score[i] = 1 - d + d * __point
                if abs(score[i] - score_back[j]) > max_diff:
                    max_diff = abs(score[i] - score_back[j])
        if max_diff < diff:
            return score
        return score

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

    """"""

    def __init__(self):
        pass

    @staticmethod
    def create_word_window(sentence, window_size ,weight = False):
        '''
        方法： 创建一个词窗口 格式 ： 词 -》 窗口词
              返回值：
        '''
        if sentence and len(sentence) > 0:
            if isinstance(sentence, (str, unicode)):
                sentence = split(sentence)
            elif not isinstance(sentence, (list, tuple)):
                raise Exception, '%s is type erro!' % sentence
            if not weight:
            	word_window = defaultdict(set)
            else:
            	word_window = defaultdict(list)
            # 这里没有处理 ， 窗口与字符串长度判断
            sentence_new = [ word for word in sentence if chinese(word.decode('utf-8'))]
            for i in range(window_size, len(sentence_new)):
                for j in range(i - window_size, i):
                	if not weight:
                		word_window[sentence_new[i]].add(sentence_new[j])
                	else:
                		word_window[sentence_new[i]].append(sentence_new[j])
            return word_window
        return None

    @staticmethod
    def textrank(word_window, iter_count=20, diff=0.000001, d=0.85):
        '''
        textrank 参照论文 ： TextRank: Bringing Order into Texts
        原理 ： 根据词窗口 建立边 词 ： 顶点
        迭代公式 ： score(Vi) = 1- d * sum(In(Vi)) * 1/ out(Vj) * score(Vj)
        Vi ，Vj 就是任意点
        参数 ： word_window  是 词- 》 该词前面n个窗口的词（）
               iter_count 迭代次数
               diff 两次迭代最小变化值
               d 阻尼系数

        '''
        if isinstance(word_window, dict):
            scoreDict = defaultdict(float)
            tmp = defaultdict(dict)            
            for __key in word_window.keys():
                scoreDict[__key] = 1.
            for c in range(iter_count):
                max_diff = 0.
                for __key in scoreDict.keys():
                	tmp[__key] = scoreDict [__key]
                for __key, __val in word_window.items():
                    score = 0.
                    for __word in __val:  # 循环每个窗口词
                        __out = 0  # 初练数目
                        if word_window.has_key(__word):
                            __out = len(word_window[__word])
                        if __word == __key or __out == 0:
                            continue
                        score += tmp[__word] / __out
                    tmp[__key] = 1 - d + d * score
                    __diff = abs(tmp[__key] - scoreDict[__key])
                    if max_diff < __diff:
                        max_diff = __diff
                for __key in scoreDict.keys():
                	scoreDict[__key] = tmp [__key]
                if max_diff <= diff:
                    break
            return scoreDict

    @staticmethod
    def sort_score(scoreDict, size=None):
        if size and size > 0:
            if size > len(scoreDict):
                size = scoreDict
        l = [(__key, __val) for __key, __val in scoreDict.items()]
        l = sorted(l, key=lambda x: x[1], reverse=True)
        if size:
            return l[:size]
        else:
            return l

if __name__ == '__main__':
    x = TextRank()
    x.extractWord('我 说 你 应该  知道 我 , 你 说 你 知道 什么')
    from xsegment.ZooSegment import FMM
    h = FMM()
    p = x.extractWord(
        h.segment("""   新华网内罗毕5月11日电（记者张艺 俞铮）国务院总理李克强11日上午在内罗毕国家宫与肯尼亚总统肯雅塔、乌干达总统穆塞韦尼、卢旺达总统卡加梅、南苏丹总统基尔等东非地区国家领导人，以及坦桑尼亚、布隆迪、非洲开发银行代表共同出席肯尼亚蒙巴萨至内罗毕铁路项目中肯共同融资协议签字仪式并讲话。该项目将由中国公司承建。李克强说，很高兴在内罗毕同各国领导人相聚一堂共商大计。你们专程前来出席此次签字仪式，表明各国支持建设东非铁路网的共同意愿。国家要发展，交通基础设施要先行。中方愿同各方分享铁路建设方面的技术和经验，积极开展设计、建设、装备、管理、人才培训、项目融资等合作。李克强表示，东非地区乃至非洲实现互联互通，将对非洲国家经济发展起到重要支撑作用。蒙内铁路是中非从次区域合作起步，共同建设非洲高速铁路、高速公路和区域航空三大网络的重大项目，中方将与相关国家及非盟加强沟通协作，充分发挥中非金融机构的融资功能，也欢迎域外第三方机构积极参与，实现互利共赢。东非国家领导人表示，蒙内铁路是肯尼亚近百年来新建的第一条铁路，将进一步完善东非铁路网，增加东非国家的运力，推进东非地区的互联互通和一体化建设，促进各国经济发展。各国感谢中国的帮助和支持，将与中方齐心协力尽早建好这一铁路，造福本地区人民。""") )
    for i in p:
        print i[0], i[1]
    k = TextRank1.create_word_window(
        ' '.join(h.segment("""   新华网内罗毕5月11日电（记者张艺 俞铮）国务院总理李克强11日上午在内罗毕国家宫与肯尼亚总统肯雅塔、乌干达总统穆塞韦尼、卢旺达总统卡加梅、南苏丹总统基尔等东非地区国家领导人，以及坦桑尼亚、布隆迪、非洲开发银行代表共同出席肯尼亚蒙巴萨至内罗毕铁路项目中肯共同融资协议签字仪式并讲话。该项目将由中国公司承建。李克强说，很高兴在内罗毕同各国领导人相聚一堂共商大计。你们专程前来出席此次签字仪式，表明各国支持建设东非铁路网的共同意愿。国家要发展，交通基础设施要先行。中方愿同各方分享铁路建设方面的技术和经验，积极开展设计、建设、装备、管理、人才培训、项目融资等合作。李克强表示，东非地区乃至非洲实现互联互通，将对非洲国家经济发展起到重要支撑作用。蒙内铁路是中非从次区域合作起步，共同建设非洲高速铁路、高速公路和区域航空三大网络的重大项目，中方将与相关国家及非盟加强沟通协作，充分发挥中非金融机构的融资功能，也欢迎域外第三方机构积极参与，实现互利共赢。东非国家领导人表示，蒙内铁路是肯尼亚近百年来新建的第一条铁路，将进一步完善东非铁路网，增加东非国家的运力，推进东非地区的互联互通和一体化建设，促进各国经济发展。各国感谢中国的帮助和支持，将与中方齐心协力尽早建好这一铁路，造福本地区人民。""") ), 7)
    c = TextRank1.create_word_window(h.segment('''海外网5月12日电 据杭州警方12日对余杭中泰事件发布两份通报，通报称，余杭中泰事件中53名犯罪嫌疑人被依法刑拘，11名违法犯罪嫌疑人主动向警方投案。杭州警方对7名网上散布谣言违法人员作出行政拘留处罚。通报《余杭中泰事件中53名犯罪嫌疑人被依法刑拘 11名违法犯罪嫌疑人主动向警方投案 5月10日，在少数不法分子的煽动和蛊惑下，余杭中泰及附近地区人员规模性聚集，封堵02省道和杭徽高速公路，一度造成交通中断，一些不法分子甚至趁机打砸、损坏车辆，围攻殴打执法民警和无辜群众。经公安机关调查，迅速将一批涉嫌聚众扰乱公共秩序、妨碍公务和寻衅滋事的犯罪嫌疑人抓获归案。公安机关已对53名涉嫌犯罪的嫌疑人刑事拘留。犯罪嫌疑人裘某某，现年43岁，临安市人。经审讯，裘某某如实供述了自己的犯罪事实。5月10日，其在当天现场聚集人群中，面对着执勤民警高喊：“大家冲上去，打死他们”，并用石块砸向现场民警。之后，他还爬上杭徽高速公路阻断交通。犯罪嫌疑人何某某，24岁，四川人，被警方抓获后承认伙同张某，用石块打砸警车。现裘某某、何某某已被警方刑事拘留。
5月11日，余杭区人民法院、余杭区人民检察院、杭州市公安局余杭分局、杭州市余杭区司法局《关于敦促违法犯罪人员自首的通告》发布后，一批违法犯罪嫌疑人慑于法律的威严，在亲友的规劝下，主动向公安机关投案。截至发稿时，已有11名涉案人员向警方投案。25岁的李某， 5月10日涉嫌在“5.10事件”现场袭警，案发后在逃。警方将其上网追逃，5月11日下午2时许，李某迫于压力，主动到公安机关投案自首，承认了自己殴打民警的犯罪事实，并对自己的行为感到非常后悔，愿意承担法律责任。公安机关鉴于其主动投案自首，如实交代自己的犯罪行为，知罪悔罪，决定予以取保候审。
公安机关重申，凡在此次事件中实施堵塞交通、毁坏公私财物、伤害他人、制造传播谣言等违法犯罪行为的人员，必须主动到公安司法机关投案自首，如实交代自己的违法犯罪行为，争取从宽处理。对拒不投案自首，潜逃或者继续实施违法犯罪行为的，公安司法机关将坚决采取有力措施缉捕归案，依法严惩。通报《杭州警方对7名网上散布谣言违法人员作出行政拘留处罚》如下：
5月12日，7名在互联网上捏造谣言，散布虚假信息的杭州籍网民张某、许某、陈某、洪某、龚某和浙江台州籍网民冯某、江西籍网民李某、被杭州市公安机关作出行政拘留处罚。5月10日，在余杭中泰地区聚集堵路打砸事件中，张某（女、35岁）在其网名为“静水流深”的微博上，发布“特警用防空盾、催泪瓦斯，如今已经有4个老百姓无辜死亡”的虚假内容。当晚，李某（女、23岁）登陆网名为小灰灰的腾讯微博发帖称“警察就像火车站乱砍人的歹徒一模一样，见人就打，被扔下桥，把人电死，现场哭成一片，实在太恐怖了”。此外，许某（女，28岁）、洪某（男，32岁）、陈某（男，37岁）、冯某（男，25岁）、龚某（女，32岁）相继于5月10日、11日编造“送到医院的伤者已经三个确认死亡，医院封锁消息”、“一个3岁小孩在妈妈怀抱中被特警抢走从立交桥摔死”等谣言在互联网上扩散，引发公众关注，扰乱公共秩序，以上7人均对上述造谣惑众的违法事实供认不讳。公安机关根据《中华人民共和国治安管理处罚法》相关规定，对上述7名人员分别作出行政拘留5-10日的处罚。'''), 3 , weight = True)
    scoremap = TextRank1.textrank(c, iter_count=100)
    for i in TextRank1.sort_score(scoremap , 8):
        print i[0], i[1]
