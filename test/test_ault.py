import unittest
from urllib import request
from grab_content import grab_adult as adult


class TestAdult(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.url = 'http://103av.com'
        self.book = 'http://www.103av.com/html/article/jiqing/2016/0901/385300.html'
        self.picture = ''
        self.movie = ''
        self.test = adult.Spider(self.url)

    def test_get_book(self):
        content = self.test.analyse_book(self.book)
        print(content)

    def test_get_all_page(self):
        test_url_1 = 'http://103av.com/html/article/jiqing/index.html'
        test_url_2 = 'http://103av.com/html/article/jiqing/2016/1102/390718.html'
        page_1 = self.test.get_all_pages(test_url_1, 9, 20)
        print(page_1)
        page_2 = self.test.get_all_pages(test_url_2)
        print(page_2)

    def test_get_catalog(self):
        html = self.test.get_page()
        print(self.test.get_catalog(html))

    def test_save_book(self):
        self.test.write_book('D:\\Temp\\test.txt', self.book)

    def test_get_target_item(self):
        catalog = self.test.get_catalog(self.url)
        print(catalog)
        target_1 = '偷拍自拍'
        target_2 = ['偷拍自拍', '激情文学', '亚洲情色']
        result_1 = self.test.get_target_item(catalog, target_1)
        print(result_1)
        result_2 = self.test.get_target_item(catalog, target_2)
        print(result_2)

    def test_get_content_url(self):
        test_url = 'http://www.103av.com/html/article/jiqing/index.html'
        result = self.test.get_content_url(test_url)
        print(result)
