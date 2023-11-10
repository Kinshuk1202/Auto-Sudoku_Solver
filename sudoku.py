import pygame
import sys

sudoku_board = [[0 for _ in range(9)] for _ in range(9)]

pygame.init()

WIDTH, HEIGHT = 600,700
GRID_SIZE = WIDTH // 9

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

solve_button = pygame.Rect(WIDTH//2-50, 650, 100, 40)
clear_button = pygame.Rect(WIDTH//2-50, 600, 100, 40)

def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            thickness = 2
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT-100), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)

def draw_numbers(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                text = font.render(str(board[row][col]), True, BLACK)
                text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
                screen.blit(text, text_rect)

def draw_buttons():
    pygame.draw.rect(screen, (0, 255, 0), solve_button)
    solve_text = small_font.render("Solve", True, BLACK)
    solve_rect = solve_text.get_rect(center=solve_button.center)
    screen.blit(solve_text, solve_rect)

    pygame.draw.rect(screen, (255, 0, 0), clear_button)
    clear_text = small_font.render("Clear", True, BLACK)
    clear_rect = clear_text.get_rect(center=clear_button.center)
    screen.blit(clear_text, clear_rect)

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def clear_board():
    for row in range(9):
        for col in range(9):
            sudoku_board[row][col] = 0

running = True
solved = False
selected_cell = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if solve_button.collidepoint(event.pos):
                if not solved:
                    solved = solve_sudoku(sudoku_board)
            elif clear_button.collidepoint(event.pos):
                clear_board()
                solved = False
            else:
                col = event.pos[0] // GRID_SIZE
                row = event.pos[1] // GRID_SIZE
                selected_cell = (row, col)

        if event.type == pygame.KEYDOWN and selected_cell:
            if event.key in range(48, 58):
                num = int(chr(event.key))
                sudoku_board[selected_cell[0]][selected_cell[1]] = num

    screen.fill(WHITE)
    draw_grid()
    draw_numbers(sudoku_board)
    draw_buttons()

    if selected_cell:
        pygame.draw.rect(screen, (0, 0, 255), (selected_cell[1] * GRID_SIZE, selected_cell[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
