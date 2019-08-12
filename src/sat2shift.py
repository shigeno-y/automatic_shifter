#!/usr/bin/env python3
# coding=utf-8
"""
Copyright 2019
SHIGENO Yoshitaka <shigeno@coop.nagoya-u.ac.jp>

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
"""

import sys
from collections import defaultdict
import argparse
import csv

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('people',
                        type=argparse.FileType('r'),
                        help='People CSV')
    parser.add_argument('works',
                        type=argparse.FileType('r'),
                        help='Works CSV.')
    parser.add_argument('infile',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='Output of SAT Solver (default: stdin)')
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
            'id' : tmp[0],
            'type' : tmp[1],
            'label' : tmp[2],
            'time' : tmp[3],
        }

    assign_result = defaultdict(list)
    first_line = True
    instrings = []
    for line in args.infile.readlines():
        line = line.strip()
        if(first_line):
            if(line == 'SAT'):
                first_line = False
                continue
            else:
                print('Input is not sat.', file=sys.stderr)
                sys.exit(1)
        tmp = line.split()
        instrings = sum(instrings, tmp)

    for s in instrings:
        s = int(s)
        if(s>0):
            w = s//1000
            p = s%1000
            assign_result[p].append(works[w])

    for pid in assign_result.keys():
        print(pid, end='')
        timetable = people[pid]['time']
        for w in assign_result[pid]:
            for (i, j) in enumerate(w['time']):
                timetable[i] = w['id']*-1 if (j == 1) else timetable[i]
        for wid in timetable:
            print(','+str(wid), end='')
        print()
