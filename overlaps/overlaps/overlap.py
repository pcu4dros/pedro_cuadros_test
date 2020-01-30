import argparse
from typing import Tuple

NONE_TYPE_ERROR = "'NoneType' value is not allowed"
NOT_TUPLES_ERROR = "One of the input values is not a tuple of integers"


def has_overlaps(first_line: Tuple[int, int], second_line: Tuple[int, int]) -> bool:
    """Check if the lines given overlaps or not
        :param first_line: The first line to check <<Tuple[int, int]>>
        :param second_line: The second line to check <<Tuple[int, int]>>
        :return: True if the first_line overlaps with the second_line, False otherwise
    """
    # Fail first if an invalid argument is given
    if first_line is None or second_line is None:
        raise ValueError(NONE_TYPE_ERROR)
    if not isinstance(first_line, tuple) or not isinstance(second_line, tuple):
        raise ValueError(NOT_TUPLES_ERROR)

    first_case = less_or_equal(first_line, second_line)
    second_case = less_or_equal(second_line, first_line)

    # if first_case and second_case are valid return True otherwise return False
    return first_case and second_case


def less_or_equal(line_a, line_b):
    # validates if minimum value of the line_a is less or equal than the maximum value of the line_b
    first_case: bool = (min(line_a[0], line_a[1]) <= max(line_b[0], line_b[1]))
    return first_case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first', nargs='+', type=int)
    parser.add_argument('--second', nargs='+', type=int)
    args = parser.parse_args()
    first = tuple(args.first)
    second = tuple(args.second)
    return print(has_overlaps(first, second))


if __name__ == "__main__":
    main()
