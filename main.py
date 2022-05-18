import queue
import sys

import pygame
import math

import grid

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

score_points = 0


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
    score_text = font1.render(str(score_points), 1, RED)
    screen.blit(text1, (20, 520))
    screen.blit(score_text, (250, 560))
    # add score / hint


def diagonal(x_frst, y_frst, x_scnd, y_scnd):
    diag = []

    if abs(x_frst - x_scnd) != abs(y_frst - y_scnd):
        print("ERROR this is not a diagonal")
        flag1_started = False
        flag2_started = False
        diag.append("X")

    else:
        print("DEBUG CHECK DIAGONALSSSSS")
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


def hor_vert(x_coord, y_coord, x_coord1, y_coord1):
    print(" DEBUG CHECK HORVERT INSDE")
    horvert = []
    # check horizontal values in a gap
    if x_coord == x_coord1 and y_coord != y_coord1:
        print(" DEBUG CHECK VERT gap same x ")
        for i in range(1, abs(y_coord - y_coord1), 1):
            if y_coord < y_coord1:
                cell = grid[x_coord][y_coord + i]
                print("-----------------------------")
                print(cell.value)
                print("-----------------------------")
            elif y_coord > y_coord1:
                cell = grid[x_coord][y_coord - i]
                print("-----------------------------")
                print(cell.value)
                print("-----------------------------")
            else:
                cell.value = 0

            if cell.value != 0:
                horvert.append(cell.value)
        # check vertical values in a gap
        print(" DEBUG CHECK HOR x gap same y")
    elif x_coord != x_coord1 and y_coord == y_coord1:
        # check y gap
        for i in range(1, abs(x_coord - x_coord1), 1):
            if x_coord < x_coord1:
                cell = grid[x_coord + 1][y_coord]
                print("-----------------------------")
                print(cell.value)
                print("-----------------------------")
            elif x_coord > x_coord1:
                cell = grid[x_coord - 1][y_coord]
                print("-----------------------------")
                print(cell.value)
                print("-----------------------------")

            else:
                cell.value = 0

            if cell.value != 0:
                horvert.append(cell.value)

    return horvert


def is_valid(cell_1, cell_2):
    valid = False
    print("DEBUG checks proximity initial_cell" + str(cell_1.x_coord) + " " + str(cell_1.y_coord))
    print("DEBUG checks proximity landing_cell" + str(cell_2.x_coord) + " " + str(cell_2.y_coord))
    # checks proximity
    if abs(cell_1.x_coord - cell_2.x_coord) == 1 and abs(cell_1.y_coord - cell_2.y_coord) == 1:
        print(" DEBUG diagonal proximity")
        valid = True
    elif cell_1.y_coord - cell_2.y_coord == 0:
        print(" DEBUG proximity same y " + str(cell_1.y_coord) + str(cell_2.y_coord) + " XXX " + str(
            cell_1.x_coord) + str(cell_2.x_coord))
        if abs(cell_1.x_coord - cell_2.x_coord) == 1:
            print(" DEBUG proximity value x " + str(cell_1.x_coord) + str(cell_2.x_coord))
            valid = True
        elif len(hor_vert(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord)) == 0:

            valid = True
    elif cell_1.x_coord - cell_2.x_coord == 0:
        print(" DEBUG proximity same x " + str(cell_1.x_coord) + str(cell_2.x_coord))
        if abs(cell_1.y_coord - cell_2.y_coord) == 1:
            print(" DEBUG proximity value y " + str(cell_1.y_coord) + str(cell_2.y_coord))
            valid = True
        elif len(hor_vert(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord)) == 0:
            valid = True

    else:
        print(" DEBUG far from each other")
        # checks cells far from each other having just empty cells in between
        if len(diagonal(cell_1.x_coord, cell_1.y_coord, cell_2.x_coord, cell_2.y_coord)) == 0:
            print(" DEBUG CHECK DIAGONAL")
            valid = True

    return valid


''' 
TBD: calculate score 
- same numbers score 5
- 10 sums score 10
sequential scoring has a bonus?
hints have a malus? 
'''


def score(cell1, cell2):
    global score_points
    score_points = 0
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
                    grid[first_cell.x_coord][first_cell.y_coord] = first_cell

                    flag1_started = True

                else:
                    if clickQueue.qsize() == 1:  # first number selected

                        scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                        clickQueue.put(scd_cell)
                        grid[first_cell.x_coord][first_cell.y_coord] = first_cell
                        grid[scd_cell.x_coord][scd_cell.y_coord] = scd_cell
                        flag2_started = True

                    elif clickQueue.qsize() > 1:  # second number selected

                        clickQueue.get()  # fifo click
                        first_cell = get_cord_first_click(scd_cell.x_coord,
                                                          scd_cell.y_coord)  # second click becomes first
                        scd_cell = get_cord_second_click(math.floor(pos[0] // dif), math.floor(pos[1] // dif))
                        clickQueue.put(scd_cell)  # adds last click

                        flag1_started = True
                        flag2_started = True

                    if score(first_cell, scd_cell) and is_valid(first_cell, scd_cell):
                        print("SCORE")

                        first_cell.value = 0
                        scd_cell.value = 0
                        flagPress1 = 1
                        flagPress2 = 0

                    else:
                        print("NO SCORE")
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
