#!/usr/bin/env python3

import os
import re
import time
import urllib.error as error

from pyquery import PyQuery as pq
from urllib import request


class Spider:
    def __init__(self, root_url):
        self.root_url = root_url

    def get_page(self, url=None):
        user_agent = {'User-Agent':
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.71 Safari/537.36'}
        if not url:
            response = request.Request(self.root_url, headers=user_agent)
        elif url and self.root_url == url:
            response = request.Request(self.root_url, headers=user_agent)
        else:
            response = request.Request(url, headers=user_agent)

        try:
            content = request.urlopen(response, timeout=10)
            html = content.read().decode('utf-8', 'ignore')
        except error:
            print('请求网页失败\n错误代码：%d' % error.HTTPError.code)
            html = None
        return html

    # 获取主页目录
    def get_catalog(self, root_url):
        catalog = []
        page = self.get_page(root_url)
        html = pq(page)
        content = [html('.navmenu.dy li'), html('.navmenu.tp li'), html('.navmenu.xs li')]
        for item in content:
            temp = {}
            for li in item:
                list = pq(li)
                key = list('a').attr('title')
                if key:
                    temp[key] = self.root_url + list('a').attr('href')
            catalog.append(temp)
        return catalog

    # 一个页面中所有目标内容的链接
    def get_content_url(self, url):
        result = {}
        html = self.get_page(url)
        page = pq(html)
        content = page('.art ul li')
        for li in content:
            item = pq(li)
            link = item('a')
            key = link.text().lstrip()
            if re.search(r'[!@#$%^&*(){}/\\+=\-<>?]', key):
                key = str(int(time.time()))
            result[key] = self.root_url + link.attr('href')
        return result

    # 获取每页电影url
    def get_movie_url(self, url):
        result = []
        html = self.get_page(url)
        page = pq(html)
        content = page('.mlist li')
        for li in content:
            temp = []
            item = pq(li)
            title = item('a').attr('title')
            temp.append(title)
            temp.append('http://107av.com' + item('a').attr('href'))
            result.append(temp)
        return result

    # 找出下标所指向的所有页面
    def get_all_pages(self, url, start=None, end=None):

        all_page = []
        head = re.search(r'(.*)\.html', url)
        page = self.get_page(url)
        html = pq(page)
        page_num = html('#pages').html()
        if re.search(r'index', url):
            if page_num:
                total = re.search(r'\d/(\d+)', page_num)
            else:
                total = None
                all_page.append(url)
            if total:
                if start and isinstance(start, int) and not end:
                    for i in range(start, int(total.group(1)) + 1):
                        if i == 1:
                            all_page.append(url)
                        all_page.append(head.group(1) + '_' + str(i) + '.html')
                elif start and end and isinstance(start, int) and isinstance(end, int):
                    for i in range(start, end + 1):
                        if i == 1:
                            all_page.append(url)
                        all_page.append(head.group(1) + '_' + str(i) + '.html')
                else:
                    all_page.append(url)
                    for i in range(2, int(total.group(1)) + 1):
                        all_page.append(head.group(1) + '_' + str(i) + '.html')
        else:
            all_page.append(url)
            if page_num:
                total = re.search(r'<b>\d</b>/<b>(\d+)</b>', page_num)
            else:
                total = None
            if total:
                for i in range(2, int(total.group(1)) + 1):
                    all_page.append(head.group(1) + '_' + str(i) + '.html')

        return all_page

    def get_target_item(self, all_url, target):

        result = {}
        if isinstance(target, list):
            for item in all_url:
                for key, value in item.items():
                    if key in target:
                        result[key] = value
            return result
        else:
            for item in all_url:
                for key, value in item.items():
                    if key == target:
                        return value

    def analyse_book(self, url):
        all_page = self.get_all_pages(url)
        result = []
        for item in all_page:
            page = self.get_page(item)
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
        html = self.get_page(url)
        page = pq(html)
        content = page(match)
        for item in content:
            p = pq(item)
            if p:
                src = p('img').attr('src')
                if src:
                    result.append('http:' + src)
        return result

    # 获取电影下载地址
    def analyse_movie(self, url):
        html = self.get_page(url)
        page = pq(html)
        link = page('.played2k textarea').text()
        return link

    def analyse_url(self, url):
        url_dir = []
        result = re.search(r'/(\d\d\d\d)/(\d\d\d\d)/(\d+)\.html', url)
        url_dir.append(result.group(1))
        url_dir.append(result.group(2))
        url_dir.append(result.group(3))
        return url_dir

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

    def link_to_book_name(self, root, name, url):
        url_path = self.analyse_url(url)
        file_name = url_path[-1] + '(' + name + ').txt'
        return os.path.join(root, url_path[0], url_path[1], file_name)


def grab_book(start, end):
    pass


def grab_movie(start, end):
    pass


def grab_picture(start, end):
    pass


if __name__ == '__main__':
    url = ''
    target = '文学'
    root = '/home/pi/Documents/grab_data/book'
    all_content = []
    link = []
    i = 1
    adult = Spider(url)
    catalog = adult.get_catalog(url)
    result = adult.get_target_item(catalog, target)
    all_page = adult.get_all_pages(result)
    for page in all_page:
        print('正在爬取第%d页\n正在解析：%s' % (i, page))
        i += 1
        for key, value in adult.get_content_url(page).items():
            print('正在获取内容：%s' % value)
            file_name = adult.link_to_book_name(root, key, value)
            adult.write_book(file_name, value)
