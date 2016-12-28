import unittest
import urllib.error as error
from urllib import parse
from urllib import request

from utils import http as cookies


class TestMethod(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.user_agent = {'User-Agent':
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/54.0.2840.99 '
                               'Safari/537.36'}

    def test_get_page(self):
        url = 'https://proxy-list.org/chinese/index.php?p=1'

        response = request.Request(url, headers=self.user_agent)
        try:
            content = request.urlopen(response, timeout=10)
            html = content.read().decode('utf-8', 'ignore')
        except error:
            print('请求网页失败\n错误代码：%d' % error.HTTPError.code)
        print(html)

    def test_cookie_login(self):
        url='https://zhuanlan.zhihu.com/p/24122984'
        postdata = parse.urlencode({
            'login': 'YmU2Y2E5ZGIyZWU0NDY3Y2JjYTMzN2ZmMjhiNTA1N2M=|1481108378|eb3c7843c0ff02d71ad07521829dd40f5dc4251c'
        }).encode()

        cookiefile = 'cookie.txt'
        cookie = cookies.MozillaCookieJar(cookiefile)
        handler=request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(handler)

        req=request.Request(url,postdata,self.user_agent)

        try:
            response=opener.open(req)
            print(response.ers().decode())
        except error.URLError as e:
            print(e.code,':',e.reason)




if __name__ == '__main__':
    unittest.main()
