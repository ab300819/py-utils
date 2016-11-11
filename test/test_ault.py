import unittest
from urllib import request
from grab_content import grab_adult as adult


class TestAdult(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.url = 'http://103av.com/html/article/jiqing/2016/1107/390969.html'
        user_agent = {'User-Agent':
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.71 Safari/537.36'}
        response = request.Request(self.url, headers=user_agent)
        content = request.urlopen(response, timeout=10)
        self.html = content.read().decode('utf-8', 'ignore')

    def test_get_book(self):
        test = adult.Spider(self.html)
        content = test.analyse_book(self.html)
        print(content)

    def test_get_all_page(self):
        test_1 = 'http://103av.com/html/article/jiqing/index.html'
        test_2 = 'http://103av.com/html/article/jiqing/2016/1102/390718.html'
        test_method = adult.Spider(self.html)
        page_1 = test_method.get_all_pages(test_1)
        print(page_1)
        page_2 = test_method.get_all_pages(test_2)
        print(page_2)

    def test_get_catalog(self):
        url = 'http://103av.com/'
        test = adult.Spider(url)
        html = test.get_page()
        print(test.get_catalog(html))

    def test_save_book(self):
        url = 'http://www.103av.com'
        test = adult.Spider(url)
        book_url = 'http://www.103av.com/html/article/jiqing/2016/1024/390110.html'
        test.write_book('D:\\Temp\\test.txt', book_url)

    def test_get_target_item(self):
        url = 'http://www.103av.com'
        test = adult.Spider(url)
        catalog = test.get_catalog(url)
        print(catalog)
        target_1 = '偷拍自拍'
        target_2 = ['偷拍自拍', '激情文学', '亚洲情色']
        result_1 = test.get_target_item(catalog, target_1)
        print(result_1)
        result_2 = test.get_target_item(catalog, target_2)
        print(result_2)

    def test_crete_dir(self):
        url = 'http://103av.com/html/article/jiqing/2016/1102/390718.html'
        test = adult.Spider(self.url)
        result = test.create_dir('d:\\Temp', url)
        print(result)

    def test_get_content_url(self):
        test_url = 'http://www.103av.com/html/article/jiqing/index.html'
        url = 'http://103av.com'
        test = adult.Spider(url)
        result = test.get_content_url(test_url)
        print(result)
