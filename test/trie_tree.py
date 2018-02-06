#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/2/5 9:07
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

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


def check_fuzzy(trie, word, path='', tol=1):
    """
    思路：实质上是对Trie的深度优先搜索，每一步加深时就消耗目标词的一个字母。
    当搜索到达某个结点时，分为不消耗容错数和消耗容错数的情形，继续搜索直到目标词为空。
    搜索过程中，用path记录搜索路径，该路径即为一个词典中存在的词，作为纠错的参考。
    最终结果即为诸多搜索停止位置的结点路径的并集。
    """
    if tol < 0:
        return set()
    elif word == '':
        results = set()
        if None in trie:
            results.add(path)
        # 增加词尾字母
        for k in trie:
            if k is not None:
                results |= check_fuzzy(trie[k], '', path + k, tol - 1)
        return results
    else:
        results = set()
        # 首字母匹配
        if word[0] in trie:
            results |= check_fuzzy(trie[word[0]], word[1:], path + word[0], tol)
        # 分情形继续搜索（相当于保留待探索的回溯分支）
        for k in trie:
            if k is not None and k != word[0]:
                # 用可能正确的字母置换首字母
                results |= check_fuzzy(trie[k], word[1:], path + k, tol - 1)
                # 插入可能正确的字母作为首字母
                results |= check_fuzzy(trie[k], word, path + k, tol - 1)
        # 跳过余词首字母
        results |= check_fuzzy(trie, word[1:], path, tol - 1)
        # 交换原词头两个字母
        if len(word) > 1:
            results |= check_fuzzy(trie, word[1] + word[0] + word[2:], path, tol - 1)
        return results


@uniqueness
def check_lazy(trie, word, path='', tol=1):
    if tol < 0:
        pass
    elif word == '':
        if None in trie:
            yield path
        # 增加词尾字母
        for k in trie:
            if k is not None:
                yield from check_lazy(trie[k], '', path + k, tol - 1)
    else:
        if word[0] in trie:
            # 首字母匹配成功
            yield from check_lazy(trie[word[0]], word[1:], path+word[0], tol)
        # 分情形继续搜索（相当于保留待探索的回溯分支）
        for k in trie:
            if k is not None and k != word[0]:
                # 用可能正确的字母置换首字母
                yield from check_lazy(trie[k], word[1:], path+k, tol-1)
                # 插入可能正确的字母作为首字母
                yield from check_lazy(trie[k], word, path+k, tol-1)
        # 跳过余词首字母
        yield from check_lazy(trie, word[1:], path, tol-1)
        # 交换原词头两个字母
        if len(word) > 1:
            yield from check_lazy(trie, word[1]+word[0]+word[2:], path, tol-1)


def check_iter(trie, word, tol=1):
    seen = set()
    q = deque([(trie, word, '', tol)])
    while q:
        trie, word, path, tol = q.popleft()
        if word == '':
            if None in trie:
                if path not in seen:
                    seen.add(path)
                    yield path
            if tol > 0:
                for k in trie:
                    if k is not None:
                        q.appendleft((trie[k], '', path+k, tol-1))
        else:
            if word[0] in trie:
                q.appendleft((trie[word[0]], word[1:], path+word[0], tol))
            if tol > 0:
                for k in trie.keys():
                    if k is not None and k != word[0]:
                        q.append((trie[k], word[1:], path+k, tol-1))
                        q.append((trie[k], word, path+k, tol-1))
                q.append((trie, word[1:], path, tol-1))
                if len(word) > 1:
                    q.append((trie, word[1]+word[0]+word[2:], path, tol-1))


def combinations(seq, m):
    if m > len(seq):
        raise ValueError('Cannot choose more than sequence has.')
    elif m == 0:
        yield ()
    elif m == len(seq):
        yield tuple(seq)
    else:
        for p in combinations(seq[1:], m-1):
            yield (seq[0],) + p
        yield from combinations(seq[1:], m)


if __name__ == "__main__":
    for combi in combinations('abcde', 2):
        print(combi)
