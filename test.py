import unittest
import storage_data


class TestMethod(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_research(self):
        connect = storage_data.connect('localhost', 27017, 'test', 'demo')
        data = {"name": "lucy", "sex": "female", "job": "nurse"}
        connect.insert(data)


if __name__ == '__main__':
    unittest.main()
