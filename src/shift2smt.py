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

if(__name__ == "__main__"):
    def p_id(pid: int):
        return pid+5000

    def w_start_id(wid: int):
        return wid+1000

    def w_end_id(base_wid: int):
        return base_wid+3000

    def w_conflict_group_id(base_wid: int):
        return base_wid+2000

    def peg_id(pid: int, gid: int):
        return pid*10000+gid+1

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

    # SMT-LIBに必要な情報を出力しておく
    print('; Shift2SMT 0.1[2019-08-07]')
    print('; SHIGENO Yoshitaka <shigeno@coop.nagoya-u.ac.jp>')
    print('(set-info :smt-lib-version 2.0)')
    print('(set-option :print-success false)')
    print('(set-option :produce-models true)')
    print('(set-option :produce-proofs false)')
    print('(set-option :smt.arith.solver 1)')
    print('(set-option :smt.arith.solver 3)')
    print()
    print('(define-fun binarize ((i Int)) Int')
    print('  (ite (= i 0) 0 1)')
    print(')')
    print()
    # 変数を宣言する(w0 は，works[0]をpeople[w0]がやる，ことに対応)
    print('; declare variables')
    for w in works.values():
        print('(declare-const w{0} Int)'.format(w['id']))
        print('(assert (and (<= 0 w{0}) (<= w{0} {1}) ))'.format(
            w['id'], len(pidMapping)+1))
    print()

    # 時間的に競合する作業は同時に1つまで
    print('; assert no one must split himself/herself into multiple NINJAs')
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
                print('(assert (not (= w{0} w{1})))'.format(w['id'], t['id']))
        tmp.append(w)
    print()

    # ホワイトリストにない作業・本人がいない時間帯は絶対ダメ
    print('; assert nobody serves despite of his/her inconvenient')
    tmp = []
    for p in people.values():
        for w in works.values():
            is_free_time = all(map(
                lambda w, p: (w == 1 and p == 1) or (w == 0),
                w['time'],
                p['time']
            ))
            if(not (is_free_time and w['type'] in p['white_list'])):
                print('(assert (not (= w{0} {1})))'.format(
                    w['id'], pidMapping.index(p['id'])+1))
    print()

    print('(maximize (+ ' +
          ' '.join(['(binarize w{0})'.format(wid) for wid in works.keys()]) + '))')

    print('(check-sat)')
    # print('(get-model)')
    print(
        '(get-value (' + ' '.join(['w{0}'.format(wid) for wid in works.keys()]) + '))')
    print('(exit)')
