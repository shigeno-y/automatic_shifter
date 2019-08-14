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
import random
import sys
import csv

if(__name__ == "__main__"):
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
    assign_result = {}
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
            'white_list': tmp[1],
            'time': tmp[2]
        }
        assign_result[tmp[0]] = []

    works = []
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
        works.append({
            'id': tmp[0],
            'type': tmp[1],
            'label': tmp[2],
            'time': tmp[3],
        })

    unassigned_works = [len(works)]

    while(unassigned_works[-1] > 0):
        for pid in people:
            p = people[pid]
            picked_work = None
            for w in works:
                is_free_time = all(map(
                    lambda w, p: (w == 1 and p == 1) or (w == 0),
                    w['time'],
                    p['time']
                ))
                if(is_free_time and w['type'] in p['white_list']):
                    picked_work = w
            if(picked_work != None):
                p['time'] = list(map(
                    lambda w, p: 0 if w == 1 else p,
                    picked_work['time'],
                    p['time']
                ))
                assign_result[pid].append(picked_work)
                works.remove(picked_work)

        random.shuffle(works)

        unassigned_works.append(len(works))
        if(len(unassigned_works) > args.retry and all([v == unassigned_works[-args.retry] for v in unassigned_works[-(args.retry-1):]])):
            print(str(
                unassigned_works[-1])+' job(s) remeins but NO MORE FREE PEOPLE. ABORT.', file=sys.stderr)
            break

    for pid in assign_result.keys():
        print(pid, end='')
        timetable = people[pid]['time']
        for w in assign_result[pid]:
            for (i, j) in enumerate(w['time']):
                timetable[i] = w['id']*-1 if (j == 1) else timetable[i]
        for wid in timetable:
            print(','+str(wid), end='')
        print()
