import queue
import sys
import traceback
from random import randint

import pygame
import math

import grid
from Cell import Cell

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDO(A)KI?")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)


dif = 500 / 9
flag1_started = False
flag2_started = False

grid = grid.create_grid()
# Load test fonts for future use
font1 = pygame.font.SysFont("verdana", 30)
font2 = pygame.font.SysFont("verdana", 10)
WHITE = 255, 255, 255
RED = 255, 0, 0
BLACK = 0, 0, 0


def get_cord_first_click(xx, yy):
    global x, y
    x = xx
    y = yy
    # position

    # values
    cell = grid[x][y]
    print(cell.value)

    return cell


def get_cord_second_click(xx1, yy1):
    global x1, y1
    x1 = xx1
    y1 = yy1
    # values
    cell = grid[x1][y1]
    print("DEBUG" + str(cell.value))

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
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]
            if cell.value == 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, WHITE, (i * dif, j * dif, dif + 1, dif + 1))

            else:
                pygame.draw.rect(screen, WHITE, (i * dif, j * dif, dif + 1, dif + 1))
                text1 = font1.render(str(cell.value), 1, BLACK)
                screen.blit(text1, (i * dif + 10, j * dif + 10))
                # Draw lines to form grid
    for i in range(10):
        thick = 1
        # horiz
        pygame.draw.line(screen, BLACK, (0, i * dif), (500, i * dif), thick)
        # vertical
        pygame.draw.line(screen, BLACK, (i * dif, 0), (i * dif, 500), thick)


# Display instruction for the game
def instruction():
    text1 = font2.render("(SHOULD) MATCH ADJACENTS EQUALS NUMBERS AND THOSE WHOSE SUM IS 10", 1, BLACK)
    screen.blit(text1, (20, 520))


def diagonal(x_frst, y_frst, x_scnd, y_scnd):
    diag = []

    if abs(x_frst - x_scnd) != abs(y_frst - y_scnd):
        print("ERROR this is not a diagonal")
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
                cell.value = 0

            if cell.value != 0:
                diag.append(cell.value)

    return diag


def is_valid(initial_cell, landing_cell):
    valid = False
    # checks proximity
    if initial_cell.y_coord - landing_cell.y_coord == 0:
        if abs(initial_cell.x_coord - landing_cell.x_coord) == 1:
            # print("DEBUG)
            # print(initial_cell.x_coord - landing_cell.x_coord)
            valid = True
    elif initial_cell.x_coord - landing_cell.x_coord == 0:
        if abs(initial_cell.y_coord - landing_cell.y_coord) == 1:
            # print("DEBUG)
            # print(initial_cell.y_coord - landing_cell.y_coord)
            valid = True
    else:
        # checks cells far from each other having just empty cells in between
        if len(diagonal(initial_cell.x_coord, initial_cell.y_coord, landing_cell.x_coord, landing_cell.y_coord)) == 0:
            valid = True
    return valid


def score(cell1, cell2):
    if cell1.value == cell2.value or cell1.value + cell2.value == 10:
        return True
    else:
        return False


clickQueue = queue.Queue()

run = True

# The loop that keeps the window running
while run:
    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            if pos[1] < 500:

                if clickQueue.qsize() == 0:

                    first_cell = get_cord_first_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                    clickQueue.put(first_cell)
                    grid[first_cell.x_coord][first_cell.y_coord] = first_cell

                    flag1_started = True
                elif clickQueue.qsize() == 1:
                    print("DUIIIIIIIIIIII ELEMENTO")
                    scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                    clickQueue.put(scd_cell)
                    grid[first_cell.x_coord][first_cell.y_coord] = first_cell
                    grid[scd_cell.x_coord][scd_cell.y_coord] = scd_cell
                    flag2_started = True

                elif clickQueue.qsize() > 1:
                    print("ELIMINA ELEMENTO")
                    clickQueue.get()
                    posCell = [scd_cell.x_coord, scd_cell.y_coord]

                    first_cell = get_cord_first_click(scd_cell.x_coord, scd_cell.y_coord)
                    scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                    clickQueue.put(scd_cell)

                    flag1_started = True
                    flag2_started = True

                    if score(first_cell, scd_cell) and is_valid(first_cell, scd_cell):
                        print("SCORE")
                        # check if close and valid
                        first_cell.value = 0
                        scd_cell.value = 0
                        flagPress1 = 1
                        flagPress2 = 0
                    '''else:
                        # reset clicks
                        first_cell = scd_cell
                        flagPress1 = 1
                        flagPress2 = 0
                        flag1_started = True
                        flag2_started = False
                        clickQueue.get()'''
                else:
                    print("dsdfsfdsdfsfsdfds")

            else:
                print("TBI SOON: HINT/SCORE")

    draw()
    instruction()
    highlight_cells()
    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
sys.exit()
