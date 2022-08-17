import unittest

import spider.utils as tool


class TestMethod(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_get_html(self):
        info = tool.Tool()
        print(info.get_html('https://www.test/'))


if __name__ == '__main__':
    unittest.main()
