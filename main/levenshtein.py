#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/2/6 10:06
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


def lev_dist(str1, str2):
    if str1 == "":
        return len(str2)
    if str2 == "":
        return len(str1)

    if str1[-1] == str2[-1]:
        cost = 0
    else:
        cost = 1

    res = min(
        lev_dist(str1[: -1], str2) + 1,
        lev_dist(str1, str2[: -1]) + 1,
        lev_dist(str1[: -1], str2[: -1]) + cost
    )
    return res

if __name__ == "__main__":
    print(lev_dist('school', 'sch'))
