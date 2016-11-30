import unittest
import re


class TestMethod(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_analyse_every_page(self):
        str=''
        result = re.sub(r'\u3000', '', str)
        print(result)

    def test_re(self):
        content='<br />'
        print(re.search(r'<br.?>',content))

if __name__ == '__main__':
    unittest.main()
