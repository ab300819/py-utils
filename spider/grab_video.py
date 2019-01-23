#!/usr/bin/env python3
import re
import time
import xmlrpc.client as rpc

import mysql.connector as database
import requests as rqs
from mysql.connector import IntegrityError, InterfaceError
from pyquery import PyQuery as pq

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||_  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |_/ |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. .'___
      ."" '<  `.___\_<|>_/___.'  >' "".
     | | :  `- \`.;`\ _ /`;.`/ -`  : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             佛祖保佑     永无BUG
'''
# http
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
HEADER = {'user-agent': USER_AGENT}

# target
PREFIX = 'http:'
MAIN_URL = 'http://www.888tv.co/videos/'
TYPE = ['3d', 'amateur', 'japanese', 'selfie', 'western']
PARAM = {'page': 1}
TOTAL_PAGE = 32
START_PAGE = 1
SLEEP_TIME = 9
US_TAG = 'HD_US'
CN_TAG = 'HD_CN'

# download
REMOTE = 'localhost'
ARIA2_URL = 'http://' + REMOTE + ':6800/rpc'
ARIA2_TOKEN = 'token:a6516320-9d0f-48dc-bf56-2cdd5314e131'
FILE_PATH = '/home/think/Samba/downloads/'
ARIA2_DIR = 'dir'

# Database
CONNECT = database.connect(host='192.168.9.109', user='root', password='110119', database='test')
CURSOR = CONNECT.cursor()

# Sql
INSERT_VIDEO_LIST = 'INSERT INTO video_list(title,video_id,url,video_type,rate,download_status) values (%s,%s,%s,%s,%s,%s)'
UPDATE_VIDEO_LIST = 'UPDATE video_list SET video_id=%s,video_type=%s where title=%s'
DELETE_VIDEO_LIST = ''
SELECT_VIDEO_LIST = ''

# regex
VIDEO_FILE_URL_RULE = re.compile('^[http|//].+video\d+\.ts$')
VIDEO_URL_RULE = re.compile('^/video/(\d+)/.+')


def get_html_response(url, param=None):
    if param is None:
        html_source = rqs.get(url, headers=HEADER)
    else:
        html_source = rqs.get(url, headers=HEADER, params=param)
    print(html_source.url)
    return html_source.text


def get_video_list(html):
    video_list_result = []
    html_parse = pq(html)
    video_list = html_parse('.col-sm-6.col-md-4.col-lg-4')

    for i in video_list:
        single_video = []
        video = pq(i)
        single_video.append(video('span').text())
        single_video.append(video('a').attr('href'))
        single_video.append(remove_str(video('b').text(), '%'))
        single_video.append(0)
        print(single_video)
        video_list_result.append(tuple(single_video))
    return video_list_result


def get_video_file(html):
    html_parse = pq(html)
    video_source_list = html_parse('source')

    if len(video_source_list) == 0:
        element = pq(video_source_list[0])
        return element.attr('src')

    for i in video_source_list:
        element = pq(i)
        if element.attr('label') is CN_TAG:
            return element.attr('src')


def get_video_file_url(url):
    video_url_list = []

    if PREFIX in url:
        url = PREFIX + url
    video_url_request = get_html_response(url)
    video_list = video_url_request.split('\n')
    if video_list:
        video_url_list = [x for x in video_list if VIDEO_URL_RULE.match(x)]

    return [PREFIX + x for x in video_url_list if PREFIX not in x]


def download_video_list(title, url_List):
    result_list = []

    server = rpc.ServerProxy(ARIA2_URL)
    if url_List:
        for i in url_List:
            result = server.aria2.addUri(ARIA2_TOKEN, [i], {ARIA2_DIR: FILE_PATH + title})
            result_list.append(result)
    return result_list


def remove_str(source, target):
    return source.rstrip(target)


def get_video():
    pass


def get_list():
    pass


def insert_video_list():
    for i in range(START_PAGE, TOTAL_PAGE + 1):
        request_url = MAIN_URL + str(i)
        print(request_url)
        html_res = get_html_response(request_url)
        video_result = get_video_list(html_res)
        print(i)
        try:
            CURSOR.executemany(INSERT_VIDEO_LIST, video_result)
        except (IntegrityError, InterfaceError):
            print("重复")
        CONNECT.commit()
        time.sleep(SLEEP_TIME)
    CONNECT.close()


def update_video_list():
    for i in range(START_PAGE, TOTAL_PAGE + 1):
        request_url = MAIN_URL + TYPE[2]
        PARAM['page'] = i
        html_res = get_html_response(request_url, PARAM)
        video_result = get_video_list(html_res)
        for url in video_result:
            try:
                CURSOR.execute(UPDATE_VIDEO_LIST, update_video_info(url, TYPE[2]))
            except (IntegrityError, InterfaceError):
                print("重复")
        CONNECT.commit()
        time.sleep(SLEEP_TIME)
    CONNECT.close()


# 获取视频更新信息
def update_video_info(video_info, type):
    update_info = []
    update_info.append(get_video_id(video_info[1]))
    update_info.append(type)
    update_info.append(video_info[0])
    return update_info


# 获取视频 id
def get_video_id(video_url):
    match_result = VIDEO_URL_RULE.match(video_url)
    return int(match_result.group(1))


if __name__ == '__main__':
    update_video_list()