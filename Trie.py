#coding=utf-8
#!/usr/bin/env python




class TrieNode(object):
    
    def __init__(self):
        self.value = 0
        self.children = {}



class Trie:
    
    
    def __init__(self):
        self.root = TrieNode()
    
    
    def add(self , words , value):
        node = self.root
        for word in words.decode("utf-8"):
            if node.children.has_key(word):
                node = node.children[word]
            else:
                t = TrieNode()
                node.children[word] = t
                node = t
        node.value = value
    
    
    def search(self , words):
        node = self.root
        isFind = True
        for word in words.decode("utf-8"):
            isFind = False
            if not node.children.has_key(word):
                return False
            else:
                node = node.children[word]
                isFind = True
        return isFind
    
if __name__ == "__main__":
    t = Trie()
    t.add("我爱天安门", 1)
    print t.search("他爱")
    
                
        
                
                
            
        
        