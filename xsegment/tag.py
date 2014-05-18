# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import sys
import os
import json
import re
reload(sys)
sys.setdefaultencoding('utf-8')



class HSpeech(object):
    __start_state = None
    __emission_probability = None
    __transition_probability = None
    __states = None
    __min_value = 0.000000000001
    def __init__(self, model=os.path.join(os.path.abspath(os.path.dirname(__file__)),  'dict/')):
       self.__load(model)
    def __load(self, path):
        if path:
            if not path.endswith('/'):
                path = path + '/'
            with open('%s%s' % (path, 'tag_start_state.dat')) as f:
                self.__start_state = json.loads(f.readline())
            # print self.__start_state
            with open('%s%s' % (path, 'tag_emission_probability.dat')) as f:
                self.__emission_probability = json.loads(f.readline())
                # print self.__emission_probability
            with open('%s%s' % (path, 'tag_transition_probability.dat')) as f:
                self.__transition_probability = json.loads(f.readline())
            with open('%s%s' % (path , 'tag_obs_status.dat')) as f:
                j = json.loads(f.readline())
                self.__states = [ __key for __key in j.keys()]
                # print self.__transition_probability
        
    def __viterbi(self, obs):
        '''
        特比算法 摘自wiki 维特比算法
        '''
        # print obs
        V = [{}]
        path = {}
        for y in self.__states:
            if self.__emission_probability[y].has_key(obs[0]):
                V[0][y] = self.__start_state[y] * \
                self.__emission_probability[y][obs[0]]
            else:
                V[0][y] = self.__start_state[y] * self.__min_value
            path[y] = [y]
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in self.__states:
                prob = 0.
                state = self.__states[0]
                for y0 in self.__states:
                    if self.__emission_probability[y].has_key(obs[t]):
                        __prob = V[t - 1][y0] * self.__transition_probability[y0][y] * self.__emission_probability[y][obs[t]]
                    else:
                        __prob = V[t - 1][y0] * self.__transition_probability[y0][y] * self.__min_value
                    if __prob > prob:
                        prob = __prob
                        state = y0
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in self.__states])
        return (prob, path[state])

    def tag(self, segment_words,split_word = ' '):
        if segment_words:
            if isinstance(segment_words , str):
                segment_words = segment_words.decode('utf-8').split(split_word)
            elif isinstance(segment_words , unicode):
                segment_words = segment_words.split(split_word)
            elif not isinstance(segment_words , (list , tuple)):
                raise Exception,'type erro!'
            state = self.__viterbi(segment_words)[1]
            return [(segment_words[i] , state[i]) for i in range(len(segment_words))]
        return None


class trainHmm(object):
    __start_state = defaultdict(float)
    __obs_status = defaultdict(float)
    # 为了防止被 0 除 出现异常 ， 则每个状态初始化为1。
    # 开始状态矩阵构建
    # 隐藏状态转移
    tag_find = re.compile('/[a-z]+').finditer
    __transition_probability = {}
    # 隐藏状态下各个观察状态发生频率
    __emission_probability = {}

    word_state = set()

    def save_state(self):
        with open('tag_start_state.dat', 'w') as f:
            f.write(json.dumps(self.__start_state))
        with open('tag_emission_probability.dat', 'w') as f:
            f.write(json.dumps(self.__emission_probability))
        with open('tag_transition_probability.dat', 'w') as f:
            f.write(json.dumps(self.__transition_probability))
        with open('tag_obs_status.dat', 'w') as f:
            f.write(json.dumps(self.__obs_status))
        

    def add_line(self, line):
        if not (line and isinstance(line, (str, unicode)) and line != ''):
            raise Exception, line
        tag_arry =[label for label in [ __tag.split('/') for __tag in line.strip().split()] if len(label) > 1 and label[1] != '' and label[0] != "" ]
        if len(tag_arry) < 0:
            return
        try:
            self.__start_state[tag_arry[0][1]] += 1.
        except Exception,e:
            print e
        for i in range(1 , len(tag_arry)):
            if not self.__transition_probability.has_key(tag_arry[i][1]):
                self.__transition_probability[tag_arry[i][1]] = defaultdict(float)
            self.__transition_probability[tag_arry[i][1]][tag_arry[i-1][1]] += 1
        for __tag in tag_arry:
            self.word_state.add(__tag[0])
            self.__obs_status[__tag[1]] += 1
            if not self.__emission_probability.has_key(__tag[1]):
                self.__emission_probability[__tag[1]] = defaultdict(float)
            self.__emission_probability[__tag[1]][__tag[0]] += 1

    def train(self, file_name):
        with open(file_name) as f:
            for line in f.readlines():
                self.add_line(line)
        self.translte()

    def translte(self):
        '''
        有状态数量转换为概率
        '''
        # 初始化矩阵数目
        __start_state_count = 0
        for __key in self.__obs_status:
            self.__start_state[__key] += 0.

        for __value in self.__start_state.values():
            __start_state_count += __value
        # 计算开始状态概率
        for __key in self.__start_state.keys():
            self.__start_state[__key] = self.__start_state[
                __key] / __start_state_count
        # 初始化矩阵概率运算完毕

        # 转移矩阵
        for __state in self.__transition_probability.keys():
            for __afther_state in self.__obs_status.keys():
            # 计算公式 =》 p(Cj | Ci) = count(Ci,Cj) / count(Ci)
                self.__transition_probability[__state][__afther_state] = (self.__transition_probability[
                    __state][__afther_state] + 1.0)/ (self.__obs_status[__state] + 1.0)

         # 观察状态发生时候 隐藏状态发生概率
        for __hide in self.__emission_probability.keys():
            for word in self.__emission_probability[__hide].keys():
                try:
                    self.__emission_probability[__hide][word] = (
                    self.__emission_probability[__hide][word] + 1) / (self.__obs_status[__hide] + 1)
                except Exception,e:
                    print __hide



    
if __name__ == '__main__':
    h = HSpeech()
    # print h.viterbi( [u'我' , u'爱 ' , u'你' ])
    # print h.viterbi( [u'恭喜' , u'你' , u'发财'])
    print h.tag('我 早饭 我 的 祖国 !')
    
    # import os 
    # import re 

    # t = trainHmm()
    # t.add_line('越南/ns 电视台/n 报道/v 了/u 许多/a 市民/n 因为/c 赌球/v 而/c >输掉/v 了/u 所有/a 金钱/n 的/u 消息/n ，/w 设有/v 电视机/n 的/u 酒吧/n 在/p 直播/v 比赛/v 时/nt 挤/v 得/u 水泄不通/i 。/w')

    # word = re.compile('/[a-z]+\s?')
    # diff = set()
    # for file_name in os.listdir("data/"):
    #     file_path = '%s%s' % ('data/' , file_name)
    #     with open(file_path) as f:
    #          content = f.readlines()
    #          try:
    #              wd = content[2].split('：')[1].strip()
    #          except Exception,e:
    #              print file_path , e
    #          for line in content[6:]:
    #             line = line.strip().replace('[%s]' % wd , wd).split("\t")[2]
    #             if line in diff:
    #                 continue
    #             diff.add(line)
    #             t.add_line(line)
    # t.train('pku_training.utf8')
    # t.translte()
    # print t.segment([u'我', u'爱', u'我', u'的', u'祖', u'国', u'。'])
    # print ' '.join(t.segment(u'南京市长江大桥今天竣工！'))
    # print ' '.join(t.segment(u'李旭泽，想投奔搜狐新闻客户端可以联系我哈，我直送他们领导老李，哈哈。。'))
    # t.save_state()
