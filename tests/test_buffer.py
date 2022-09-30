import unittest
from src.editor import Buffer, Cursor


class TestBuffer(unittest.TestCase):
    def setUp(self) -> None:
        self.text = "\n1 line\n2 line\n3 line\n     \n5 line"
        self.split_text = self.text.split("\n")
        self.buffer = Buffer(self.text)
        # print(self.buffer[:])

    def test_indexator(self) -> None:
        for i, line in enumerate(self.buffer):
            with self.subTest(i=i):
                self.assertEqual(line, self.split_text[i])

    def test_len(self) -> None:
        self.assertEqual(len(self.buffer), len(self.split_text))

    def test_join(self) -> None:
        self.assertEqual("\n".join(self.buffer), self.text)

    def test_insert_in_the_beginning(self) -> None:
        self.buffer.insert(Cursor(0, 0), "0 line")
        self.assertEqual(self.buffer[0], "0 line")

    def test_insert_in_the_middle(self) -> None:
        self.buffer.insert(Cursor(2, 2), "inserted ")
        self.assertEqual(self.buffer[2], "2 inserted line")

    def test_insert_in_the_end(self) -> None:
        self.buffer.insert(Cursor(5, 6), " inserted")
        self.assertEqual(self.buffer[5], "5 line inserted")

    def test_delete_empty_line(self) -> None:
        self.buffer.delete(Cursor(0, 0))
        self.assertListEqual(self.buffer[:], self.split_text[1:])

    def test_delete_one_symbol(self) -> None:
        self.buffer.delete(Cursor(2, 1))
        self.assertEqual(self.buffer[2], "2line")

    def test_delete_two_symbols(self) -> None:
        self.buffer.delete(Cursor(2, 1), 2)
        self.assertEqual(self.buffer[2], "2ine")

    def test_delete_in_the_end(self) -> None:
        self.buffer.delete(Cursor(2, 6))
        expected_line = "2 line3 line"
        expected_list = self.split_text[:2] + [expected_line] + self.split_text[4:]
        self.assertEqual(self.buffer[2], expected_line)
        self.assertListEqual(self.buffer[:], expected_list)

    def test_split(self) -> None:
        self.buffer.split(Cursor(2, 2))
        expected_list = self.split_text[:2] + ["2 ", "line"] + self.split_text[3:]
        self.assertListEqual(self.buffer[:], expected_list)


if __name__ == "__main__":
    unittest.main()
