import pygame
import random
import sys

# ---------- SETTINGS ----------
GRID_SIZE = 100
CELL_SIZE = 40
MARGIN = 50
BOARD_PIXELS = GRID_SIZE * CELL_SIZE

WIDTH = MARGIN * 3 + BOARD_PIXELS * 2
HEIGHT = MARGIN * 2 + BOARD_PIXELS + 80

WATER = (30, 90, 160)
GRID_LINE = (10, 40, 80)
SHIP_COLOR = (90, 90, 90)
HIT_COLOR = (200, 40, 40)
MISS_COLOR = (230, 230, 230)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (15, 25, 45)

SHIP_SIZES = [5, 4, 3, 3, 2]

EMPTY, SHIP, HIT, MISS = "empty", "ship", "hit", "miss"

# ---------- SETUP ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 32, bold=True)


def create_empty_board():
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def place_ships_randomly(board):
    for size in SHIP_SIZES:
        placed = False
        while not placed:
            horizontal = random.choice([True, False])
            if horizontal:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - size)
                cells = [(row, col + i) for i in range(size)]
            else:
                row = random.randint(0, GRID_SIZE - size)
                col = random.randint(0, GRID_SIZE - 1)
                cells = [(row + i, col) for i in range(size)]

            if all(board[r][c] == EMPTY for r, c in cells):
                for r, c in cells:
                    board[r][c] = SHIP
                placed = True


def all_ships_sunk(board):
    for row in board:
        if SHIP in row:
            return False
    return True


def draw_board(board, top_left_x, top_left_y, hide_ships):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = top_left_x + col * CELL_SIZE
            y = top_left_y + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            status = board[row][col]

            if status == SHIP and hide_ships:
                color = WATER
            elif status == SHIP:
                color = SHIP_COLOR
            elif status == HIT:
                color = HIT_COLOR
            elif status == MISS:
                color = MISS_COLOR
            else:
                color = WATER

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)


def get_cell_from_mouse(mouse_pos, top_left_x, top_left_y):
    mx, my = mouse_pos
    if (top_left_x <= mx < top_left_x + BOARD_PIXELS and
            top_left_y <= my < top_left_y + BOARD_PIXELS):
        col = (mx - top_left_x) // CELL_SIZE
        row = (my - top_left_y) // CELL_SIZE
        return int(row), int(col)
    return None


def ai_take_turn(board):
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if board[row][col] in (EMPTY, SHIP):
            if board[row][col] == SHIP:
                board[row][col] = HIT
            else:
                board[row][col] = MISS
            return


def draw_text(text, x, y, use_font=font, color=TEXT_COLOR):
    surface = use_font.render(text, True, color)
    screen.blit(surface, (x, y))


# ---------- GAME STATE ----------
player_board = create_empty_board()
enemy_board = create_empty_board()
place_ships_randomly(player_board)
place_ships_randomly(enemy_board)

player_left_x = MARGIN
enemy_left_x = MARGIN * 2 + BOARD_PIXELS
board_top_y = MARGIN + 40

player_turn = True
game_over = False
winner_text = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn:
            cell = get_cell_from_mouse(event.pos, enemy_left_x, board_top_y)
            if cell:
                row, col = cell
                if enemy_board[row][col] in (EMPTY, SHIP):
                    if enemy_board[row][col] == SHIP:
                        enemy_board[row][col] = HIT
                    else:
                        enemy_board[row][col] = MISS
                    player_turn = False

    if not game_over and not player_turn:
        ai_take_turn(player_board)
        player_turn = True

    if all_ships_sunk(enemy_board):
        game_over = True
        winner_text = "You win! All enemy ships sunk."
    elif all_ships_sunk(player_board):
        game_over = True
        winner_text = "AI wins! All your ships sunk."

    screen.fill(BG_COLOR)

    draw_text("Your Fleet", player_left_x, MARGIN, big_font)
    draw_text("Enemy Waters", enemy_left_x, MARGIN, big_font)

    draw_board(player_board, player_left_x, board_top_y, hide_ships=False)
    draw_board(enemy_board, enemy_left_x, board_top_y, hide_ships=True)

    status_y = board_top_y + BOARD_PIXELS + 20
    if game_over:
        draw_text(winner_text, MARGIN, status_y, big_font)
    else:
        turn_msg = "Your turn - click enemy waters" if player_turn else "AI is thinking..."
        draw_text(turn_msg, MARGIN, status_y, font)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()