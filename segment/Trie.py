# coding=utf-8
#!/usr/bin/env python


class TrieNode(object):

    def __init__(self):
        self.value = 0
        self.children = {}


class Trie(object):

    def __init__(self):
        self.root = TrieNode()

    def __eq__(self, word):
        if word and isinstance(word, (str, unicode)):
            return self.search(word)
        return False

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, key):
        return self.search(key)

    def add(self, words, value):
        if not (words and isinstance(words, (str, unicode)) and value and isinstance(value, (int, float))):
            return
        node = self.root
        for word in words.decode("utf-8"):
            if node.children.has_key(word):
                node = node.children[word]
            else:
                t = TrieNode()
                node.children[word] = t
                node = t
        node.value = value

    def search(self, words):
        if not (words and isinstance(wrods, (str, unicode))):
            return False
        node = self.root
        isFind = False
        for word in words.decode("utf-8"):
            isFind = False
            if not node.children.has_key(word):
                return False
            else:
                node = node.children[word]
                if node.value > -1:
                    isFind = True
        return isFind

if __name__ == "__main__":
    t = Trie()
    t.add("我爱天安门", 1)
    print t == '天爱'
