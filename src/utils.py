import argparse
from typing import List


def parse_args(*arguments: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    for arg in arguments:
        parser.add_argument(arg)
    return parser.parse_args()


def to_one_dimensional_index(index: tuple[int, int], lines: List[List]) -> int:
    symbol_count = 0
    for row in range(index[0]):
        symbol_count += len(lines[row]) + 1
    symbol_count += index[1]
    return symbol_count


def to_string_list(chr_list: List[chr]) -> List[str]:
    str = "".join(chr_list)
    return str.split("\n")
