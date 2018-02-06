#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/1/4 8:46
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com
import re
from collections import Counter


class BufferedSPC:
    def __init__(self, corpus):
        """
        :param corpus: 训练文本路径
        """
        self._corpus_dict = Counter(
            self._words(open(corpus).read())
        )

    @staticmethod
    def _words(text):
        """读取文本单词作为训练数据"""
        return re.findall(r'\w+', text.lower())

    def _prob(self, word):
        """单词`word`的频率"""
        return self._corpus_dict[word] / sum(self._corpus_dict.values())

    def correction(self, word):
        """单词`word`的纠错最佳推荐"""
        return max(self.search(word), key=self._prob)

    def search(self, word):
        """单词`word`的候选纠错"""
        return (self.known([word]) or
                self.known(self.edits1(word)) or
                self.known(self.edits2(word)) or
                [word])

    def known(self, possible_words):
        """与单词`words`在一定编辑距离内且真实存在的单词"""
        return set(w for w in possible_words if w in self._corpus_dict)

    @staticmethod
    def edits1(word):
        """与单词`word`编辑距离为1的字符串"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """与单词`word`编辑距离为2的字符串"""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
