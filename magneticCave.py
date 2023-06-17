import pygame
import random
#this program will have 3 modes: player vs player, player vs computer, computer vs player

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# dimensions of the board
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = WIDTH // 8

#create 2d ARRAY to represent the board
gameBoard = [[0 for _ in range(8)] for _ in range(8)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("magnetic cave")
# Draw the squares of the chess board
for row in range(8):
    for col in range(8):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        color = WHITE if (row + col) % 2 == 0 else BLACK
        pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

# Update the display
pygame.display.flip()



