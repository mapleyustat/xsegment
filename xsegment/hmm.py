# coding=utf-8
#!/usr/bin/env python

from collections import defaultdict
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


state = defaultdict(int)
start_state = {'s': 0, 'b': 0}

transition_probability = {
    's': {'s': 0,  'b': 0, 'm': 0, 'e': 0}, 'b': {'s': 0,  'b': 0, 'm': 0, 'e': 0},
    'm': {'s': 0,  'b': 0, 'm': 0, 'e': 0}, 'e': {'s': 0,  'b': 0, 'm': 0, 'e': 0}}
emission_probability = {'s': {}, 'e': {}, 'b': {}, 'm': {}}


with open('pku_training.utf8') as f:
    for line in f.readlines():
        text_arry = line.strip().split(' ')
        if len(text_arry[0].decode('utf-8')) > 1:
            start_state['b'] += 1
        else:
            start_state['s'] += 1
        word_label = []
        for word in text_arry:
            word = word.decode('utf-8')
            word = word.strip()
            if len(word) == 1:
                word_label.append('s')
                state['s'] = state['s'] + 1
            elif len(word) == 2:
                word_label.append('b')
                word_label.append('e')
                state['b'] += 1
                state['e'] += 1
            elif len(word) > 2:
                word_label.append('b')
                for i in range(len(word[1:-2])):
                    word_label.append('m')
                word_label.append('e')
                state['b'] += 1
                state['m'] += len(word[1:-2])
                state['e'] += 1
        for i in range(len(word_label) - 1):
            transition_probability[word_label[i]][word_label[i + 1]] += 1
print state
print start_state
print transition_probability
