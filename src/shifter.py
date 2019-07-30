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
    args = parser.parse_args()

    people = []
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
        people.append({
            'id' : tmp[0],
            'white_list' : tmp[1],
            'service_time' : tmp[2]
        })
    print(people)

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
        """
        to feed `works_bad.csv', use this script:
        job_tmp = []
        for t in [i / 2 for i in range(18, 35)]:
            if(tmp[3] <= t and t < tmp[4]):
                job_tmp.append(1)
            else:
                job_tmp.append(0)
        works.append([
            tmp[0],
            tmp[1],
            tmp[2],
            job_tmp,
        })
        """
        works.append({
            'id' : tmp[0],
            'type' : tmp[1],
            'label' : tmp[2],
            'job_time' : tmp[3],
        })
    print(works)

    for w in works:
        job_time = w['job_time']
        matched = None
        for p in people:
            is_matched = (all(map(
                lambda x,y: (x==1 and x==y) or x==0,
                job_time,
                p['service_time']
            )))
            if(is_matched):
                matched = p
                break
        print(matched)

