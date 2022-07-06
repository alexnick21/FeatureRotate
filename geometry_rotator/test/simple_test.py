import unittest

class TestFunction(unittest.TestCase):
    def test_true(self):
        self.assertEqual(1+1, 2)
if __name__ == '__main__':
    unittest.main()