import argparse


def parse_args(*arguments: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    for arg in arguments:
        parser.add_argument(arg)
    return parser.parse_args()
