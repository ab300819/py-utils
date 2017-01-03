#!/usr/bin/env python3

import os
import re
import time
import spider.utils as tool

from datetime import datetime
from enum import Enum
from multiprocessing import Process, Lock
from urllib import request
from pymongo import MongoClient, errors
from pyquery import PyQuery as pq

'''
      ┏━┓       ┏━┓
    ┏━┛ ┻━━━━━━━┛ ┻━┓
    ┃               ┃
    ┃      ━━━      ┃
    ┃               ┃
    ┃    ┳━┛ ┗━┳    ┃
    ┃               ┃
    ┃               ┃
    ┃      ━┻━      ┃
    ┃               ┃
    ┗━━━┓      ┏━━━━┛
        ┃      ┃
        ┃      ┃
        ┃      ┃
        ┃      ┃
        ┃      ┗━━━━━━━━━━┓
        ┃                 ┃
        ┃                 ┣━━┓
        ┃                 ┏━━┛
        ┗━━━┓ ┳ ┏━━┓ ┳ ┏━━┛
            ┃ ┃ ┃  ┃ ┃ ┃
            ┃ ┫ ┫  ┃ ┫ ┫
            ┃ ┃ ┃  ┃ ┃ ┃
            ┗━┻━┛  ┗━┻━┛
Code is far away from bug with the animal protecting
           神兽保佑,代码无bug
'''

Status = Enum('Status', 'start processing complete')


class Adult:
    def __init__(self, root_url):
        self.root_url = root_url
        self.tool = tool.Tool()
        global Status

    # 获取主页目录
    def get_catalog(self, root_url):
        catalog = []
        page = self.tool.get_html(root_url)
        if not page:
            return None
        html = pq(page)
        content = [html('.navmenu.dy li'), html('.navmenu.tp li'), html('.navmenu.xs li')]
        for item in content:
            temp = {}
            for li in item:
                link = pq(li)
                key = link('a').attr('title')
                if key:
                    temp[key] = self.root_url + link('a').attr('href')
            catalog.append(temp)
        return catalog

    # 一个页面中所有目标内容的链接
    def get_content_url(self, url):
        result = {}
        html = self.tool.get_html(url)
        if not html:
            return None
        page = pq(html)
        content = page('.art ul li')
        for li in content:
            item = pq(li)
            link = item('a')
            key = link.text().lstrip()

            # 如果包含特殊符号以时间戳命名
            if re.search(r'[!@#$%^&*(){}/\\+=\-<>?]', key):
                key = str(int(time.time()))
            result[key] = self.root_url + link.attr('href')
        return result

    # 找出下标所指向的所有页面
    def get_all_pages(self, url):

        all_page = []
        head = re.search(r'(.*)\.html', url)
        page = self.tool.get_html(url)
        html = pq(page)
        page_num = html('#pages').html()
        if page_num:
            if re.search(r'index', url):
                total = re.search(r'\d/(\d+)', page_num)
            else:
                total = re.search(r'<b>\d</b>/<b>(\d+)</b>', page_num)
        else:
            total = None
        all_page.append(url)

        if total:
            for i in range(2, int(total.group(1)) + 1):
                all_page.append(head.group(1) + '_' + str(i) + '.html')

        return all_page

    # 获取目标link
    def get_target_item(self, all_url, target):
        result = {}
        for item in all_url:
            for key, value in item.items():
                if isinstance(target, list):
                    if key in target:
                        result[key] = value
                else:
                    if key in target:
                        return value

    # 获取每页电影url
    def get_movie_url(self, url):
        result = []
        html = self.tool.get_html(url)
        page = pq(html)
        content = page('.mlist li')
        for li in content:
            temp = []
            item = pq(li)
            title = item('a').attr('title')
            temp.append(title)
            temp.append(self.root_url + item('a').attr('href'))
            result.append(temp)
        return result

    # 获取电影下载地址
    def analyse_movie(self, url):
        html = self.tool.get_html(url)
        page = pq(html)
        link = page('.played2k textarea').text()
        return link

    def generate_book_name(self, root, name, url):
        result = re.search(r'/(\d\d\d\d)/(\d\d\d\d)/(\d+)\.html', url)
        file_name = result.group(3) + '(' + name + ').txt'
        return os.path.join(root, result.group(1), result.group(2), file_name)

    def analyse_book(self, url):
        all_page = self.get_all_pages(url)
        result = []
        for item in all_page:
            page = self.tool.get_html(item)
            html = pq(page)
            content = html('.artbody.imgbody p').html()
            if content:
                section = re.split(r'<br.*?>', content)
                result.extend(
                    list(map(lambda x: re.sub(r'[\u3000\t\n]|<a.*</a>|<script.*</script>', '', x.lstrip()), section)))
        return result

    # movie: '.endtext.vodimg p'
    # picture: '.artbody.imgbody p'
    def analyse_picture(self, url, match):
        result = []
        html = self.tool.get_html(url)
        page = pq(html)
        content = page(match)
        for item in content:
            p = pq(item)
            if p:
                src = p('img').attr('src')
                if src:
                    result.append('http:' + src)
        return result

    def write_image(self, image_name, image_url):
        image = request.urlopen(image_url)
        data = image.read()
        with open(image_name, 'wb') as f:
            f.write(data)

    def write_book(self, book_name, book_url):
        if os.path.exists(book_name):
            print('已经存在保存：%s' % os.path.split(book_name)[1])
            print('保存在：%s' % book_name)
            return
        else:
            book_content = self.analyse_book(book_url)
            self.crete_dir(book_name)
            print('正在保存：%s' % os.path.split(book_name)[1])
            print('保存在：%s' % book_name)
            with open(book_name, 'w+', encoding='utf-8') as f:
                for section in book_content:
                    if section:
                        f.write('  ' + section + '\n')

    def crete_dir(self, file_name):
        path = os.path.split(file_name)
        if not os.path.exists(path[0]):
            os.makedirs(path[0])

    ##########################################

    def insert(self):
        post = {
            # 资源标题
            'title': '',
            # 资源类型（小说，类型，图片）
            'type': '',
            # 资源主页
            'main_url': '',
            # 资源下载地址
            'source_url': '',
            # 样例地址
            'sample_url': '',
            # 资源保存路径
            'path': '',
            # 资源更新时间
            'update_time': '',
            # 资源爬取时间
            'grab_time': '',
            # 资源开始下载时间
            'down_start_time': '',
            # 资源下载结束时间
            'down_end_time': '',
            # 资源状态
            'statue': ''

        }
        self.adult_collection.insert(post)
        print('Insert Success!')

    def split_url(self, url=str):
        url_split = re.split(r'[:/]+', url)
        url_split.pop(0)
        url_split.pop(0)
        return '/'.join(url_split)


