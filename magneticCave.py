import copy
import math
from time import sleep
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Dimensions of the board
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = WIDTH // 8
ROW_COUNT =  8
COLOUMN_COUNT = 8 
WINDOW = 5

# Create 2D array to represent the board
gameBoard = [[0 for _ in range(8)] for _ in range(8)]


def check_win(board, piece):
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
                == piece
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
                == piece
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
                == piece
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
                == piece
            ):
                # Game over
                return True

    return False


def valid_moves(board):
    # This function will return a list of valid moves
    # A move is valid if the square is empty and it is in the first or last column or there is a piece in the adjacent square
    validMoves = []
    for row in range(8):
        for col in range(8):
            if (
                board[row][col] == 0
                and ((col == 0 or col == 7) or (board[row][col - 1] != 0 or board[row][col + 1] != 0))
            ):
                validMoves.append((row, col))
    return validMoves

def setup_board():
    # Draw the squares of the chess board
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def place_piece(row, col, player):
    # Place a piece on the board and update the display
    color = RED if player == 1 else BLUE
    pygame.draw.circle(
        screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2
    )
    gameBoard[row][col] = player

def update_board():
    # Update the display
    pygame.display.flip()

def print_board(board):
    # Print the board to the console
    for row in board:
        print(row)

def display_winner(player):
    # Display the winner in the middle of the screen
    font = pygame.font.Font(None, 36)
    color = RED if player == 1 else BLUE
    text = font.render(f"Player {player} wins!", True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    # Give the text a background
    pygame.draw.rect(screen, GRAY, text_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()


def position_score(board,current_player):
    score = 0
    piece = current_player + 1
    #we will give higer score to the pieces that are closer to the center
    
    #score for center row
    center_array1 = [int(board[3][0]), int(board[3][ROW_COUNT - 1])]
    center_array2 = [int(board[4][0]), int(board[4][ROW_COUNT - 1])]
   

    score = 2*center_array1.count(piece) + 2*center_array2.count(piece)
    score -= 2*center_array1.count(piece - 1) + 2*center_array2.count(piece - 1)

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r])]
        for c in range(COLOUMN_COUNT - 4):
            window = row_array[c:c+5]
            if window.count(piece) == 5:
                score += 100
            elif window.count(piece) == 4 and window.count(0) == 1:
                score += 15
            elif window.count(piece) == 3 and window.count(0) == 2:
                score += 10
            elif window.count(piece - 1) == 4 and window.count(0) == 1:
                score -= 95
            elif window.count(piece - 1) == 3 and window.count(0) == 2:
                score -= 13

    for c in range(COLOUMN_COUNT):
        col_array = []
        for r in range(ROW_COUNT):
            col_array.append(board[r][c])
        for r in range(ROW_COUNT - 4):
            #col_array is the coloumn in each row
            window = col_array[r:r+WINDOW]
            if window.count(piece) == 5:
                score += 100
            elif window.count(piece) == 4 and window.count(0) == 1:
                score += 15
            elif window.count(piece) == 3 and window.count(0) == 2:
                score += 10
            elif window.count(piece - 1) == 4 and window.count(0) == 1:
                score -= 95
            elif window.count(piece - 1) == 3 and window.count(0) == 2:
                score -= 13
    # now we will check for positive diagonal
    for r in range(ROW_COUNT - 4):
        for c in range(COLOUMN_COUNT - 4):
            window = [board[r+i][c+i] for i in range(5)]
            if window.count(piece) == 5:
               score += 100
            elif window.count(piece) == 4 and window.count(0) == 1:
                score += 15
            elif window.count(piece) == 3 and window.count(0) == 2:
                score += 10
            elif window.count(piece-1) == 4 and window.count(0) == 1:
                score -= 95
    #now we will check for negative diagonal
    for r in range(ROW_COUNT - 4):
        for c in range(COLOUMN_COUNT - 4):
            window = [board[r+4-i][c+i] for i in range(5)]
            if window.count(piece) == 5:
                score += 100
            elif window.count(piece) == 4 and window.count(0) == 1:
                score += 15
            elif window.count(piece) == 3 and window.count(0) == 2:
                score += 10
            elif window.count(piece-1) == 4 and window.count(0) == 1:
                score -= 95
    print(score)
    return score


def pick_best_move(board, current_player):
    max_score = -math.inf
    validMoves = valid_moves(board)
    best_move = random.choice(validMoves)
    for move in validMoves:
        row = move[0]
        col = move[1]
        temp_board = copy.deepcopy(board)
        temp_board[row][col] = (current_player + 1)
        score = position_score(temp_board,current_player)
        if score > max_score:
            max_score = score
            best_move = move
    return  best_move
def terminal_node(board):
    return check_win(board,1) or check_win(board, 2) or len(valid_moves(board)) == 0

#the superstar ! , the minimax algorithm

#the superstar ! , the minimax algorithm
def minimax(board, depth, alpha, beta, maximizingPlayer):
    validMoves = valid_moves(board)
    is_terminal = terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, 2):
                return (None, 100000000000000) # computer wins
            elif check_win(board, 1):
                return (None, -10000000000000) #player wins
            else:
                return (None, 0) #game is over, draw
        else: #depth is zero
            return (None, position_score(board,1))
    if maximizingPlayer:
        value = -math.inf
        move = random.choice(validMoves)
        for m in validMoves:
            row = m[0]
            col = m[1]
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 2
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                move = m
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return move, value
    else: #minimizing player
        value = math.inf
        move = random.choice(validMoves)
        for m in validMoves:
            row = m[0]
            col = m[1]
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 1
            new_score = minimax(temp_board, depth - 1,  alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                move = m
            beta = min(beta, value)
            if alpha >= beta:
                break
        return move, value
       

while True:
    print("Welcome to Magnetic Cave!")
    print("1. Player vs Player")
    print("2. Player vs Computer")
    print("3. Computer vs Player")
    print("4. Exit")
    gameMode = int(input("Enter the game mode: "))
    if gameMode == 1 or gameMode == 2 or gameMode == 3:
        break
    elif gameMode == 4:
        exit()
    else:
        print("#" * 50)
        print("Invalid input. Please try again.")
        print("#" * 50)
current_player = 0

if gameMode == 3: current_player = 1
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magnetic Cave")
setup_board()
update_board()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Get the position of the mouse cursor
            pos = pygame.mouse.get_pos()
            # Convert the position into an index
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE

            # Check if the clicked square is a valid move
            if (row, col) in valid_moves(gameBoard):
                place_piece(row, col, current_player + 1)

                if check_win(gameBoard, current_player + 1):
                    display_winner(current_player + 1)
                    game_over = True

                current_player = (current_player + 1) % 2

                update_board()

    if current_player == 1 and (gameMode == 2 or gameMode == 3) and not game_over:
        validMoves = valid_moves(gameBoard)
        print(validMoves)
        move, score = minimax(gameBoard, 2, -math.inf, math.inf, True)
        #move = pick_best_move(gameBoard, current_player)
        print(move)
        print(score)
        place_piece(move[0], move[1], (current_player + 1))
        if check_win(gameBoard, current_player + 1):
            display_winner(current_player + 1)
            game_over = True
        current_player = (current_player + 1) % 2
        update_board()

# Quit the game
pygame.quit()
