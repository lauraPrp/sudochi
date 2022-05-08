import random

grid = []


def create_grid():
    for j in range(9):
        row = []
        for i in range(9):
            n = random.randint(1, 9)
            row.append(n)
        grid.append(row)
    return grid



