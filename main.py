import pygame
import math
import grid
from Cell import Cell

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDOKI?")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)
x = 0
y = 0
x1 = 0
y1 = 0

dif = 500 / 9
val = 0
flagPress1 = 0
flagPress2 = 0

grid = grid.create_grid()

# Load test fonts for future use
font1 = pygame.font.SysFont("verdana", 30)
font2 = pygame.font.SysFont("verdana", 10)


def get_cord_first_click(pos):
    global x
    global y
    x = pos[0] // dif
    y = pos[1] // dif
    # position
    print("first press " + str(math.floor(x)), str(math.floor(y)))
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
    print("2 press " + str(math.floor(x1)), str(math.floor(y1)))
    # values
    cell = grid[math.floor(x1)][math.floor(y1)]
    print(cell.value)

    return cell


# Highlight the cell selected
def highlight_cell():
    # draw red lines vert/hor to highlight the cell
    if flagPress1 != 0 and flagPress2 != 0:
        for i in range(2):
            pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
            pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)
            pygame.draw.line(screen, (255, 0, 0), (x1 * dif - 3, (y1 + i) * dif), (x1 * dif + dif + 3, (y1 + i) * dif), 7)
            pygame.draw.line(screen, (255, 0, 0), ((x1 + i) * dif, y1 * dif), ((x1 + i) * dif, y1 * dif + dif), 7)


def draw():
    # Draw the lines on the board
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]
            if cell.value != 0:
                # Fill blue color in already numbered grid
                # pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(cell.value), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 10, j * dif + 10))
            elif cell.value == 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
                # Draw lines to form grid
    for i in range(10):
        thick = 1
        # horiz
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        # vertical
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)


# Fill value entered in cell
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# Display instruction for the game
def instruction():
    text1 = font2.render("(SHOULD) MATCH ADIACENTS EQUALS NUMBERS AND THOSE WHOSE SUM IS 10", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))


def check_pressed(flag1, flag2):
    if flag1 == 0 and flag2 == 0:
        return False
    else:
        return True


def reset_pressed():
    flagPress1 = 0
    flagPress2 = 0


run = True

# The loop that keeps the window running
while run:
    # pos1 = 0, 0
    # pos2 = 0, 0
    # White color background
    screen.fill((255, 255, 255))

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
                get_cord_first_click(pos)
                pos1 = pos
            elif flagPress1 == 1 and flagPress2 == 0:
                flagPress2 = 1
                pos2 = pos
                get_cord_second_click(pos)
            elif flagPress1 == 1 and flagPress2 == 1:
                # evaluate

                pos1 = pos2
                pos2 = pos
                cell1 = get_cord_first_click(pos1)
                cell2 = get_cord_second_click(pos)
                print("reset " + str(cell1.value) + str(cell2.value))
                flagPress1 = 0
                flagPress2 = 0
                if cell1.value == cell2.value:
                    print("SAME")

    draw()
    instruction()
    if check_pressed:
        highlight_cell()

    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
