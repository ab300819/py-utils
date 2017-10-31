#!/usr/bin/env python3

import os, re, html, time, json
import requests
import spider.ui as ui

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


class Adult:
    def __init__(self, root_path):
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.root_path = root_path
        self.root_url = None
        self.session = requests.session()

    def __get_root_url(self, url):
        root_url = re.split(r'/+', url)
        return root_url[0] + '//' + root_url[1] + '/'

    # 获取主页目录
    def get_catalog(self, root_url):
        catalog = []
        self.root_url = root_url
        response = self.session.get(root_url, headers=self.user_agent)
        html = pq(response.content)
        content = [html('.navmenu.dy li'), html('.navmenu.tp li'), html('.navmenu.xs li')]
        for item in content:
            temp = {}
            for li in item:
                link = pq(li)
                key = link('a').attr('title')
                if key:
                    temp[key] = root_url + link('a').attr('href')
            catalog.append(temp)
        return catalog

    # 一个页面中所有目标内容的链接
    def get_content_url(self, url):
        result = {}
        response = self.session.get(url, headers=self.user_agent)
        html = pq(response.content)
        content = html('.art ul li')
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
        response = self.session.get(url, headers=self.user_agent)
        html = pq(response.content)
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
        response = self.session.get(url, headers=self.user_agent)
        html = pq(response.content)
        content = html('.mlist li')
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
        response = self.session.get(url, headers=self.user_agent)
        html = pq(response.content)
        link = html('.played2k textarea').text()
        return link

    # 获取书籍
    def get_book(self, url):
        response = self.session.get(url, headers=self.user_agent)
        book_html = pq(response.content.decode('utf-8'))

        # 书籍标题
        book_title = re.split(r'[>\xa0 ]+', book_html('.art_box h2').remove('a').text())

        # 拼接文件名和书籍名称
        book_url_info = re.search(r'/(\d\d\d\d)/(\d\d\d\d)/(\d+)\.html', url)
        book_name = book_url_info.group(3) + '(' + book_title[-1] + ').txt'
        file_path = os.path.join(self.root_path, book_url_info.group(1), book_url_info.group(2))
        file_name = os.path.join(file_path, book_name)

        if os.path.exists(file_name):
            print('已保存:%s' % book_name)
        else:
            # 正文内容
            book_content = book_html('.artbody.imgbody p').html()
            # 总页码
            book_total = book_html('#pages').html()

            # 获取总页码并拼接url
            other_page = []
            book_url_head = re.search(r'(.*)\.html', url)
            total_num = re.search(r'<b>\d</b>/<b>(\d+)</b>', book_total)
            for num in range(2, int(total_num.group(1)) + 1):
                other_page.append(book_url_head.group(1) + '_' + str(num) + '.html')

            # 获取剩余页面内容并合并书籍内容
            for other in other_page:
                response = self.session.get(other, headers=self.user_agent)
                content = pq(response.content.decode('utf-8'))
                book_content += content('.artbody.imgbody p').html()
            book = re.sub(r'<br.*?>', '\n', book_content)

            if os.path.exists(file_path):
                print('正在保存:%s' % book_name)
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write('   ' + book.strip())
                print('已经保存:%s' % book_name)
            else:
                os.makedirs(file_path)
                print('正在保存:%s' % book_name)
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write('   ' + book.strip())
                print('已经保存:%s' % book_name)

    # 获取图片
    # movie: '.endtext.vodimg p'
    # picture: '.artbody.imgbody p'
    def get_picture(self, url):
        picture_list = []

        response = self.session.get(url, headers=self.user_agent)
        picture_html = pq(response.content.decode('utf-8'))

        # 图集标题
        picture_title = re.split(r'[>\xa0 ]+', picture_html('.art_box h2').remove('a').text())

        # 获取所有图片的
        picture_source = picture_html('.artbody.imgbody p')
        for item in picture_source:
            picture_element = pq(item)
            if picture_element.html():
                picture_list.append('http:' + picture_element('img').attr('src'))

        # 拼接图片文件路径和文件夹名称
        url_info = re.search(r'/(\d\d\d\d)/(\d\d\d\d)/(\d+)\.html', url)
        picture_path = os.path.join(self.root_path,
                                    url_info.group(1),
                                    url_info.group(2),
                                    url_info.group(3))

        if os.path.exists(picture_path):
            if self.__check_picture_file(picture_path, len(picture_list)):
                print(url_info.group(3) + '(' + picture_title[-1] + ')已保存！')
            else:
                self.__save_picture(picture_path, picture_title[-1], picture_list)
        else:
            os.makedirs(picture_path)
            self.__save_picture(picture_path, picture_title[-1], picture_list)

    def __check_picture_file(self, path, file_num):
        file_list = os.listdir(path)
        print(file_list)
        # for item in file_list:
        #     if not os.path.isfile(os.path.join(path, item)):
        #         file_list.remove(item)
        return len(file_list) == file_num

    def __save_picture(self, picture_path, picture_title, picture_list):
        for picture in picture_list:
            picture_name = str(int(time.time() * 1000)) + '(' + picture_title + ').jpg'
            file_name = os.path.join(picture_path, picture_name)
            picture_response = self.session.get(picture, headers=self.user_agent)
            with open(file_name, 'wb') as f:
                f.write(picture_response.content)
                print('已保存' + picture_name)



'''
post = {
        # 资源标题
        'title': '',
        # 资源类型（小说，类型，图片）
        'type': '',
        # 类别
        'belong': '',
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
'''


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
    picture_url = [
        'http://2222av.co/html/tupian/qingchun/2016/1031/390647.html',
        'http://2222av.co/html/tupian/qingchun/2016/1031/390637.html',
        'http://2222av.co/html/tupian/qingchun/2016/1031/390616.html'
    ]
    book_url = [
        'http://2222av.co/html/article/jiqing/2017/0224/394592.html',
        'http://2222av.co/html/article/jiqing/2017/0224/394597.html',
        'http://2222av.co/html/article/jiqing/2017/0224/394577.html'
    ]

    root_path = ui.get_choose_path()

    test = Adult(root_path)
    for i in picture_url:
        test.get_picture(i)
