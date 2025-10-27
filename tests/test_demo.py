#!/usr/bin/env python3

import unittest

class TestDemo(unittest.TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()