import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the chess board
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = WIDTH // 8

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Create a 2D list to represent the chessboard
chessboard = [['' for _ in range(8)] for _ in range(8)]

def check_win(board):
    # A player wins if they have 4 in a row

    # Check horizontal spaces
    for y in range(len(board)):
        for x in range(len(board[y]) - 4):
            if (
                board[y][x]
                == board[y][x + 1]
                == board[y][x + 2]
                == board[y][x + 3]
                == board[y][x + 4]
                != ""
            ):
                # Game over
                return True

    # Check vertical spaces
    for x in range(len(board[0])):
        for y in range(len(board) - 4):
            if (
                board[y][x]
                == board[y + 1][x]
                == board[y + 2][x]
                == board[y + 3][x]
                == board[y + 4][x]
                != ""
            ):
                # Game over
                return True

    # Check / diagonal spaces
    for x in range(len(board[0]) - 4):
        for y in range(4, len(board)):
            if (
                board[y][x]
                == board[y - 1][x + 1]
                == board[y - 2][x + 2]
                == board[y - 3][x + 3]
                == board[y - 4][x + 4]
                != ""
            ):
                # Game over
                return True

    # Check \ diagonal spaces
    for x in range(len(board[0]) - 4):
        for y in range(len(board) - 4):
            if (
                board[y][x]
                == board[y + 1][x + 1]
                == board[y + 2][x + 2]
                == board[y + 3][x + 3]
                == board[y + 4][x + 4]
                != ""
            ):
                # Game over
                return True

    return False

# Fill the background with a light gray color
screen.fill(GRAY)

# Draw the squares of the chess board
for row in range(8):
    for col in range(8):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        color = WHITE if (row + col) % 2 == 0 else BLACK
        pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

# Update the display
pygame.display.flip()

# Keep track of the current player
current_player = 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse cursor
            pos = pygame.mouse.get_pos()
            # Convert the position into an index
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE

            # Check if the clicked square is empty and in the first or last column or there is a piece in the adjacent square
            if chessboard[row][col] == '' and ((col == 0 or col == 7) or (chessboard[row][col - 1] != '' or chessboard[row][col + 1] != '')):
                if current_player == 1:
                    # Draw a red circle for player 1
                    pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2)
                    chessboard[row][col] = 'Player 1'
                    current_player = 2
                    #check if player 1 has won
                    if check_win(chessboard):
                        print('Player 1 wins!')
                        # Display message in the middle of the screen
                        font = pygame.font.Font(None, 36)
                        text = font.render('Player 1 wins!', True, RED)
                        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        #give the text a background
                        pygame.draw.rect(screen, GRAY, text_rect)
                        screen.blit(text, text_rect)
                        pygame.display.flip()

                else:
                    # Draw a blue circle for player 2
                    pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2)
                    chessboard[row][col] = 'Player 2'
                    current_player = 1
                    #check if player 2 has won
                    if check_win(chessboard):
                        print('Player 2 wins!')
                        # Display message in the middle of the screen
                        font = pygame.font.Font(None, 36)
                        text = font.render('Player 1 wins!', True, RED)
                        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        #give the text a background
                        pygame.draw.rect(screen, GRAY, text_rect)
                        screen.blit(text, text_rect)
                        pygame.display.flip()

            # Update the display
            pygame.display.flip()

# Quit the game
pygame.quit()