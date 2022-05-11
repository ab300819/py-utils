#!/usr/bin/env python3

__author__ = 'mason'

import codecs
import os
import sys

import chardet

"""
转换文件编码
"""


def find_all_file(path):
    for root, dir_list, file_list in os.walk(path):
        for file_name in file_list:
            yield os.path.join(root, file_name)


def convert(file_name: str, from_code, to_code='UTF-8'):
    with codecs.open(file_name, 'r', from_code) as in_file:
        in_file_content = in_file.read()
    with codecs.open(file_name, 'w', to_code) as out_file:
        out_file.write(in_file_content)


if __name__ == '__main__':
    root_path = sys.argv[1]
    result = []
    for full_file_name in find_all_file(root_path):
        with open(full_file_name, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
        convert(full_file_name, encoding)
