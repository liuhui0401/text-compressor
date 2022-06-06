"""Process Chinese documents into Huffman strings.

    Args:
        txt_list: segment the words, build a heap and 
            build the huffman tree.
    
    Returns:
        A file in the form of npy, which stores the 
            huffman tree.
"""

import heapq
import jieba
import numpy as npy
import os
import sys
from tqdm import tqdm


os.chdir(sys.path[0] + "/text")
txt_list = [
    "sanguoyanyi.txt",
    "liaozhai.txt",
    "suiyuanshidan.txt",
    "shuihuzhuan.txt",
    "yueyanglouji.txt",
]

# Count the word frequency
word_dict = {}
novel_len = 0
for txt in tqdm(txt_list):
    novel = ""
    with open(txt, "r") as f:
        novel = f.read()
    novel_len += len(novel)
    word_list = jieba.lcut(novel)
    for word in word_list:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
print("novel_len=", novel_len)

# Build the heap for words
heap = []
for (key, val) in word_dict.items():
    heapq.heappush(heap, (val, key))
print(len(heap))

# Record phrases with a frequency greater than 40,
# all others are split into single-character records.
single_word = {}
total_size = 0
maxx = 0
word_limit = 40
while heap[0][0] < word_limit:
    tmp = heapq.heappop(heap)
    l = len(tmp[1])
    total_size += l * tmp[0]
    for i in range(l):
        if tmp[1][i] in single_word:
            single_word[tmp[1][i]] += 1
            maxx = max(maxx, single_word[tmp[1][i]])
        else:
            single_word[tmp[1][i]] = 1
print(total_size, len(single_word), len(heap), maxx)

# Build the heap for single words
for (key, val) in single_word.items():
    heapq.heappush(heap, (val, key))

# Suppose there are 1000 uncounted characters,
# we use special characters to represent and construct Huffman trees
heapq.heappush(heap, (1000, "qaz666"))
huffman_dict = {}
bit_to_huff = {}


# Generate Huffman codes
class Node(object):
    def __init__(self, name=None, value=None):
        self._name = name
        self._value = value
        self._left = None
        self._right = None


class HuffmanTree(object):
    maxlen = 0
    minlen = 1000

    # According to the idea of the Huffman tree:
    # based on the node, build the Huffman tree in reverse
    def __init__(self, char_weights):
        # Generate nodes based on the input characters and their frequency
        self.Leav = [Node(part[1], part[0]) for part in char_weights]
        while len(self.Leav) != 1:
            self.Leav.sort(key=lambda node: node._value, reverse=True)
            c = Node(value=(self.Leav[-1]._value + self.Leav[-2]._value))
            c._left = self.Leav.pop(-1)
            c._right = self.Leav.pop(-1)
            self.Leav.append(c)
        self.root = self.Leav[0]
        self.Buffer = list(range(30))

    # Use recursive ideas to generate codes
    def pre(self, tree, length):
        self.maxlen = max(self.maxlen, length)
        node = tree
        if not node:
            return
        elif node._name:
            tmp_str = ""
            for i in range(length):
                tmp_str += str(self.Buffer[i])
            huffman_dict[node._name] = tmp_str
            bit_to_huff[tmp_str] = node._name
            self.minlen = min(self.minlen, length)
            return
        self.Buffer[length] = 0
        self.pre(node._left, length + 1)
        self.Buffer[length] = 1
        self.pre(node._right, length + 1)

    # Generate and save Huffman codes
    def save_code(self):
        self.pre(self.root, 0)
        os.chdir(sys.path[0])
        npy.save("./static/huffman_dict.npy", huffman_dict)
        npy.save("./static/bit_to_huff.npy", bit_to_huff)
        print(self.mnlen, self.mxlen)


print("len(heap):", len(heap))
tree = HuffmanTree(heap)
tree.save_code()
