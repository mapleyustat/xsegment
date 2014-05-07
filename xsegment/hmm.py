# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class trainHmm(object):
    state = defaultdict(int)
    # 开始状态矩阵构建
    start_state = {'s': 0, 'b': 0, 'm': 0, 'e': 0}
    # 隐藏状态转移
    transition_probability = {
        's': {'s': 0,  'b': 0, 'm': 0, 'e': 0}, 'b': {'s': 0,  'b': 0, 'm': 0, 'e': 0},
'm': {'s': 0,  'b': 0, 'm': 0, 'e': 0}, 'e': {'s': 0,  'b': 0, 'm': 0, 'e': 0}}
    # 隐藏状态下各个观察状态发生频率
    emission_probability = {'s': defaultdict(int), 'e': defaultdict(
                            int), 'b': defaultdict(int), 'm': defaultdict(int)}

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
                    self.state[word_label[i][0]] += 1
                    self.emission_probability[
                        word_label[i][0]][word_label[i][1]] += 1


t = trainHmm()
t.train('pku_training.utf8')
t.save_state()
