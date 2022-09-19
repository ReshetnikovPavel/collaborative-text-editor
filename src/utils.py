from typing import List
import argparse


def parse_args(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    for arg in arguments:
        parser.add_argument(arg)
    return parser.parse_args()
