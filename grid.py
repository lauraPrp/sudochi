from numpy import random
from Cell import Cell
import numpy as np



def create_grid():
    #grid = np.random.rand(9,9)
    grid = random.randint(9, size=(9, 9))
    '''for j in range(9):
        row = []
        for i in range(9):
            cell = Cell(j,i,random.randint(1, 9),"255,255,255", False)
            row.append(cell)
        grid.append(row)'''
    return grid



