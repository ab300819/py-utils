#! -*- coding: utf-8 -*-

import logging as log
import re
import urllib.error as HttpError
from html.parser import HTMLParser
from urllib import request, parse

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
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''

log.basicConfig(level=log.INFO)


class MovieInfo(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info = []
        self.tag = None

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag == 'a':
            self.tag = None

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == 'a':
            self.tag = 'a'

    def handle_data(self, data):
        super().handle_data(data)
        if self.tag != 'a':
            if '状态' not in data:
                self.info.append(data.lstrip())

    def error(self, message):
        pass


def get_page_part(url, match=None):
    user_agent = {'User-Agent':
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    response = request.Request(url, headers=user_agent)

    try:
        content = request.urlopen(response, timeout=10)
        page = content.read().decode('gbk', 'ignore')
    except HttpError:
        print(HttpError.HTTPError.code)
        page = None

    if page and match:
        jquery = pq(page)
        select = jquery(match).html()
        return select
    else:
        return page


def get_movie_download(url):
    down_url = {}
    movie_download = []

    down_html = get_page_part(url, match='.ndownlist')
    if not down_html:
        return None

    target = re.search(r'<script>var GvodUrls = "(.*)";</script>', down_html)
    if not target:
        return None
    download = re.split(r'#+', target.group(1))

    file_name_match = re.compile(r'\|(.*)\|(.*)\.mp4')

    for item in download:
        file_name = re.search(file_name_match, item)
        if not file_name:
            return None
        down_url[parse.unquote(file_name.group(2))] = item

    movie_download.append(down_url)
    return movie_download


def get_movie(url, url_title):
    movie_list = pq(get_page_part(url, match='.mlist'))
    movie_item = movie_list('li')
    movies = []

    for item in movie_item:
        movie_content = get_movie_content(item)
        movie_link = get_movie_url(item)
        movie_url = url_title + movie_link[0]
        movie_content.append(movie_link[1])
        movie_download = get_movie_download(movie_url)
        if not movie_download:
            movie_download = 'no download url'
        movies.append(list_2_dict(movie_content, movie_download))

    return movies


def list_2_dict(info, download):
    item = ['时间', '主演', '地区', '类型', '更新', '片名']
    movie = dict(zip(item, info))
    movie['download'] = download
    # log.info(movie)

    return movie


def get_movie_content(item):
    content = []
    match = r'(.*)：(.*)'
    parser = MovieInfo()
    parser.feed(pq(item).html())
    for item in parser.info:
        check = re.search(match, item)
        if check:
            content.append(check.group(2))
        else:
            content.append(item)

    return content


def get_movie_url(item):
    url_info = []
    url = pq(item)
    url_info.append(url('.p').attr('href'))
    url_info.append(url('.p').attr('title'))
    return url_info


if __name__ == '__main__':
    main_url = 'http://www.xiamp4.com'
    url = 'http://www.xiamp4.com/GvodHtml/15.html'
    movies = []

    catalog = get_page_part(url, match='.pages.uppages')

    page_num = re.search(r'(\d)/(\d\d\d)', catalog).group(2)
    total_page = int(page_num)

    for i in range(1, total_page + 1):
        if i == 1:
            print('开始第1组网页')
            movies = get_movie(url, main_url)
            # storage_data.connect('localhost', 27017).insert_many(get_movie(url, main_url))
        else:
            print('开始第%d组网页' % i)
            next_url = main_url + '/GvodHtml/15_' + str(i) + '.html'
            log.info(next_url)

            movie_group = get_movie(next_url, main_url)
            movies.append(movie_group)

            log.info(movie_group)

            # storage_data.connect('localhost', 27017).insert_many(movie_group)
