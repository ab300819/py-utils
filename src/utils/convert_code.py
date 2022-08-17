#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'mason'

import codecs
import os
import platform

import chardet

if platform.system().startswith('Windows'):
    try:
        from winmagic import magic
    except ImportError:
        print('Not found magic.Please try to run \'pip install python-magic-win64\' to install.')
elif platform.system().startswith('Darwin'):
    try:
        import magic
    except ImportError:
        print('Not found magic.Please try to run \'brew install libmagic\' and \'pip install python-magic\' to install.')

target_code = 'utf-8'
target_path = 'C:\\Users\\mengshen\\Documents\\Project\\MIC'
include_file = ['properties', 'asp', 'cgi', 'log', 'js', 'jsp', 'do', 'mno', 'pl', 'vm', 'xsd', 'meta', 'css', 'MF',
                'cfc', 'jspf', 'java', 'py', 'dtd', 'mail', 'htc', 'cfm', 'xml', 'php', 'json', 'ascx', 'aspx', 'txt',
                'tld', 'lasso', 'html']


def check_text_file(file_path):
    try:
        file_format_info = magic.from_file(file_path)
    except PermissionError:
        file_format_info=''    
    return 'text' in file_format_info


# 遍历所有文件
def walk_all_text_file(path):
    result=[]
    all = os.walk(path)
    for root, dir_list, file_list in all:
        result+=[os.path.join(root, file_name) for file_name in file_list if check_text_file(os.path.join(root, file_name))]
    return result


def list_suffix(path):
    suffix_list = set()
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            suffix = os.path.splitext(file_name)[-1][1:]
            suffix_list.add(suffix)
    return suffix_list


def convert_to_target(path):
    print("convert file:" + path)
    with open(path, 'rb') as f:
        content = f.read()
        code = chardet.detect(content)['encoding']
        if code is None or code == 'utf-8':
            print("unknown encode:" + path)
            return
        print("file code:" + code)
        if code.lower() == 'gb2312':
            code = 'gb18030'

        try:
            with open(path, 'r', encoding=code) as t:
                content_str = t.read()
                codecs.open(path, 'w', encoding=target_code).write(content_str)
                print("encode file:" + path)
        except LookupError:
            print("error encode" + path)
        except UnicodeDecodeError:
            print("error encode" + path)


if __name__ == '__main__':
    file_list = walk_all_text_file("C:\\Users\\mengshen\\Desktop")
    for file in file_list:
        convert_to_target(file)
