'''
Copyright (c) 2019.11 Ying He (heyingyouxiang@qq.com). All rights reserved.
'''

import os


def count_lines(filepath):
    return len(open(filepath, 'r').readlines())


def write_lines(filepath,lines):
    with open(filepath,'w') as fw:
        fw.writelines(lines)

def read_lines(filepath):
    return open(filepath, 'r').readlines()

def return_oswalk(path):
    for root, dirs, files in os.walk(path):
        return root, dirs, files