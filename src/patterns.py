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
from functools import reduce
import random
import sys
import csv

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="automatic shifter")
    parser.add_argument('works',
                        type=argparse.FileType('r'),
                        help='Works CSV.')
    args = parser.parse_args()

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
        works.append(tmp[3])

    for p in set(map(
        lambda x: reduce(lambda a,b: a*2+b, x),
        works
    )):
        tmp = []
        for i in range(17):
            tmp.insert(0, 1 if (p&(1<<i)) else 0)
        print(tmp)
