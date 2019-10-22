import codecs
import os

import chardet

target_code = 'utf-8'
target_path = 'C:\\Users\\mengshen\\Documents\\Project\\MIC'
include_file = ['properties', 'asp', 'cgi', 'log', 'js', 'jsp', 'do', 'mno', 'pl', 'vm', 'xsd', 'meta', 'css', 'MF',
                'cfc', 'jspf', 'java', 'py', 'dtd', 'mail', 'htc', 'cfm', 'xml', 'php', 'json', 'ascx', 'aspx', 'txt',
                'tld', 'lasso', 'html']


# 遍历所有文件
def list_all_file(path):
    result = []
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            suffix = os.path.splitext(file_name)[-1][1:]
            if suffix.lower() in include_file:
                file_path = os.path.join(path, file_name)
                print(file_path)
                result.append(file_path)
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
    file_list = list_all_file(target_path)
    for file in file_list:
        convert_to_target(file)
