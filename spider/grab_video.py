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
MAIN_URL = 'http://www.888tv.co'
TYPE = ['3d', 'amateur', 'japanese', 'selfie', 'western']
PARAM = {'page': 1}
TOTAL_PAGE = 1
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
SELECT_VIDEO_LIST = 'SELECT id,url FROM video_list'
SELECT_VIDEO_ID_LIST_WITH_PAGE = 'SELECT id,url FROM video_list WHERE video_type=%s LIMIT %s OFFSET %s'
SELECT_VIDEO_ID_LIST = 'SELECT id,url FROM video_list WHERE video_type=%s ORDER BY rate DESC'
SELECT_VIDEO_FILE_LIST = 'SELECT vf.url FROM video_list vl JOIN video_file vf ON vf.video_id=vl.id WHERE vl.id=%s'
SAVE_VIDEO_FILE_LIST = 'INSERT INTO video_file(video_id,url,download_status) VALUES (%s,%s,%s)'

# regex
VIDEO_FILE_URL_RULE = re.compile('^[http|//].+video\d+\.ts$')
VIDEO_URL_RULE = re.compile('^/video/(\d+)/.+')


# 获取网页内容
def get_html_response(url, param=None):
    if param is None:
        html_source = rqs.get(url, headers=HEADER)
    else:
        html_source = rqs.get(url, headers=HEADER, params=param)
    print(html_source.url)
    return html_source.text


# 获取视频列表
def get_video_list(html, video_type=None, multi=True):
    video_list_result = []
    html_parse = pq(html)
    video_list = html_parse('.col-sm-6.col-md-4.col-lg-4')

    for i in video_list:
        single_video = []
        video = pq(i)
        single_video.append(video('span').text())
        single_video.append(get_video_id(video('a').attr('href')))
        single_video.append(video('a').attr('href'))
        if video_type:
            single_video.append(video_type)
        else:
            single_video.append('')
        single_video.append(remove_str(video('b').text(), '%'))
        single_video.append(0)
        print(single_video)
        if multi:
            video_list_result.append(tuple(single_video))
        else:
            video_list_result.append(single_video)
    return video_list_result


# 获取视频文件列表
def get_video_file(html):
    html_parse = pq(html)
    video_source_list = html_parse('source')

    if len(video_source_list) == 1:
        element = pq(video_source_list[0])
        return element.attr('src')

    for i in video_source_list:
        element = pq(i)
        if element.attr('label') is CN_TAG:
            return element.attr('src')


# 获取视频 url
def get_video_file_url(id, url):

    if PREFIX not in url:
        url = PREFIX + url
    video_url_request = get_html_response(url)
    video_file_list = video_url_request.split('\n')

    return [tuple([id, x, 0]) for x in video_file_list if VIDEO_FILE_URL_RULE.match(x)]


# 创建批量下载
def download_video_list(title, url_list):
    result_list = []

    server = rpc.ServerProxy(ARIA2_URL)
    if url_list:
        for i in url_list:
            result = server.aria2.addUri(ARIA2_TOKEN, [i], {ARIA2_DIR: FILE_PATH + title})
            result_list.append(result)
    return result_list


# 移除字符串符号
def remove_str(source, target):
    return source.rstrip(target)


def get_video():
    pass


def get_list():
    pass


# 判断该条有没有视频
def check_exist_video_file(video_id):
    video_file_list = query(SELECT_VIDEO_FILE_LIST, video_id)
    if video_file_list:
        return True
    else:
        return False


# 整页保存视频列表
def insert_multi_video_list():
    for i in range(START_PAGE, TOTAL_PAGE + 1):
        request_url = MAIN_URL + str(i)
        print(request_url)
        html_res = get_html_response(request_url)
        video_result = get_video_list(html_res)
        print(i)
        save_multi(INSERT_VIDEO_LIST, video_result)
        time.sleep(SLEEP_TIME)
    CONNECT.commit()


# 单条保存视频信息
def insert_single_video_list(total_page, video_type):
    for i in range(START_PAGE, total_page):
        request_url = MAIN_URL + video_type
        PARAM['page'] = i
        html_res = get_html_response(request_url, PARAM)
        video_result = get_video_list(html_res, multi=False)
        for url in video_result:
            save_single(INSERT_VIDEO_LIST, url)
        CONNECT.commit()
        time.sleep(SLEEP_TIME)


def update_video_list(video_type):
    for i in range(START_PAGE, TOTAL_PAGE + 1):
        request_url = MAIN_URL + video_type
        PARAM['page'] = i
        html_res = get_html_response(request_url, PARAM)
        video_result = get_video_list(html_res)
        for url in video_result:
            save_single(UPDATE_VIDEO_LIST, update_video_info(url, video_type))
        CONNECT.commit()
        time.sleep(SLEEP_TIME)


# 获取视频更新信息
def update_video_info(video_info, video_type):
    return [get_video_id(video_info[1]), video_type, video_info[0]]


# 获取视频 id
def get_video_id(video_url):
    match_result = VIDEO_URL_RULE.match(video_url)
    return int(match_result.group(1))


# 保存单条
def save_single(sql, data):
    try:
        CURSOR.execute(sql, data)
        print('成功：' + str(data))
    except (IntegrityError, InterfaceError):
        print("重复")


# 一次保存多条
def save_multi(sql, data_list):
    try:
        CURSOR.executemany(sql, data_list)
    except (IntegrityError, InterfaceError):
        print("重复")


def query(sql, condition=None):
    query_result = []
    try:
        if condition:
            CURSOR.execute(sql, condition)
        else:
            CURSOR.execute(sql)
        query_result = CURSOR.fetchall()
    except(IntegrityError, InterfaceError):
        print()
    return query_result


if __name__ == '__main__':
    video_id_list = query(SELECT_VIDEO_ID_LIST, [TYPE[3]])
    for video in video_id_list:
        if MAIN_URL not in video[1]:
            video_list = get_video_file(get_html_response(MAIN_URL + video[1]))
        else:
            video_list = get_video_file(get_html_response(video[1]))
        video_file = get_video_file_url(video[0], video_list)
        save_multi(SAVE_VIDEO_FILE_LIST, video_file)
        CONNECT.commit()
        time.sleep(SLEEP_TIME)
    CONNECT.close()
