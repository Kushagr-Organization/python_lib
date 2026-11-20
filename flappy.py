"""
Flappy-style game in Python using pygame.

Install:  pip install pygame
Run:      python flappy.py

Controls: SPACE / UP / left mouse click to flap. ESC to quit.
"""

import random
import sys

import pygame

# ---------- Settings ----------
WIDTH, HEIGHT = 400, 600
FPS = 60

GRAVITY = 0.45
FLAP_STRENGTH = -8.0
MAX_FALL_SPEED = 10

PIPE_WIDTH = 70
PIPE_GAP = 160
PIPE_SPEED = 3
PIPE_SPAWN_MS = 1500

GROUND_HEIGHT = 80

SKY = (113, 197, 207)
GREEN = (84, 176, 52)
DARK_GREEN = (56, 128, 32)
GROUND_COLOR = (222, 216, 149)
GROUND_TOP = (150, 200, 60)
YELLOW = (250, 220, 60)
ORANGE = (240, 140, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SPAWN_EVENT = pygame.USEREVENT + 1


class Player:
    RADIUS = 14

    def __init__(self):
        self.x = 100
        self.reset()

    def reset(self):
        self.y = HEIGHT // 2
        self.vel = 0.0

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL_SPEED)
        self.y += self.vel

    @property
    def rect(self):
        r = self.RADIUS - 2  # slightly forgiving hitbox
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)

    def draw(self, surf):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(surf, YELLOW, center, self.RADIUS)
        pygame.draw.circle(surf, BLACK, center, self.RADIUS, 2)
        # eye
        pygame.draw.circle(surf, WHITE, (center[0] + 6, center[1] - 4), 5)
        pygame.draw.circle(surf, BLACK, (center[0] + 8, center[1] - 4), 2)
        # beak
        pygame.draw.polygon(
            surf,
            ORANGE,
            [(center[0] + 12, center[1]), (center[0] + 22, center[1] + 3), (center[0] + 12, center[1] + 7)],
        )
        # wing (flaps depending on velocity)
        wing_y = center[1] + (4 if self.vel < 0 else 8)
        pygame.draw.ellipse(surf, ORANGE, (center[0] - 12, wing_y - 4, 14, 8))


class Pipe:
    def __init__(self, x):
        self.x = x
        min_top = 70
        max_top = HEIGHT - GROUND_HEIGHT - PIPE_GAP - 70
        self.gap_top = random.randint(min_top, max_top)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    @property
    def top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_top)

    @property
    def bottom_rect(self):
        y = self.gap_top + PIPE_GAP
        return pygame.Rect(self.x, y, PIPE_WIDTH, HEIGHT - GROUND_HEIGHT - y)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collides(self, rect):
        return rect.colliderect(self.top_rect) or rect.colliderect(self.bottom_rect)

    def draw(self, surf):
        for rect, is_top in ((self.top_rect, True), (self.bottom_rect, False)):
            pygame.draw.rect(surf, GREEN, rect)
            pygame.draw.rect(surf, DARK_GREEN, rect, 3)
            # pipe cap
            cap_h = 22
            cap_y = rect.bottom - cap_h if is_top else rect.top
            cap = pygame.Rect(rect.x - 4, cap_y, PIPE_WIDTH + 8, cap_h)
            pygame.draw.rect(surf, GREEN, cap)
            pygame.draw.rect(surf, DARK_GREEN, cap, 3)


def draw_ground(surf, offset):
    y = HEIGHT - GROUND_HEIGHT
    pygame.draw.rect(surf, GROUND_COLOR, (0, y, WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(surf, GROUND_TOP, (0, y, WIDTH, 14))
    for x in range(-20 + offset, WIDTH + 20, 24):
        pygame.draw.line(surf, DARK_GREEN, (x, y + 14), (x - 12, y + 2), 3)


def draw_text(surf, text, font, color, center, shadow=True):
    if shadow:
        s = font.render(text, True, BLACK)
        surf.blit(s, s.get_rect(center=(center[0] + 2, center[1] + 2)))
    t = font.render(text, True, color)
    surf.blit(t, t.get_rect(center=center))


def load_best():
    try:
        with open("flappy_best.txt") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_best(score):
    try:
        with open("flappy_best.txt", "w") as f:
            f.write(str(score))
    except OSError:
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Game")
    clock = pygame.time.Clock()

    big_font = pygame.font.SysFont("arial", 48, bold=True)
    med_font = pygame.font.SysFont("arial", 28, bold=True)
    small_font = pygame.font.SysFont("arial", 20)

    player = Player()
    pipes = []
    score = 0
    best = load_best()
    state = "ready"  # ready, playing, dead
    ground_offset = 0

    pygame.time.set_timer(SPAWN_EVENT, PIPE_SPAWN_MS)

    def restart():
        nonlocal pipes, score, state
        player.reset()
        pipes = []
        score = 0
        state = "ready"

    while True:
        # ---------- Events ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            flap_pressed = (
                (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP))
                or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            )

            if flap_pressed:
                if state == "ready":
                    state = "playing"
                    pipes.append(Pipe(WIDTH + 20))
                    player.flap()
                elif state == "playing":
                    player.flap()
                elif state == "dead":
                    restart()

            if event.type == SPAWN_EVENT and state == "playing":
                pipes.append(Pipe(WIDTH + 20))

        # ---------- Update ----------
        if state == "ready":
            # gentle bobbing
            player.y = HEIGHT // 2 + pygame.math.Vector2(0, 8).rotate(pygame.time.get_ticks() * 0.3).y
            ground_offset = (ground_offset - PIPE_SPEED) % 24

        elif state == "playing":
            player.update()
            ground_offset = (ground_offset - PIPE_SPEED) % 24

            for pipe in pipes:
                pipe.update()
                if not pipe.passed and pipe.x + PIPE_WIDTH < player.x:
                    pipe.passed = True
                    score += 1
            pipes = [p for p in pipes if not p.off_screen()]

            hit_pipe = any(p.collides(player.rect) for p in pipes)
            hit_ground = player.y + Player.RADIUS >= HEIGHT - GROUND_HEIGHT
            hit_ceiling = player.y - Player.RADIUS <= 0

            if hit_pipe or hit_ground or hit_ceiling:
                state = "dead"
                if score > best:
                    best = score
                    save_best(best)

        elif state == "dead":
            # let the player fall to the ground
            if player.y + Player.RADIUS < HEIGHT - GROUND_HEIGHT:
                player.update()

        # ---------- Draw ----------
        screen.fill(SKY)
        for pipe in pipes:
            pipe.draw(screen)
        draw_ground(screen, int(ground_offset))
        player.draw(screen)

        if state == "ready":
            draw_text(screen, "Get Ready!", big_font, WHITE, (WIDTH // 2, 150))
            draw_text(screen, "Press SPACE or click to flap", small_font, WHITE, (WIDTH // 2, 210))
        elif state == "playing":
            draw_text(screen, str(score), big_font, WHITE, (WIDTH // 2, 60))
        elif state == "dead":
            draw_text(screen, "Game Over", big_font, WHITE, (WIDTH // 2, 190))
            draw_text(screen, f"Score: {score}", med_font, WHITE, (WIDTH // 2, 260))
            draw_text(screen, f"Best: {best}", med_font, WHITE, (WIDTH // 2, 300))
            draw_text(screen, "Press SPACE or click to restart", small_font, WHITE, (WIDTH // 2, 360))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()