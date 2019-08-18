#!/usr/bin/env python3
# coding=utf-8
"""
Copyright 2019 SHIGENO Yoshitaka <shigeno@coop.nagoya-u.ac.jp>

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
"""

import argparse
import csv
from collections import defaultdict

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="automatic shifter")
    parser.add_argument('people',
                        type=argparse.FileType('r'),
                        help='People CSV')
    parser.add_argument('works',
                        type=argparse.FileType('r'),
                        help='Works CSV.')
    args = parser.parse_args()

    people = {}
    people_csv = csv.reader(args.people)
    for row in people_csv:
        tmp = []
        for c in row:
            val = None
            try:
                val = eval(c)
            except NameError:
                val = c
            tmp.append(val)
        people[tmp[0]] = {
            'id': tmp[0],
            'white_list': tmp[1],
            'time': tmp[2]
        }
    pidMapping = sorted(people.keys())

    works = {}
    works_csv = csv.reader(args.works)
    for row in works_csv:
        tmp = []
        for c in row:
            val = None
            try:
                val = eval(c)
            except Exception:
                val = c
            tmp.append(val)
        works[tmp[0]] = {
            'id': tmp[0],
            'type': tmp[1],
            'label': tmp[2],
            'time': tmp[3],
        }

    # 時間的に競合する作業は同時に1つまで
    conflict_works = set()
    tmp = []
    for w in works.values():
        conflicts = []
        for t in tmp:
            is_conflict = any(map(
                lambda w, p: (w == 1 and p == 1),
                w['time'],
                t['time']
            ))
            if(is_conflict):
                conflicts.append(t)
                # conflict_works[w['id']].append(t['id'])
                conflict_works.add((w['id'], t['id']))
        tmp.append(w)

    # ホワイトリストにない作業・本人がいない時間帯は絶対ダメ
    candidate_wx_y = defaultdict(list)
    for p in people.values():
        for w in works.values():
            is_free_time = all(map(
                lambda x, y: (x == 1 and y == 1) or (x == 0),
                w['time'],
                p['time']
            ))
            if(is_free_time and w['type'] in p['white_list']):
                candidate_wx_y[w['id']].append(p['id'])

    # SATにコメントを出力しておく
    print('c Shift2SMT 0.1[2019-08-07]')
    print('c SHIGENO Yoshitaka <shigeno@coop.nagoya-u.ac.jp>')
    buffering = []
    max_var_id = 0

    # すべてのworkに少なくとも1人を割り当てる
    for wid in candidate_wx_y.keys():
        tmp = ''
        for pid in candidate_wx_y[wid]:
            tmp += str(wid*1000+pid) + ' '
        tmp += '0'
        buffering.append(tmp)

    # 時間的に競合する作業は同時に1つまで
    for pid in people.keys():
        for (p, q) in conflict_works:
            x = min(p, q)
            y = max(p, q)
            if (pid in candidate_wx_y[x] and pid in candidate_wx_y[y]):
                buffering.append(
                    '-{0} -{1} 0'.format(x*1000 + pid, y*1000 + pid))
                max_var_id = max(max_var_id, y*1000 + pid)

    print('p cnf {0} {1}'.format(max_var_id, len(buffering)))
    print('\n'.join(buffering))
