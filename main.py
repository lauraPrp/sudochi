import queue
import sys

import pygame
import math
import numpy as np

import grid
from Cell import Cell
from icecream import ic

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDO(A)KI?")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)


dif = 500 / 9
flag1_started = False
flag2_started = False

grid = list(grid.create_grid())
# Load test fonts for future use
font1 = pygame.font.SysFont("verdana", 30)
font2 = pygame.font.SysFont("verdana", 10)
WHITE = 255, 255, 255
RED = 255, 0, 0
BLACK = 0, 0, 0

score_points = 0


def get_cord_first_click(xx, yy):
    global x, y
    x = xx
    y = yy
    cell = Cell(xx, yy, grid[x][y], WHITE, True)

    return cell


def get_cord_second_click(xx1, yy1):
    global x1, y1
    x1 = xx1
    y1 = yy1
    # values
    cell = Cell(x1, y1, grid[x1][y1], WHITE, True)

    return cell


# Highlight the cell selected
def highlight_cells():
    # draw red lines vert/hor to highlight the cell

    for i in range(2):
        if flag1_started:
            pygame.draw.line(screen, RED, (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
            pygame.draw.line(screen, RED, ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)
        if flag2_started:
            pygame.draw.line(screen, RED, (x1 * dif - 3, (y1 + i) * dif), (x1 * dif + dif + 3, (y1 + i) * dif), 7)
            pygame.draw.line(screen, RED, ((x1 + i) * dif, y1 * dif), ((x1 + i) * dif, y1 * dif + dif), 7)


def draw():
    # Draw the lines on the board
    gridArr = list(grid)

    for i in range(9):
        for j in range(9):

            pygame.draw.rect(screen, WHITE, (i * dif, j * dif, dif + 1, dif + 1))

            if gridArr[i][j] != 0:
                text1 = font1.render(str(np.floor(gridArr[i][j]).astype(np.int32)), 1, BLACK)
                screen.blit(text1, (i * dif + 10, j * dif + 10))
                # Draw lines to form grid
    for i in range(10):
        thick = 1
        # horiz lines
        pygame.draw.line(screen, BLACK, (0, i * dif), (500, i * dif), thick)
        # vertical lines
        pygame.draw.line(screen, BLACK, (i * dif, 0), (i * dif, 500), thick)


# Display instruction for the game
def instruction():
    text1 = font2.render("(SHOULD) MATCH ADJACENTS EQUALS NUMBERS AND THOSE WHOSE SUM IS 10", 1, BLACK)
    score_text = font1.render(str(score_points), 1, RED)
    screen.blit(text1, (20, 520))
    screen.blit(score_text, (250, 560))
    # add score / hint


def diagonal(x_frst, y_frst, x_scnd, y_scnd):
    diag = []

    if abs(x_frst - x_scnd) != abs(y_frst - y_scnd):
        ic("this is not a diagonal")
        flag1_started = False
        flag2_started = False
        diag.append("X")

    else:
        for i in range(1, abs(y_frst - y_scnd), 1):
            if x_frst < x_scnd and y_frst < y_scnd:
                cell = grid[x_frst + i][y_frst + i]

            elif x_frst < x_scnd and y_frst > y_scnd:
                cell = grid[x_frst + i][y_frst - i]

            elif x_frst > x_scnd and y_frst < y_scnd:
                cell = grid[x_frst - i][y_frst + i]

            elif x_frst > x_scnd and y_frst > y_scnd:
                cell = grid[x_frst - i][y_frst - i]

            else:
                cell = 0

            if cell != 0:
                ic(cell)
                diag.append(cell)

    return diag


def hor_vert(x3, y3, x2, y2):
    ic()
    middleNumbers = []
    numpy_grid = np.array(grid)
    horizontal = x2 - x3
    vertical = y2 - y3

    count = max(abs(vertical + 1), abs(horizontal + 1))

    if horizontal == 0:
        for cc in np.round(np.linspace(y3, y2, count)).astype(np.int32):
            ic(numpy_grid[cc][y2])
            middleNumbers.append(numpy_grid[x2][cc])

    if vertical == 0:
        for cc in np.round(np.linspace(x3, x2, count)).astype(np.int32):
            ic(numpy_grid[y2][cc])
            middleNumbers.append(numpy_grid[cc][y2])

    if np.sum(middleNumbers).astype(int) == numpy_grid[x3, y3] + numpy_grid[x2, y2]:

        ic(numpy_grid[y3, x3])
        ic(numpy_grid[x2, y2])

        return 0
    else:
        ic(np.sum(middleNumbers).astype(int))
        return np.sum(middleNumbers).astype(int)


def is_valid(cell_1, cell_2):
    valid = False
    ic("DEBUG checks proximity initial_cell" + str(cell_1.x_coord) + " " + str(cell_1.y_coord))
    ic("DEBUG checks proximity landing_cell" + str(cell_2.x_coord) + " " + str(cell_2.y_coord))
    # Check they are 2 different cells
    if cell_1.x_coord == cell_2.x_coord and cell_1.y_coord == cell_2.y_coord:
        return False
    # checks proximity
    if abs(cell_1.x_coord - cell_2.x_coord) == 1 and abs(cell_1.y_coord - cell_2.y_coord) == 1:
        ic(" DEBUG diagonal proximity")
        valid = True
    elif cell_1.y_coord - cell_2.y_coord == 0:

        if abs(cell_1.x_coord - cell_2.x_coord) == 1:
            ic(" DEBUG proximity same y ")
            valid = True
        elif hor_vert(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord) < 1:
            ic(" DEBUG same line vert y " )
            valid = True
    elif cell_1.x_coord - cell_2.x_coord == 0:

        if abs(cell_1.y_coord - cell_2.y_coord) == 1:
            ic(" DEBUG proximity same x ")
            valid = True
        elif hor_vert(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord) < 1:
            ic(" DEBUG same line hor x " )
            valid = True

    else:

        # checks cells far from each other having just empty cells in between
        if len(diagonal(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord)) < 1:
            valid = True

    return valid


# shuffle
''' 
TBD: calculate score 
- same numbers score 5
- 10 sums score 10
sequential scoring has a bonus?
hints have a malus? 
'''


def score(cell1, cell2):
    global score_points
    if cell1.value == 0 or cell2.value == 0:
        ic("nice trail crocodile")
        return False
    else:
        if cell1.value == cell2.value:
            score_points = score_points + 5
            return True

        elif cell1.value + cell2.value == 10:
            score_points = score_points + 10
            return True
        else:
            return False


clickQueue = queue.Queue()  # keeps clicks state

run = True

# The loop that keeps the window running
while run:
    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            if pos[1] < 500:  # checks click is in the numbers board

                if clickQueue.qsize() == 0:  # start

                    first_cell = get_cord_first_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                    clickQueue.put(first_cell)
                    # grid[first_cell.x_coord][first_cell.y_coord] = first_cell

                    flag1_started = True

                else:
                    if clickQueue.qsize() == 1:  # first number selected

                        scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                        clickQueue.put(scd_cell)
                        # grid[first_cell.x_coord][first_cell.y_coord] = first_cell
                        # grid[scd_cell.x_coord][scd_cell.y_coord] = scd_cell
                        flag2_started = True

                    elif clickQueue.qsize() > 1:  # second number selected

                        clickQueue.get()  # fifo click
                        first_cell = get_cord_first_click(scd_cell.x_coord,
                                                          scd_cell.y_coord)  # second click becomes first
                        scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                        clickQueue.put(scd_cell)  # adds last click

                        flag1_started = True
                        flag2_started = True

                    if is_valid(first_cell, scd_cell) and score(first_cell, scd_cell):
                        ic("SCORE")

                        grid[first_cell.x_coord][first_cell.y_coord] = 0
                        grid[scd_cell.x_coord][scd_cell.y_coord] = 0

                        flagPress1 = 1
                        flagPress2 = 0

                    else:
                        ic("NO SCORE")
            else:
                ic("TBI SOON: HINT/SCORE")

    draw()
    instruction()
    highlight_cells()
    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
sys.exit()
