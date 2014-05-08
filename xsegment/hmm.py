# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class trainHmm(object):
    state = defaultdict(float)
    __states = ['s', 'm', 'b', 'e']
    # 为了防止被 0 除 出现异常 ， 则每个状态初始化为1。
    # 开始状态矩阵构建
    __start_state = {'s': 1., 'b': 1., 'm': 1., 'e': 1.}
    # 隐藏状态转移
    __transition_probability = {
        's': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}, 'b': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.},
'm': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}, 'e': {'s': 1.,  'b': 1., 'm': 1., 'e': 1.}}
    # 隐藏状态下各个观察状态发生频率
    __emission_probability = {'s': defaultdict(float), 'e': defaultdict(
        float), 'b': defaultdict(float), 'm': defaultdict(float)}

    word_state = set()

    def save_state(self):
        with open('__start_state.dat', 'w') as f:
            f.write(json.dumps(self.__start_state))
        with open('__emission_probability.dat', 'w') as f:
            f.write(json.dumps(self.__emission_probability))
        with open('__transition_probability.dat', 'w') as f:
            f.write(json.dumps(self.__transition_probability))

    def add_line(self, line):
        if not (line and isinstance(line, (str, unicode)) and line != ''):
            raise Exception, line
        text_arry = line.strip().split(' ')
        if len(text_arry[0].decode('utf-8')) > 1:
            self.__start_state['b'] += 1
        else:
            self.__start_state['s'] += 1
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
         # 2元文法
        for i in range(len(word_label) - 1):
            self.__transition_probability[
                word_label[i][0]][word_label[i + 1][0]] += 1
        # 循环整个标记
        for i in range(len(word_label)):
            self.word_state.add(word_label[i][1])
            self.state[word_label[i][0]] += 1
            self.__emission_probability[
                word_label[i][0]][word_label[i][1]] += 1

    def train(self, file_name):
        with open(file_name) as f:
            for line in f.readlines():
                self.add_line(line)
        self.__translte()

    def __translte(self):
        '''
        有状态数量转换为概率
        '''
        # 初始化矩阵数目
        __start_state_count = 0
        for __value in self.__start_state.values():
            __start_state_count += __value
        # 计算开始状态概率
        for __key in self.__start_state.keys():
            self.__start_state[__key] = self.__start_state[
                __key] / __start_state_count
        # 初始化矩阵概率运算完毕

        # 转移矩阵
        for __state in self.__transition_probability.keys():
            for __afther_state in self.__transition_probability[__state].keys():
            # 计算公式 =》 p(Cj | Ci) = count(Ci,Cj) / count(Ci)
                self.__transition_probability[__state][__afther_state] = self.__transition_probability[
                    __state][__afther_state] / self.state[__state]

         # 观察状态发生时候 隐藏状态发生概率
        for __hide in self.__emission_probability.keys():
            for word in self.word_state:
                self.__emission_probability[__hide][word] = (
                    self.__emission_probability[__hide][word] + 1) / self.state[__hide]

    def __viterbi(self, obs):
        V = [{}]
        path = {}
        for y in self.__states:
            V[0][y] = self.__start_state[y] * \
                self.__emission_probability[y][obs[0]]
            path[y] = [y]
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in self.__states:
                (prob, state) = max(
                    [(V[t - 1][y0] * self.__transition_probability[y0][y] * self.__emission_probability[y][obs[t]], y0) for y0 in self.__states])
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in self.__states])
        return (prob, path[state])

    def segment(self, sentence):
        sentence = sentence.decode('utf-8')
        __obs = self.__viterbi(sentence)[1]
        word = []
        __index = 0
        __size = len(sentence)
        while __index < __size:
            if __obs[__index] == 's':
                word.append(sentence[__index])
                __index = __index + 1
            elif __obs[__index] == 'b':
                __word = []
                while __obs[__index] != 'e':
                    __word.append(sentence[__index])
                    __index = __index + 1
                __word.append(sentence[__index])
                word.append(''.join(__word))
                __index = __index + 1
            else:
                print __obs[__index]
        return word


if __name__ == '__main__':
    t = trainHmm()
    t.train('pku_training.utf8')
    # print t.segment([u'我', u'爱', u'我', u'的', u'祖', u'国', u'。'])
    print ' '.join(t.segment(u'南京市长江大桥今天竣工！'))
    print ' '.join(t.segment(u'李旭泽，想投奔搜狐新闻客户端可以联系我哈，我直送他们领导老蔡，哈哈。。'))
    t.save_state()
