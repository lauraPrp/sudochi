
import pygame
import random
import math
import grid

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDOKI?")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)
x = 0
y = 0
dif = 500 / 9
val = 0

grid = grid.create_grid()

# Load test fonts for future use
font1 = pygame.font.SysFont("verdana", 30)
font2 = pygame.font.SysFont("verdana", 10)


def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif
    # position
    print(math.floor(x), math.floor(y))
    # values
    print(grid[math.floor(x)][math.floor(y)])


# Highlight the cell selected
def highlight_cell():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


def draw():
    # Draw the lines on the board
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                # pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 10, j * dif + 10))
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
    text1 = font2.render("MATCH ADIACENTS EQUALS NUMBERS AND THOSE WHOSE SUM IS 10", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))


run = True

# The loop thats keep the window running
while run:

    # White color background
    screen.fill((255, 255, 255))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
            # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        # Get the number to be inserted if key pressed

    draw()

    highlight_cell()
    instruction()

    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
