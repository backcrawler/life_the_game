"""
Life The Game

Dots are represented as tuples: (x, y) where x is an absciss and y is an ordinate.
Keep in mind that iteration often comes through i and j where i is a row num and j - column num.
"""


import random
import argparse
from typing import List, Dict, Tuple, Union, Any

# Default configuration
ROWS = 15
COLS = 15
PROB = 0.25

SHIFT = (-1, 0, 1)

# Cell repr
ALIVE = 'X'
DEAD = '.'

# Typings
FieldType = List[List[str]]
DotType = Tuple[int, int]
CellType = str  # Union[ALIVE, DEAD]

# Arg parsing
parser = argparse.ArgumentParser(description='Process config data')
parser.add_argument('--rows', type=int, help='Number of rows')
parser.add_argument('--cols', type=int, help='Number of columns')
parser.add_argument('--prob', type=float, help='Probability of population. Must be greater than 0 and less than 1.')
args = parser.parse_args()

rows_num = args.rows or ROWS
cols_num = args.cols or COLS
probability = args.prob or PROB


def count_neighbors(dot: DotType, field: FieldType) -> int:
    count = 0
    x, y = dot
    for x_shift in SHIFT:
        x0 = x + x_shift
        if x0 < 0 or x0 >= cols_num:
            continue

        for y_shift in SHIFT:
            y0 = y + y_shift
            if y0 < 0 or y0 >= rows_num:
                continue
            if y_shift == 0 and x_shift == 0:  # we dont check self
                continue

            neighbor = field[y0][x0]
            if neighbor == ALIVE:
                count += 1

    return count


def make_decision(dot: DotType, field: FieldType, count: int) -> CellType:
    if count <= 1 or count >= 4:
        return DEAD
    elif count == 3:
        return ALIVE
    elif count == 2:
        x, y = dot
        current = field[y][x]
        if current == ALIVE:
            return ALIVE
    return DEAD


def count_new_configuration(field: FieldType) -> FieldType:
    new_configuration = create_blank_field()
    for i in range(rows_num):
        for j in range(cols_num):
            dot = (j, i)
            result = count_neighbors(dot, field)
            new_configuration[i][j] = make_decision(dot, field, result)

    return new_configuration


def create_blank_field() -> FieldType:
    field = []
    for row in range(rows_num):
        temp = [DEAD for _ in range(cols_num)]
        field.append(temp)
    return field


def generate_random_field(prob=0.5) -> FieldType:
    if prob <= 0 or prob >= 1:
        raise ValueError(f'Incorrect probability value: {prob} for generation')
    field = create_blank_field()
    dots = [(j, i) for i in range(rows_num) for j in range(cols_num) if prob > random.random()]
    return fill_field(field, dots)


def fill_field(field: FieldType, dots: List[DotType]) -> FieldType:
    for dot in dots:
        j, i = dot
        if j < 0 or j >= cols_num:
            continue
        if i < 0 or i >= rows_num:
            continue
        field[i][j] = ALIVE

    return field


def print_field(field: FieldType) -> None:
    for row in field:
        print(' '.join(row))


def main() -> None:
    start_config = generate_random_field(probability)
    print_field(start_config)
    current_config = start_config
    for step in range(25):
        new_config = count_new_configuration(current_config)
        print('\n')
        print_field(new_config)
        current_config = new_config


if __name__ == '__main__':
    main()
