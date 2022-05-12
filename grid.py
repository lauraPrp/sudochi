import random
from Cell import Cell

grid = []


def create_grid():
    for j in range(9):
        row = []
        for i in range(9):
            cell = Cell(j,i,random.randint(1, 9),"255,255,255", False)
            row.append(cell)
        grid.append(row)
    return grid

'''
def create_grid():
    for j in range(9):
        row = []
        for i in range(9):
            n = random.randint(1, 9)
            row.append(n)
        grid.append(row)
    return grid
'''


