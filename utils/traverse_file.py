#!/usr/bin/env python3

__author__ = 'mason'

import hashlib as codec
import os
import sys

"""
遍历文件夹内所有文件，并计算 md5
"""


def find_all_file(root):
    for root, dir_list, file_list in os.walk(root):
        for file_name in file_list:
            yield os.path.join(root, file_name)


def check_md5(file_name: str):
    with open(file_name, 'rb') as f:
        md5 = codec.md5()
        md5.update(f.read())
        mdd_hash = str(md5.hexdigest())
    return mdd_hash


if __name__ == '__main__':
    root_path = sys.argv[1]
    result = []
    for full_file_name in find_all_file(root_path):
        md5_sum = ["'" + full_file_name + "'", check_md5(full_file_name)]
        result.append(md5_sum)
    with open(root_path.strip(os.sep) + '_file_md5', 'w') as f:
        for file in result:
            cell = ':'.join(file) + '\n'
            f.write(cell)
