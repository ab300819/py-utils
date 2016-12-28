import re
import urllib.error as error
from pyquery import PyQuery as pq
from urllib import request


def get_article(url):
    user_agent = {'User-Agent':
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/54.0.2840.71 Safari/537.36'}
    response = request.Request(url, headers=user_agent)
    try:
        result = request.urlopen(response, timeout=10)
        html = result.read().decode('utf-8', 'ignore')
    except error:
        print('请求网页失败\n错误代码：%d' % error.HTTPError)
    print(html)
    page = pq(html)
    content = page('.main.receptacle.post-view.ng-scope.full-screen-cover')
    filname = content('.multiline1.entry-title').text().replace('：', '-')
    content('.entry-title-image.ng-scope').remove()
    content('.placeholder').remove()
    content('ui-badge').remove()
    content='<>'
    save_file(filname, content)


def save_file(filename, content):
    templet = 'D:\\Project\\data\\zhihu\\templet.html'
    article = 'D:\\Project\\data\\zhihu\\' + filename + '.html'
    with open(templet, 'r', encoding='utf-8') as f:
        str = f.read()
    position = str.find('</div>')
    result = str[:position] + content + str[position:]
    with open(article, 'w', encoding='utf-8') as f:
        f.write(result)


if __name__ == '__main__':
    url = 'https://zhuanlan.zhihu.com/p/22160507'
    get_article(url)
