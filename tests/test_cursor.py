import unittest
from src.editor import Buffer, Cursor


class TestCursor(unittest.TestCase):
    def setUp(self) -> None:
        self.cursor = Cursor(0, 0)
        self.text = "\n1 line\n2 line\n3 line\n     \n5 line"
        self.buffer = Buffer(self.text)

    def test_position_property(self) -> None:
        self.assertTupleEqual(self.cursor.position, (0, 0))
        self.assertTupleEqual(Cursor(1, 5).position, (1, 5))
        self.assertTupleEqual(Cursor(7, 9).position, (7, 9))

    def test_row_property(self) -> None:
        self.assertEqual(self.cursor.row, 0)
        self.assertEqual(Cursor(1, 5).row, 1)
        self.assertEqual(Cursor(7, 9).row, 7)

    def test_col_property(self) -> None:
        self.assertEqual(self.cursor.col, 0)
        self.assertEqual(Cursor(1, 5).col, 5)
        self.assertEqual(Cursor(7, 9).col, 9)

    def test_up_at_beginning_buffer(self) -> None:
        self.cursor.up(self.buffer)
        self.assertTupleEqual(self.cursor.position, (0, 0))

    def test_up(self) -> None:
        cursor = Cursor(2, 0)

        cursor.up(self.buffer)
        self.assertTupleEqual(cursor.position, (1, 0))

        cursor.up(self.buffer)
        self.assertTupleEqual(cursor.position, (0, 0))

    def test_down_at_end_buffer(self) -> None:
        cursor = Cursor(5, 0)

        cursor.down(self.buffer)
        self.assertTupleEqual(cursor.position, (5, 0))

    def test_down(self) -> None:
        cursor = Cursor(2, 0)

        cursor.down(self.buffer)
        self.assertTupleEqual(cursor.position, (3, 0))

        cursor.down(self.buffer)
        self.assertTupleEqual(cursor.position, (4, 0))

    def test_left_at_beginning_buffer(self) -> None:
        self.cursor.left(self.buffer)
        self.assertTupleEqual(self.cursor.position, (0, 0))

    def test_left_at_beginning_line(self) -> None:
        cursor = Cursor(2, 0)
        cursor.left(self.buffer)
        self.assertTupleEqual(cursor.position, (1, len(self.buffer[1])))

    def test_left(self) -> None:
        cursor = Cursor(2, 5)

        cursor.left(self.buffer)
        self.assertTupleEqual(cursor.position, (2, 4))

        cursor.left(self.buffer)
        self.assertTupleEqual(cursor.position, (2, 3))

    def test_right_at_end_buffer(self) -> None:
        pos = (self.buffer.bottom, len(self.buffer[5]))
        cursor = Cursor(*pos)
        cursor.right(self.buffer)
        self.assertTupleEqual(cursor.position, pos)

    def test_right_at_end_line(self) -> None:
        cursor = Cursor(2, len(self.buffer[2]))
        cursor.right(self.buffer)
        self.assertTupleEqual(cursor.position, (3, 0))

    def test_right(self) -> None:
        cursor = Cursor(2, 0)

        cursor.right(self.buffer)
        self.assertTupleEqual(cursor.position, (2, 1))

        cursor.right(self.buffer)
        self.assertTupleEqual(cursor.position, (2, 2))


if __name__ == "__main__":
    unittest.main()
