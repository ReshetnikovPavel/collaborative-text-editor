import unittest

from src.utils import to_one_dimensional_index

class MyTestCase(unittest.TestCase):
    def test_1(self):
        text = [list("Hello world!")]
        index = to_one_dimensional_index((0, 5), text)
        self.assertEqual(index, 5)

    def test_2(self):
        big_text = [list("0123"), list("56789")]
        index = to_one_dimensional_index((1, 3), big_text)
        self.assertEqual(index, 8)

    def test_3(self):
        super_mega_big_text = [list("0123"), list("56789"), list("abcde"), list("fghij")]
        index = to_one_dimensional_index((3, 2), super_mega_big_text)
        self.assertEqual(index, 19)


if __name__ == '__main__':
    unittest.main()
