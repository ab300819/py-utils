import unittest

from spider import grab_adult as adult


class TestAdult(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.url = 'http://1111av.co/'
        self.book = 'http://103.com/html/article/jiqing/2016/1010/389315.html'
        self.picture = ''
        self.movie = 'http://103.com/list/1.html'
        self.test = adult.Adult(self.url)

    def test_get_book(self):
        content = self.test.analyse_book(self.book)
        print('获取内容:%s' % content)
        for x in content:
            if x:
                print(x)

    def test_get_all_page(self):
        test_url_1 = 'http://1111av.co/html/tupian/toupai/index.html'
        test_url_2 = 'http://1111av.co/html/article/jiqing/2016/1102/390718.html'
        page_1 = self.test.get_all_pages(test_url_1)
        print(page_1)
        page_2 = self.test.get_all_pages(test_url_2)
        print(page_2)

    def test_get_catalog(self):
        print(self.test.get_catalog(self.url))

    def test_save_book(self):
        self.test.write_book('D:\\Temp\\test.txt', self.book)

    def test_get_target_item(self):
        catalog = self.test.get_catalog(self.url)
        # print(catalog)
        target_1 = '偷拍自拍'
        target_2 = ['亚洲情色', '偷拍自拍', '激情文学']
        result_1 = self.test.get_target_item(catalog, target_1)
        print(result_1)
        result_2 = self.test.get_target_item(catalog, target_2)
        print(result_2)

    def test_get_content_url(self):
        test_url = 'http://1111av.co/html/tupian/toupai/index.html'
        result = self.test.get_content_url(test_url)
        print(result)

    def test_special(self):
        url = 'http://www.103.com/html/article/jiqing/index_11.html'
        result = self.test.get_content_url(url)
        for key, value in result.items():
            print('%s:%s' % (key, value))

    def test_get_movie_url(self):
        result = self.test.get_movie_url(self.movie)
        for i in result:
            print(i)

    def test_analyse_movie(self):
        url = 'http://103.com/vod/10793.html'
        link = self.test.analyse_movie(url)
        print(link)

    def test_analyse_picture(self):
        url_1 = 'http://103.com/vod/10793.html'
        url_2 = 'http://103.com/html/tupian/toupai/2016/1028/390432.html'
        picture = self.test.analyse_picture(url_2, '.artbody.imgbody p')
        movie = self.test.analyse_picture(url_1, '.endtext.vodimg p')
        print(picture)
        print('-----------')
        print(movie)

    def test_write_picture(self):
        url = 'http://i1.1100lu.xyz/1100/vod/201611/07/vod/qmzqee2zbwv.jpg'
        file_name = 'D:\\Temp\\test.jpg'
        self.test.write_image(file_name, url)

    def test_split_url(self):
        url = self.test.split_url('http://1111av.co/html/article/jiqing/index.html')
        print(url)

