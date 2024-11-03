#create SudoKo game using pygame
#install pygame using: pip install pygame

import pygame
import sys
import random
import copy
#init pygame
pygame.init()

#screen settings
WIDTH,HEIGHT = 540,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SudoKu")

#colors and font
BG_COLOR = (255,255,255)
LINE_COLOR = (0,0,0)
HIGHLIGHT_COLOR = (200,200,255)
INCORRECT_COLOR = (255,100,100)
FONT = pygame.font.Font(None,40)
SMALL_FONT = pygame.font.Font(None,30)

#difficulty settings
difficulty_levels ={
    "easy":30, # 30 cells to keep
    "medium":20, 
    "hard":10
}

#cell and grid 
CELL_SIZE = WIDTH//9
SELECTED_CELL = None
incorrect_cell = set() # to track incorrect guesses
attempts = 5

# generate a full, valid sudoku board
def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def fill_board(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] ==0:
                    nums = list(range(1,10))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board,row,col,num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    fill_board(board)
    return board
#create a puzzle by removing cells based on difficulty
def create_puzzle(board,difficulty):
    puzzle = copy.deepcopy(board)
    cells_to_remove = 81 - difficulty_levels[difficulty]
    while cells_to_remove > 0:
        row, col = random.randint(0,8), random.randint(0,8)
        if puzzle[row][col] != 0 :
            puzzle[row][col] = 0
            cells_to_remove -= 1
    return puzzle

#draw the board grid
def draw_grid():
    SCREEN.fill(BG_COLOR)
    for row in range(9):
        for col in range(9):
            cell_x = col * CELL_SIZE
            cell_y = row * CELL_SIZE

            #Highlight selected cell 
            if SELECTED_CELL == (row, col):
                pygame.draw.rect(SCREEN,HIGHLIGHT_COLOR,(cell_x,cell_y,CELL_SIZE,CELL_SIZE))
            elif (row, col) in incorrect_cell:
                pygame.draw.rect(SCREEN,INCORRECT_COLOR,(cell_x,cell_y,CELL_SIZE,CELL_SIZE))
            
            #draw numbers
            if BOARD[row][col] != 0:
                text = FONT.render(str(BOARD[row][col]),True,LINE_COLOR)
                SCREEN.blit(text,(cell_x + CELL_SIZE // 3, cell_y + CELL_SIZE // 3))
    #Draw lines 
    for i in range(10):
        width = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN,LINE_COLOR,(0,i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)
        pygame.draw.line(SCREEN,LINE_COLOR,(i * CELL_SIZE,0), (i * CELL_SIZE,WIDTH), width)
    #display attempts
    attempt_text = SMALL_FONT.render(f"Attempts left: {attempts}", True,LINE_COLOR)
    SCREEN.blit(attempt_text,(10, HEIGHT-40))

#place a number in the selected cell 
def place_number(num):
    global attempts
    if SELECTED_CELL:
        row,col = SELECTED_CELL
        if SOLUTION[row][col] == num:
            BOARD[row][col] = num 
            if (row, col) in incorrect_cell:
                incorrect_cell.remove((row,col))
        else:
            incorrect_cell.add((row,col))
            attempts -= 1
            if attempts == 0:
                end_game("Game over - No attempts left.")

def end_game(message):
    global attempts
    while True:
        SCREEN.fill(BG_COLOR,(0,HEIGHT - 100, WIDTH, 100))
        text = FONT.render(message,True,(255,0,0))
        restart_text = SMALL_FONT.render("Press R to Restart Or Q to Quit",True,(0,0,0))
        SCREEN.blit(text,(WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        SCREEN.blit(restart_text,(WIDTH // 3 - restart_text.get_width() // 2, HEIGHT - 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    choose_difficulty()
                    attempts = 5
                    return 
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
#Difficulty selection function 
def choose_difficulty():
    global BOARD,SOLUTION, attempts
    while True:
        SCREEN.fill(BG_COLOR)
        easy_text = FONT.render("Press E for easy", True, LINE_COLOR)
        medium_text = FONT.render("Press M for medium", True,LINE_COLOR)
        hard_text = FONT.render("Press H for hard", True,LINE_COLOR)

        SCREEN.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT //2 - 80))
        SCREEN.blit(medium_text,(WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 - 30))
        SCREEN.blit(hard_text,( WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    SOLUTION = generate_full_board()
                    BOARD = create_puzzle(SOLUTION,"easy")
                    return
                elif event.key == pygame.K_m:
                    SOLUTION = generate_full_board()
                    BOARD = create_puzzle(SOLUTION,"medium")
                    return 
                if event.key == pygame.K_h:
                    SOLUTION = generate_full_board()
                    BOARD = create_puzzle(SOLUTION,"hard")
                    return
# Main game loop
choose_difficulty()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE
            SELECTED_CELL = (row, col)

        if event.type == pygame.KEYDOWN:
            if SELECTED_CELL and event.unicode.isdigit() and event.unicode != 0:
                place_number(int(event.unicode))
    draw_grid()
    pygame.display.flip()