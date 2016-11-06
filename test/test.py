import unittest
from urllib import request
from grab_content import grab_pictures as grab


class TestMethod(unittest.TestCase):
    def setUp(self):
        super().setUp()
        url = 'http://www.103av.com/html/tupian/toupai/index.html'
        user_agent = {'User-Agent':
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        response = request.Request(url, headers=user_agent)

        content = request.urlopen(response, timeout=10)
        self.html = content.read().decode('utf-8', 'ignore')

    def test_analyse_every_page(self):
        self.main = 'http://www.103av.com/'
        url_list = grab.analyse_every_page(self.main, self.html)
        print(url_list)

    def test_total(self):
        self.total = grab.analyse_total_page(self.html)
        print(self.total)



if __name__ == '__main__':
    unittest.main()
