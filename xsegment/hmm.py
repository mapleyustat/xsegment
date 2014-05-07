# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class trainHmm(object):
    state = defaultdict(float)
    # 为了防止被 0 除 出现异常 ， 则每个状态初始化为1。
    # 开始状态矩阵构建
    start_state = {'s': 1., 'b': 1., 'm': 1., 'e': 1.}
    # 隐藏状态转移
    transition_probability = {
        's': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}, 'b': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.},
'm': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}, 'e': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}}
    # 隐藏状态下各个观察状态发生频率
    emission_probability = {'s': defaultdict(float), 'e': defaultdict(
                            float), 'b': defaultdict(float), 'm': defaultdict(float)}

    word_state = set()

    def save_state(self):
        with open('start_state.dat', 'w') as f:
            f.write(json.dumps(self.start_state))
        with open('emission_probability.dat', 'w') as f:
            f.write(json.dumps(self.emission_probability))
        with open('transition_probability.dat', 'w') as f:
            f.write(json.dumps(self.transition_probability))

    def train(self, file_name):
        with open(file_name) as f:
            for line in f.readlines():
                text_arry = line.strip().split(' ')
                if len(text_arry[0].decode('utf-8')) > 1:
                    self.start_state['b'] += 1
                else:
                    self.start_state['s'] += 1
                word_label = []  # 保存单词标签 ， 单词 （位置标记 ， 词）
                for word in text_arry:
                    word = word.decode('utf-8')  # 因为汉字是utf-8
                    word = word.strip()
                    if len(word) == 1:
                        word_label.append(('s', word))
                    elif len(word) == 2:
                        word_label.append(('b', word[0]))
                        word_label.append(('e', word[1]))
                    elif len(word) > 2:
                        word_label.append(('b', word[0]))
                        for i in range(len(word[1:-1])):
                            word_label.append(('m', word[i + 1]))
                        word_label.append(('e', word[-1]))
                for i in range(len(word_label) - 1):
                    self.transition_probability[
                        word_label[i][0]][word_label[i + 1][0]] += 1
                for i in range(len(word_label)):
                	self.word_state.add(word_label[i][1])
                	self.state[word_label[i][0]] += 1
                	self.emission_probability[word_label[i][0]][word_label[i][1]] += 1
        self.__translte()

    def __translte(self):
        '''
        有状态数量转换为概率
        '''
        # 初始化矩阵数目
        start_state_count = 0
        for __value in self.start_state.values():
            start_state_count += __value
        # 计算开始状态概率
        for __key in self.start_state.keys():
            self.start_state[__key] = self.start_state[
                __key] / start_state_count
        # 初始化矩阵概率运算完毕

        # 转移矩阵
        for __state in self.transition_probability.keys():
            for __afther_state in self.transition_probability[__state].keys():
                # 计算公式 =》 p(Cj | Ci) = count(Ci,Cj) / count(Ci)
                self.transition_probability[__state][__afther_state] = self.transition_probability[
                    __state][__afther_state] / self.state[__state]

         # 观察状态发生时候 隐藏状态发生概率
        for __hide in self.emission_probability.keys():
        	for word in self.word_state:
        		self.emission_probability[__hide][word] = (self.emission_probability[__hide][word] + 1) / self.state[__hide] 




t = trainHmm()
t.train('pku_training.utf8')
t.save_state()
