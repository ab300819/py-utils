#!-*- coding:utf-8 -*-
# !/usr/bin/env python3

import logging as log
import os
import re
import time
import urllib.error as Error
from urllib import request

from pyquery import PyQuery as pq

log.basicConfig(level=log.INFO)


def get_main_page(url):
    user_agent = {'User-Agent':
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/54.0.2840.71 Safari/537.36'}

    response = request.Request(url, headers=user_agent)

    try:
        content = request.urlopen(response, timeout=10)
        html = content.read().decode('utf-8', 'ignore')

    except Error:
        print('请求网页失败\n错误代码：%d' % Error.HTTPError.code)
        html = None

    return html


def parser_content(content_html, title_match, img_match):
    content = []
    image = []

    page = pq(content_html)
    title_page = page(title_match).text().split('偷拍自拍')
    title = title_page[-1].lstrip()
    content.append(title)

    img_page = page(img_match)
    for p in img_page('p'):
        item = pq(p)
        src = item('img').attr('src')
        if src:
            image.append('http:' + src)
    content.append(image)
    return content


def save_to_dir(root, img_dir, img_list):
    file_dir = os.path.join(root, img_dir[0], img_dir[1], img_dir[-1] + '(' + img_list[0] + ')')
    log.info(file_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    for item in img_list[1]:
        filename = str(int(time.time())) + '.jpg'
        log.info(filename)
        write_file(os.path.join(file_dir, filename), item)


def write_file(file_name, img_url):
    image = request.urlopen(img_url)
    data = image.read()
    f = open(file_name, 'wb')
    f.write(data)
    f.close()


def analyse_url(url):
    url_dir = []
    url_info = re.search(r'/(\d\d\d\d)/(\d\d\d\d)/(\d+)\.html', url)
    url_dir.append(url_info.group(1))
    url_dir.append(url_info.group(2))
    url_dir.append(url_info.group(3))
    return url_dir


def analyse_every_page(url_title, list_page):
    item = []
    page = pq(list_page)
    list_href = page('.art li')
    for li in list_href:
        element = pq(li)
        item.append(url_title + element('a').attr('href'))
    log.info(item)
    return item


def analyse_total_page(page):
    all_page = []
    html = pq(page)
    page_num = html('#pages').text()
    result = re.search(r'\d/(\d+)', page_num)
    total = result.group(1)
    all_page.append('http://www.103av.com/html/tupian/toupai/index.html')
    for i in range(int(total) + 1):
        if i not in [0, 1]:
            all_page.append('http://www.103av.com/html/tupian/toupai/index_' + str(i) + '.html')
    return all_page


def get_picture(main_url, url, root):
    html = get_main_page(url)
    pages = analyse_total_page(html)
    for item in pages:
        item_page = get_main_page(item)
        html = analyse_every_page(main_url, item_page)
        for cell in html:
            content_page = get_main_page(cell)
            content = parser_content(content_page, '.art_box h2', '.artbody.imgbody')
            url_dir = analyse_url(cell)
            save_to_dir(root, url_dir, content)


if __name__ == '__main__':
    # main_url = 'http://www.103av.com/html/tupian/toupai/2016/1003/389108.html'
    main_url = 'http://www.103av.com/'
    url = 'http://www.103av.com/html/tupian/toupai/index.html'
    root = 'D:\\Temp\\crawler'

    get_picture(main_url, url, root)
