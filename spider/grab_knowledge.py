import os
import re
import time
from urllib.parse import urlparse  # py3
import requests
from pyquery import PyQuery as pq

html_template = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link type="text/css" rel="stylesheet" href="../Styles/itranswarp.css" />
    <title>{title}</title>
</head>

<body>
    {head}
    {content}
</body>

</html>
'''

start_url = 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000'
head_url = 'http://www.liaoxuefeng.com'

path = 'D:\\Project\\ebook\\gitTech\\'


user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

session = requests.session()

url_list = []

url_list_result = pq(session.get(start_url, headers=user_agent).content.decode('utf-8'))

for li in url_list_result('.uk-nav.uk-nav-side')[1]:
    link = pq(li)
    link_target = link('a').attr('href')
    url_list.append(head_url + link_target)

for url in url_list:
    print(url + '开始！')
    content = session.get(url, headers=user_agent).content.decode('utf-8')
    content_parse = pq(content)
    page_content = '<div class="x-wiki-content">' + content_parse('.x-wiki-content').html() + '</div>'
    title = content_parse('h4').html()
    head = '<h4>' + title + '</h4>'
    html = html_template.format(title=title, head=head, content=page_content)
    with open(path + title + '.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(url + '已完成！')



