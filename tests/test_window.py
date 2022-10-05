import unittest
from src.editor import Buffer, Cursor, Window


class TestWindow(unittest.TestCase):
    def setUp(self) -> None:
        self.text = "\n1 line\n2 line\n3 line\n     \n5 line"
        self.buffer = Buffer(self.text)
        self.cursor = Cursor(0, 0)
        self.window = Window(10, 10)

    def test_num_rows_property(self) -> None:
        self.assertEqual(self.window.num_rows, 10)
        self.assertEqual(Window(100, 10).num_rows, 100)
        self.assertEqual(Window(0, 10).num_rows, 0)

    def test_num_cols_property(self) -> None:
        self.assertEqual(self.window.num_cols, 10)
        self.assertEqual(Window(10, 100).num_cols, 100)
        self.assertEqual(Window(10, 0).num_cols, 0)

    def test_bottom_property(self) -> None:
        self.assertEqual(self.window.bottom, 9)
        self.assertEqual(Window(100, 10, 10, 1).bottom, 109)
        self.assertEqual(Window(0, 10, 35, 1).bottom, 34)

    def test_up(self) -> None:
        self.window.up(self.cursor)



if __name__ == "__main__":
    unittest.main()
