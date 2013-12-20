#coding=utf-8
#!/usr/bin/env python




class TrieNode(object):
    
    def __init__(self):
        self.value = 0
        self.children = {}



class Trie(object):
    
    
    def __init__(self):
        self.root = TrieNode()
    
    
    def add(self , words , value):
        node = self.root
        if not words:
            return 
        for word in words:
            if node.children.has_key(word):
                node = node.children[word]
            else:
                t = TrieNode()
                node.children[word] = t
                node = t
        node.value = value
    
    
    def search(self , words):
        node = self.root
        isFind = False
        for word in words:
            isFind = False
            if not node.children.has_key(word):
                return False
            else:
                node = node.children[word]
                if node.value > -1:
                    isFind = True
        return isFind

    def find(self , words):
        node = self.root
        value = None
        for word in words:
            if not node.children.has_key(word):
                return None
            else:
                node = node.children[word]
                value = node.value
        if value:
            return value
        else:
            return words
    
if __name__ == "__main__":
    t = Trie()
    t.add("我爱天安门", 1)
    print t.find("我爱")