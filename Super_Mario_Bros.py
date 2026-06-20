import pygame
import sys
import random

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario - Enemies Left & Right")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 100, 255)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# Clock and font
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Ground
GROUND_Y = 350

# Mario
mario = pygame.Rect(100, GROUND_Y - 50, 40, 50)
velocity_y = 0
jump = False
gravity = 0.8

# Enemy list as dictionaries with direction
enemies = [{"rect": pygame.Rect(600, GROUND_Y - 40, 40, 40), "dir": -1}]
enemy_speed = 2

# Coins
coins = [pygame.Rect(random.randint(200, 750), GROUND_Y - 70, 20, 20) for _ in range(5)]

# Score, time, levels
score = 0
start_ticks = pygame.time.get_ticks()
game_over = False
level = 1

# Spawn helpers
def spawn_enemy():
    x = random.randint(500, 750)
    direction = random.choice([-1, 1])
    return {"rect": pygame.Rect(x, GROUND_Y - 40, 40, 40), "dir": direction}

def spawn_coin():
    x = random.randint(200, 750)
    return pygame.Rect(x, GROUND_Y - 70, 20, 20)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, 50))  # ground

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mario.x -= 5
        if keys[pygame.K_RIGHT]:
            mario.x += 5
        if keys[pygame.K_SPACE] and not jump:
            velocity_y = -15
            jump = True

        # Apply gravity
        velocity_y += gravity
        mario.y += velocity_y
        if mario.y >= GROUND_Y - mario.height:
            mario.y = GROUND_Y - mario.height
            velocity_y = 0
            jump = False

        # Move enemies
        for enemy in enemies[:]:
            rect = enemy["rect"]
            dir = enemy["dir"]

            rect.x += enemy_speed * dir

            # Reverse direction on screen bounds
            if rect.left <= 0 or rect.right >= WIDTH:
                enemy["dir"] *= -1

            # Collision: jump-on to defeat
            if mario.colliderect(rect):
                if velocity_y > 0 and mario.bottom - rect.top < 20:
                    enemies.remove(enemy)
                    score += 100
                    velocity_y = -15  # bounce up
                else:
                    game_over = True

        # Coin collection
        for coin in coins[:]:
            if mario.colliderect(coin):
                coins.remove(coin)
                score += 5

        # Leveling up
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds // 15 >= level:
            level += 1
            enemy_speed += 1
            enemies.append(spawn_enemy())
            coins.append(spawn_coin())

        # Draw Mario
        pygame.draw.rect(screen, RED, mario)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, BLUE, enemy["rect"])

        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, GOLD, coin.center, 100)

        # Score increase over time
        score += 0.02

    else:
        game_over_text = big_font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 40))

    # Draw score and level
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()




