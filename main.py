import pygame
import math

from pygame.transform import scale

import grid
from Cell import Cell

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDO(A)KI?")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)
x = 0
y = 0
x1 = 0
y1 = 0

dif = 500 / 9
flagPress1 = 0
flagPress2 = 0
flag1_started = False
flag2_started = False

grid = grid.create_grid()

# Load test fonts for future use
font1 = pygame.font.SysFont("verdana", 30)
font2 = pygame.font.SysFont("verdana", 10)
WHITE = 255, 255, 255
RED = 255, 0, 0
BLACK = 0, 0, 0


def get_cord_first_click(pos):
    global x
    global y
    x = pos[0] // dif
    y = pos[1] // dif
    # position
    print("DEBUG first press " + str(math.floor(x)), str(math.floor(y)))
    # values
    cell = grid[math.floor(x)][math.floor(y)]
    print(cell.value)

    return cell


def get_cord_second_click(pos):
    global x1
    global y1
    x1 = pos[0] // dif
    y1 = pos[1] // dif
    # position
    print("DEBUG 2 press " + str(math.floor(x1)), str(math.floor(y1)))
    # values
    cell = grid[math.floor(x1)][math.floor(y1)]
    print("DEBUG" + str(cell.value))

    return cell


# Highlight the cell selected
def highlight_cells():
    # draw red lines vert/hor to highlight the cell
    if (flag1_started):
        for i in range(2):
            pygame.draw.line(screen, RED, (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
            pygame.draw.line(screen, RED, ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)
            if (flag2_started):
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
                text1 = font1.render(str(cell.value), 1, (BLACK))
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


def is_near(initial_cell, landing_cell):
    # bishop like move
    dx = abs(initial_cell.x_coord - landing_cell.x_coord)
    dy = abs(initial_cell.y_coord - landing_cell.y_coord)
    if abs(initial_cell.x_coord - landing_cell.x_coord == 1) and (initial_cell.y_coord - landing_cell.y_coord == 0):
        return True
    elif abs(landing_cell.x_coord - initial_cell.x_coord == 1) and (initial_cell.y_coord - landing_cell.y_coord == 0):
        return True
    elif abs(initial_cell.y_coord - landing_cell.y_coord == 1) and (initial_cell.x_coord - landing_cell.x_coord == 0):
        return True
    elif abs(landing_cell.y_coord - initial_cell.y_coord == 1) and (initial_cell.x_coord - landing_cell.x_coord == 0):
        return True
    elif (dx == dy) and (dx > 0):

        return True
    else:
        print("not legal move")
        return False


run = True

# The loop that keeps the window running
while run:
    # pos1 = 0, 0
    # pos2 = 0, 0
    # White color background
    screen.fill(WHITE)

    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            # setPressed
            if flagPress1 == 0:
                flagPress1 = 1
                flag1_started = True

                first_cell = get_cord_first_click(pos)
                # first_cell.is_selected = True
                grid[first_cell.x_coord][first_cell.y_coord] = first_cell

            elif flagPress1 == 1 and flagPress2 == 0:
                flagPress2 = 1

                scd_cell = get_cord_second_click(pos)
                flag2_started = True
                # cell.is_selected = True
                grid[scd_cell.x_coord][scd_cell.y_coord] = scd_cell

                print("DEBUG reset " + str(first_cell.value) + str(scd_cell.value))
                # bug 3rd click
                flagPress1 = 0
                flagPress2 = 0
                if (first_cell.value == scd_cell.value) or (first_cell.value + scd_cell.value == 10):
                    # check if valid
                    print("DEBUG SAME")
                    if (is_near(first_cell, scd_cell)):
                        first_cell.value = 0
                        scd_cell.value = 0
                    # disable cells

    draw()
    instruction()
    highlight_cells()
    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
