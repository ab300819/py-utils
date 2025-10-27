#!/usr/bin/env python3

import os
import re
import datetime
import shutil
import subprocess as sp
import mysql.connector as database
from mysql.connector import IntegrityError

PREFIX_DIR = '/Users/mengshen/Desktop/'
TARGET_DIR = 'result2/'
SHELL = 'ffmpeg -i'
SELL_PARAM = '-c copy'
FILE_RULE = re.compile('^video(\d+)\.ts$')


def merge_file(file_dir):
    for i in file_dir:
        os.chdir(PREFIX_DIR+i)
        dir_list = os.listdir()
        file_list = get_file_list(dir_list)
        print(file_list)
        file_name = ['video'+x+'.ts' for x in file_list]
#       print(file_name)
        file_contact = '|'.join(file_name)
#       print(file_contact)
        contact_shell = SHELL+' "concat:'+file_contact+'" '+SELL_PARAM+' "'+i+'.ts"'
        print(contact_shell)
        sp.call(contact_shell, shell=True)
        move_file(i+'.ts', PREFIX_DIR+TARGET_DIR+i+'.ts')


# 获取已下载文件名列表
def get_file_list(dir_list):
    file_list = []
    for value in dir_list:
        check_download_file_name(value, file_list)
    file_list.sort()
    return file_list

# 判断已下载文件文件名合法性


def check_download_file_name(file_name, file_list):
    if os.path.isfile(file_name):
        match_result = FILE_RULE.match(file_name)
        if match_result:
            file_list.append(match_result.group(1))

# 将已合并文件移动到指定文件夹


def move_file(source, target):
    shutil.move(source, target)

# 获取将要下载的文件名


def get_will_download_file():
    conn = database.connect(user='root', password='110119',
                            database='test', host='localhost')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id,title FROM video_list WHERE title LIKE '1000%' AND rate>50")
    select_values = cursor.fetchall()
    conn.close()
    return select_values


def get_current_dir():
    pwd = os.getcwd()
    dir_list = pwd.spilit('/')
    return dir_list[-1]


def create_default_dir():
    pass
    # current_time =


if __name__ == "__main__":
    downlaod_file = get_will_download_file()
    file_dir = [x[1] for x in downlaod_file]
    merge_file(file_dir)
