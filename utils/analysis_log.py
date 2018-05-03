#!/usr/bin/env python3

import sys

print('参数个数：%d' % len(sys.argv))
# print('参数名称：%s' % sys.argv[1])


def read_file(file_path):
    with open(file_path, 'r') as f:
        f.read()


if __name__ == '__main__':
    match_rule = r'^[response|response]\(([0-9a-zA-Z]{32})\)$'
    file_path = 'C:\\Users\\lenovo\\Desktop\\application_external.log.2018-03-07.4'
    read_file(file_path)
