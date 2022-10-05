class Buffer:
    def __init__(self, text: str = ""):
        self.lines = text.split('\n')

    def __getitem__(self, index: int) -> str:
        return self.lines[index]

    def __len__(self) -> int:
        return len(self.lines)

    @property
    def bottom(self) -> int:
        return len(self) - 1

    def insert(self, cursor_position: tuple[int, int], value: str) -> None:
        row, col = cursor_position
        current = self.lines.pop(row)
        new_line = current[:col] + value + current[col:]
        self.lines.insert(row, new_line)

    def delete(self, cursor_position: tuple[int, int], count: int = 1) -> None:
        row, col = cursor_position
        if (row, col) >= (self.bottom, len(self[row])):
            return
        curr_line = self.lines.pop(row)
        if col < len(self[row]):
            new_line = curr_line[:col] + curr_line[col + count:]
            if not new_line:
                return
            self.lines.insert(row, new_line)
        else:
            next_line = self.lines.pop(row)
            new_line = curr_line + next_line
            self.lines.insert(row, new_line)

    def split(self, cursor_position: tuple[int, int]) -> None:
        row, col = cursor_position
        curr_line = self.lines.pop(row)
        self.lines.insert(row, curr_line[:col])
        self.lines.insert(row + 1, curr_line[col:])

    def join(self, cursor_position: tuple[int, int]) -> None:
        row, col = cursor_position
        current = self.lines.pop(row)
        next_line = self.lines.pop(row)
        self.lines.insert(row, current + next_line)