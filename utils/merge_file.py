#!/usr/bin/env python3

import os
import re
import datetime

SHELL = 'ffmpeg -i'
SELL_PARAM = '-c copy'
FILE_RULE = re.compile('^video(\d\d\d)\.ts$')
TARGET_DIR = '/home/think/Samba/videos/touch/'


def merge_file(path):
    pass


def get_current_dir():
    pwd = os.getcwd()
    dir_list = pwd.spilit('/')
    return dir_list[-1]


def get_file_list():
    pass


def move_file():
    pass


def create_default_dir():
    current_time =


if __name__ == "__main__":
    merge_file('.')