class GrabData(Process):
    def __init__(self, loop, lock):
        Process.__init__(self)
        self.loop = loop
        self.lock = lock

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            self.lock.acquire()
            print('Pid:' + str(self.pid) + 'Loop Count:' + str(count))
            self.lock.release()


class TaskQueue:
    def __init__(self, database, collection, timeout=10):
        self.client = MongoClient()
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.timeout = timeout
        global Status

    def __bool__(self):
        pass

    def push(self, data={}):
        try:
            self.collection.insert(data)
            print('数据插入成功！')
        except errors.DuplicateKeyError as e:
            print(str(e.code + ':' + e.details))

    def check(self):
        pass

    def complete(self):
        pass


class DownloadController:
    pass


if __name__ == '__main__':
    # url = ''
    # target = '文学'
    # root = '/home/pi/Documents/grab_data/book'
    # all_content = []
    # link = []
    # i = 1
    # adult = Adult(url)
    # catalog = adult.get_catalog(url)
    # result = adult.get_target_item(catalog, target)
    # all_page = adult.get_all_pages(result)
    # for page in all_page:
    #     print('正在爬取第%d页\n正在解析：%s' % (i, page))
    #     i += 1
    #     for key, value in adult.get_content_url(page).items():
    #         print('正在获取内容：%s' % value)
    #         file_name = adult.generate_book_name(root, key, value)
    #         adult.write_book(file_name, value)

    database = TaskQueue('sources', 'adult')
