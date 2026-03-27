#%%
import asyncio
import numpy as np
import pygame

# 
BOARD_SIZE = 8
TILE_SIZE = 80
SCREEN_SIZE = BOARD_SIZE * TILE_SIZE
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 
directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def initialize_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    board[3][3], board[4][4] = 1, 1
    board[3][4], board[4][3] = -1, -1
    return board

def is_valid_move(board, row, col, player):
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return False

    if board[row][col] != 0:
        return False

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == -player:
            r += dr
            c += dc
            flipped = True

        if flipped and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            return True

    return False

def get_valid_moves(board, player):
    return [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if is_valid_move(board, r, c, player)
    ]

def apply_move(board, row, col, player):
    board[row][col] = player

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flipped_positions = []

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == -player:
            flipped_positions.append((r, c))
            r += dr
            c += dc

        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            for fr, fc in flipped_positions:
                board[fr][fc] = player

def draw_board(screen, board):
    screen.fill(GREEN)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            pygame.draw.rect(
                screen, BLACK,
                (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                1
            )

            center = (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2)
            radius = TILE_SIZE // 2 - 5

            if board[r][c] == 1:
                pygame.draw.circle(screen, WHITE, center, radius)
            elif board[r][c] == -1:
                pygame.draw.circle(screen, BLACK, center, radius)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Othello Game")
    clock = pygame.time.Clock()

    board = initialize_board()
    player = 1
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE

                if is_valid_move(board, row, col, player):
                    apply_move(board, row, col, player)
                    player *= -1

                    if not get_valid_moves(board, player):
                        player *= -1
                        if not get_valid_moves(board, player):
                            running = False

        draw_board(screen, board)
        pygame.display.flip()
        clock.tick(30)

        # Pygbag is inmortant to yield control to the event loop to keep the UI responsive
        await asyncio.sleep(0)

asyncio.run(main())