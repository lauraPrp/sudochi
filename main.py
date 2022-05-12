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
flagPress1 = 0
flagPress2 = 0

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

    for i in range(2):
        pygame.draw.line(screen, RED, (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, RED, ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)
        pygame.draw.line(screen, RED, (x1 * dif - 3, (y1 + i) * dif), (x1 * dif + dif + 3, (y1 + i) * dif), 7)
        pygame.draw.line(screen, RED, ((x1 + i) * dif, y1 * dif), ((x1 + i) * dif, y1 * dif + dif), 7)


def draw():
    # Draw the lines on the board
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]

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

                cell = get_cord_first_click(pos)
                #cell.is_selected = True
                grid[cell.x_coord][cell.y_coord] = cell
                pos1 = pos

            elif flagPress1 == 1 and flagPress2 == 0:
                flagPress2 = 1
                pos2 = pos
                cell = get_cord_second_click(pos)
                #cell.is_selected = True
                grid[cell.x_coord][cell.y_coord] = cell
            elif flagPress1 == 1 and flagPress2 == 1:
                # evaluate

                pos1 = pos2
                pos2 = pos
                cell1 = get_cord_first_click(pos1)
                cell2 = get_cord_second_click(pos)
                #cell1.is_selected = True
                #cell2.is_selected = True
                grid[cell1.x_coord][cell1.y_coord] = cell1
                grid[cell2.x_coord][cell2.y_coord] = cell2
                print("reset " + str(cell1.value) + str(cell2.value))
                flagPress1 = 0
                flagPress2 = 0
                if cell1.value == cell2.value:
                    # check if valid
                    print("SAME")
                    cell1.value = 0;
                    cell2.value = 0;

    draw()
    instruction()
    highlight_cell()
    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
