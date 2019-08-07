#!/usr/bin/env python3
# coding=utf-8
"""
Copyright 2018 SHIGENO Yoshitaka <shigeno@coop.nagoya-u.ac.jp>

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
"""

import argparse
from collections import defaultdict, deque
import sys
import csv

def BreadthFirstSearch(C, E, F, s, t, N):
    m = 0
    P = [-1 for i in range(N)]
    P[s] = -2
    M = [0 for i in range(N)]
    M[s] = sys.maxsize
    Q = deque()
    Q.append(s)
    while (len(Q) > 0):
        u = Q.pop()
        for v in E[u]:
            #（まだ容量があり、v がまだ探索されていなかった場合）
            if (C[u][v] - F[u][v] > 0 and P[v] == -1):
                P[v] = u
                M[v] = min(M[u], C[u][v] - F[u][v])
                if (v != t):
                    Q.append(v)
                else:
                    return M[t], P
    return 0, P


def EdmondsKarp(C:list, E:list, s:int, t:int, N:int):
    """
    エドモンズ・カープ法
    Thanks to https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm
    
    Arguments:
        C {list} -- list of list denotes edges' capacity.
        E {list} -- list of list denotes edges.
        s {int} -- start node id
        t {int} -- end node id
        N {int} -- size of Matrix
    """
    f = 0
    F = [ [0 for i in range(N)] for j in range(N)]

    while(True):
        m, P = BreadthFirstSearch(C, E, F, s, t, N)
        if (m == 0):
            break
        f += m
        v = t
        while(v != s):
            u = P[v]
            F[u][v] += m
            F[v][u] -= m
            v = u
    return f, F

if(__name__ == "__main__"):
    def p_id(pid:int):
        return pid+2000

    def w_id(wid:int):
        return wid+1000
    
    def peg_id(pid:int, gid:int):
        return pid*10000+gid+1

    parser = argparse.ArgumentParser(description="automatic shifter")
    parser.add_argument('people',
                        type=argparse.FileType('r'),
                        help='People CSV')
    parser.add_argument('works',
                        type=argparse.FileType('r'),
                        help='Works CSV.')
    parser.add_argument('--retry',
                        type=int,
                        default=5,
                        help='Aborts when we cannot assign any jobs in last (retry count) iterations')
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
            'id' : tmp[0],
            'white_list' : tmp[1],
            'time' : tmp[2]
        }

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
            'id' : tmp[0],
            'type' : tmp[1],
            'label' : tmp[2],
            'time' : tmp[3],
        }

    START_NODE = 1
    END_NODE = 2
    edges = []
    for p in people.values():
        edges.append( (START_NODE, p_id(p['id']), 20) )
    for w in works.values():
        edges.append( (w_id(w['id']), END_NODE, 1) )
    for p in people.values():
        personal_exclusive_groups = [
            [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]],
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]],
        ]
        for w in works.values():
            is_free_time = all(map(
                lambda w,p: (w == 1 and p == 1) or (w == 0),
                w['time'],
                p['time']
            ))
            is_in_whitelist = w['type'] in p['white_list']
            if(is_free_time and is_in_whitelist):
                for g in personal_exclusive_groups:
                    if(any(map(lambda x,y: x==1 and y==1, g[0], w['time']))):
                        g.append(w)

        for i, g in enumerate(personal_exclusive_groups):
            if(len(g)>1):
                edges.append( (p_id(p['id']), peg_id(p['id'], i), 1) )
                for j in g[1:]:
                    edges.append( (peg_id(p['id'], i), w_id(j['id']), 1) )

    idMapping = [START_NODE, END_NODE]
    for (f, t, c) in edges:
        if(not f in idMapping):
            idMapping.append(f)
        if(not t in idMapping):
            idMapping.append(t)

    N = len(idMapping)
    C = defaultdict(lambda: defaultdict(lambda: 0))
    E = defaultdict(list)
    index = idMapping.index
    for (f, t, c) in edges:
        C[index(f)][index(t)] = c
        E[index(f)].append(index(t))

    f, F = EdmondsKarp(C, E, 0, 1, N)
    print('Jobs Assigned :' + str(f) + ' of '+str(len(works)), file=sys.stderr)
    result = []
    for from_id, row in enumerate(F):
        for to_id, val in enumerate(row):
            if(val > 0):
                #print(from_id, to_id, sep='\t')
                #print(idMapping[from_id], idMapping[to_id], sep='\t')
                result.append( (idMapping[from_id], idMapping[to_id]) )

    tmp = defaultdict(list)
    for (f, t) in result:
        tmp[f].append(t)

    assign_result = defaultdict(list)
    keys = tmp.keys()
    for k in keys:
        for kk in tmp[k]:
            if(kk in keys):
                for kkk in tmp[kk]:
                    if(kkk in keys):
                        for kkkk in tmp[kkk]:
                            if(kkkk in keys):
                                print(kk-2000, kkkk-1000)
                                assign_result[kk-2000].append(works[kkkk-1000])

    for pid in assign_result.keys():
        print(pid, end='')
        timetable = people[pid]['time']
        for w in assign_result[pid]:
            for (i, j) in enumerate(w['time']):
                timetable[i] = w['id']*-1 if (j == 1) else timetable[i]
        for wid in timetable:
            print(','+str(wid), end='')
        print()
