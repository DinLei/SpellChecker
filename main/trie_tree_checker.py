#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/2/5 14:31
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

import re
from functools import wraps
from collections import deque


def uniqueness(func):
    @wraps(func)
    def _func(*a, **kw):
        seen = set()
        it = func(*a, **kw)
        while 1:
            x = next(it)
            if x not in seen:
                yield x
                seen.add(x)
    return _func


class TrieTree:
    def __init__(self, corpus):
        self._tree = self.make_trie(
            self._words(open(corpus).read())
        )
        self.candidate = set()

    @staticmethod
    def make_trie(words):
        """构造Trie（用dict登记结点信息和维持子结点集合）"""
        trie = {}
        for word in words:
            t = trie
            for c in word:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t[None] = None
        return trie

    @staticmethod
    def _words(text):
        """读取文本单词作为训练数据"""
        return re.findall(r'\w+', text.lower())

    @uniqueness
    def search(self, word, tol=1):
        q = deque([(self._tree, word, '', tol)])
        while q:
            trie, word, path, tol = q.popleft()
            if word == '':
                if None in trie:
                    if path not in self.candidate:
                        self.candidate.add(path)
                        yield path
                if tol > 0:
                    for k in trie:
                        if k is not None:
                            q.appendleft((trie[k], '', path + k, tol - 1))
            else:
                if word[0] in trie:
                    q.appendleft((trie[word[0]], word[1:], path + word[0], tol))
                if tol > 0:
                    for k in trie.keys():
                        if k is not None and k != word[0]:
                            q.append((trie[k], word[1:], path + k, tol - 1))
                            q.append((trie[k], word, path + k, tol - 1))
                    q.append((trie, word[1:], path, tol - 1))
                    if len(word) > 1:
                        q.append((trie, word[1] + word[0] + word[2:], path, tol - 1))


if __name__ == "__main__":
    trie_spc = TrieTree("../data/training.txt")
    print(list(trie_spc.search('schol')))

