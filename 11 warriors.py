import pygame
import sys
import lvl
import asyncio
import os

if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('11 Warriors')


def load(path):
    return pygame.image.load(path).convert_alpha()


def get_image(sheet, frame_x, frame_y, width, height, scale, colorkey):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (frame_x * width, frame_y * height, width, height))
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    image.set_colorkey(colorkey)
    return image


def brighten_for_night(image):
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, world, char):
        super().__init__()
        self.full = load('sprites/full.png')
        self.half = load('sprites/half.png')
        self.empty = load('sprites/empty.png')
        self.world = world
        self.sheet = load(f'sprites/{char}.png')

        if char == 'knight':
            self.run_right = [get_image(self.sheet, i, 2, 32, 32, 2, (0, 0, 0)) for i in range(8)]
            self.run_right.extend([get_image(self.sheet, i, 3, 32, 32, 2, (0, 0, 0)) for i in range(8)])
            self.run_left = [pygame.transform.flip(f, True, False) for f in self.run_right]
            self.idle = [get_image(self.sheet, i, 0, 32, 32, 2, (0, 0, 0)) for i in range(4)]
            self.jump = get_image(self.sheet, 6, 5, 32, 32, 2, (0, 0, 0))
            self.run_speed = 0.1
        else:
            idle_row = 1 if char == 'mordred' else 0
            r1, r2 = (2, 3) if char == 'mordred' else (1, 2)
            self.idle = [get_image(self.sheet, i, idle_row, 32, 32, 2, (0, 0, 0)) for i in range(4)]
            self.run_right = [get_image(self.sheet, i, r1, 32, 32, 2, (0, 0, 0)) for i in range(4)]
            self.run_right.extend([get_image(self.sheet, i, r2, 32, 32, 2, (0, 0, 0)) for i in range(4)])
            self.run_left = [get_image(self.sheet, i, r1, 32, 32, 2, (0, 0, 0)) for i in range(4, 8)]
            self.run_left.extend([get_image(self.sheet, i, r2, 32, 32, 2, (0, 0, 0)) for i in range(4, 8)])
            jump_row = {
                'merlin': 3, 'arthurPendragon': 4, 'guinevere': 3, 'lancelot': 4,
                'gawain': 4, 'percival': 4, 'ladyOfTheLake': 3, 'mordred': 5,
                'morganLeFay': 3, 'fisherKing': 3,
            }[char]
            self.jump = get_image(self.sheet, 0, jump_row, 32, 32, 2, (0, 0, 0))
            self.run_speed = 0.1

        self.run = self.run_right
        if char != 'gawain':
            self.run_right = [brighten_for_night(frame) for frame in self.run_right]
            self.run_left = [brighten_for_night(frame) for frame in self.run_left]
            self.idle = [brighten_for_night(frame) for frame in self.idle]
            self.jump = brighten_for_night(self.jump)
        self.current_sprite = 0
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = self.world.p_x - 10
        self.rect.y = self.world.p_y
        self.hb = pygame.Rect(
            self.rect.x + 20,
            self.rect.y + 20,
            self.rect.width - 40,
            self.rect.height - 30,
        )
        self.direction = 'right'
        self.spd = 5
        self.is_anim = 'idle'
        self.gravity = 1
        self.jump_height = 14
        self.velocity_y = 0
        self.on_ground = False
        self.invincible = 0
        self.kb = 2.5
        self.knockback_velocity_x = 0
        self.h1 = self.full
        self.h2 = self.full
        self.h3 = self.full
        self.enemies = [Slime, Chicken, GiantFrog]
        self.death_font = pygame.font.Font('fonts/PixelOperator8-Bold.ttf', 40)
        self.deadl1 = self.death_font.render('GAME OVER...', True, 'black')
        self.deadl2 = self.death_font.render('Press R to restart.', True, 'black')

    def take_hit(self, damage, knockback_direction):
        # Returns False if the hit was ignored (invincible / already dead).
        if self.invincible > 0 or (self.h1 == self.empty and self.h2 == self.empty and self.h3 == self.empty):
            return False

        # Hearts are lost right-to-left, half a heart per hit.
        if self.h3 == self.full:
            self.h3 = self.half
        elif self.h3 == self.half:
            self.h3 = self.empty
        elif self.h3 == self.empty:
            if self.h2 == self.full:
                self.h2 = self.half
            elif self.h2 == self.half:
                self.h2 = self.empty
            elif self.h2 == self.empty:
                if self.h1 == self.full:
                    self.h1 = self.half
                elif self.h1 == self.half:
                    self.h1 = self.empty

        self.invincible = 45
        self.knockback_velocity_x = knockback_direction * 8
        self.velocity_y = -4
        self.on_ground = False
        return True

    def move(self):
        keys = pygame.key.get_pressed()

        self.velocity_y += self.gravity
        if self.velocity_y >= 16:
            self.velocity_y = 16
            self.on_ground = False

        self.hb.y += self.velocity_y

        if self.velocity_y > 0:
            self.on_ground = False
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.velocity_y = 0
                    self.hb.bottom = tr.top
                    self.on_ground = True

        if self.velocity_y < 0:
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.hb.top = tr.bottom
                    self.on_ground = False
                    self.velocity_y += self.gravity
                    self.rect.y += self.velocity_y

        if abs(self.knockback_velocity_x) >= 1:
            knockback_step = int(round(self.knockback_velocity_x))
            self.hb.x += knockback_step
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    if knockback_step > 0:
                        self.hb.right = tr.left
                    else:
                        self.hb.left = tr.right
                    self.knockback_velocity_x = 0
                    break
            else:
                self.knockback_velocity_x *= 0.75
        else:
            self.knockback_velocity_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.hb.x -= self.spd
                self.direction = 'left'
                self.is_anim = 'run'
                for tile in self.world.tile_list:
                    tr = tile[1]
                    if self.hb.colliderect(tr):
                        self.hb.left = tr.right
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.hb.x += self.spd
                self.direction = 'right'
                self.is_anim = 'run'
                for tile in self.world.tile_list:
                    tr = tile[1]
                    if self.hb.colliderect(tr):
                        self.hb.right = tr.left

        if not self.on_ground:
            self.is_anim = 'jump'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.is_anim = 'run'
        else:
            self.is_anim = 'idle'

        if self.is_anim == 'run':
            self.run = self.run_right if self.direction == 'right' else self.run_left
            self.current_sprite += self.run_speed
            if self.current_sprite >= len(self.run):
                self.current_sprite = 0
            self.image = self.run[int(self.current_sprite)]

        if self.is_anim == 'idle':
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.idle):
                self.current_sprite = 0
            self.image = self.idle[int(self.current_sprite)]

        if self.is_anim == 'jump':
            self.image = self.jump

        if self.direction == 'left' and self.is_anim != 'run':
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x = self.hb.x - 20
        self.rect.y = self.hb.y - 20

    def update(self):
        self.move()
        if self.invincible > 0:
            self.invincible -= 1
        screen.blit(self.h1, (0, 0))
        screen.blit(self.h2, (16, 0))
        screen.blit(self.h3, (32, 0))


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, world, sheet, font):
        super().__init__()
        self.world = world
        self.sheet = sheet
        self.run = [brighten_for_night(get_image(self.sheet, i, 1, 24, 24, 2, (0, 0, 0))) for i in range(4)]
        self.idle = [brighten_for_night(get_image(self.sheet, i, 0, 24, 24, 2, (0, 0, 0))) for i in range(4)]
        self.idle.extend([brighten_for_night(get_image(self.sheet, i, 0, 24, 24, 2, (0, 0, 0))) for i in range(2, 0, -1)])
        self.current_sprite = 0
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hb = pygame.Rect(
            self.rect.x - 40,
            self.rect.y + 20,
            self.rect.width - 20,
            self.rect.height - 25,
        )
        self.direction = 'right'
        self.spd = 4
        self.is_anim = 'idle'
        self.gravity = 1
        self.jump_height = 16
        self.velocity_y = 0
        self.on_ground = False
        self.c = font.render('!', True, 'black')
        self.chase = False
        self.range = pygame.Rect(self.hb.x - 100, self.hb.y, self.hb.width + 200, self.hb.height)
        self.max_health = 25
        self.health = self.max_health
        self.knockback_velocity_x = 0

    def take_hit(self, damage, knockback_direction):
        self.health = max(0, self.health - damage)
        self.knockback_velocity_x = knockback_direction * 8
        self.velocity_y = -4
        self.on_ground = False

    def move(self):
        self.velocity_y += self.gravity
        if self.velocity_y >= 15:
            self.velocity_y = 15
            self.on_ground = False

        self.hb.y += self.velocity_y

        if self.velocity_y > 0:
            self.on_ground = False
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.velocity_y = 0
                    self.hb.bottom = tr.top
                    self.on_ground = True

        if self.velocity_y < 0:
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.hb.top = tr.bottom
                    self.on_ground = False
                    self.velocity_y += self.gravity
                    self.rect.y += self.velocity_y

        # Chase the player when they are inside the aggro range.
        if self.range.colliderect(player.hb):
            screen.blit(self.c, (self.hb.centerx - 5, self.hb.top - 25))
            if player.hb.centerx > self.range.centerx:
                self.direction = 'right'
                self.is_anim = 'run'
                self.chase = 'right'
            if player.hb.centerx < self.range.centerx:
                self.direction = 'left'
                self.is_anim = 'run'
                self.chase = 'left'
        else:
            self.is_anim = 'idle'
            self.chase = False

        if self.is_anim == 'run':
            self.current_sprite += 0.14
            if self.current_sprite >= len(self.run):
                self.current_sprite = 0
            self.image = self.run[int(self.current_sprite)]

        if self.is_anim == 'idle':
            self.current_sprite += 0.11
            if self.current_sprite >= len(self.idle):
                self.current_sprite = 0
            self.image = self.idle[int(self.current_sprite)]

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.y = self.hb.y - 25

        if abs(self.knockback_velocity_x) >= 1:
            knockback_step = int(round(self.knockback_velocity_x))
            self.hb.x += knockback_step
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    if knockback_step > 0:
                        self.hb.right = tr.left
                    else:
                        self.hb.left = tr.right
                    self.knockback_velocity_x = 0
                    break
            else:
                self.knockback_velocity_x *= 0.75
        else:
            self.knockback_velocity_x = 0
            if self.chase == 'right':
                self.hb.x += player.spd - 2
            if self.chase == 'left':
                self.hb.x -= player.spd - 2

        # Touching the player hurts them.
        if self.hb.colliderect(player.hb):
            player_knockback_direction = 1 if player.hb.centerx >= self.hb.centerx else -1
            if player.take_hit(10, player_knockback_direction):
                self.take_hit(0, -player_knockback_direction)
            else:
                player.hb.x += player_knockback_direction * player.kb

        self.rect.x = self.hb.x - 10.5

        # Health bar
        bar_width = 2.5 * self.max_health
        bar_x = self.hb.centerx - self.hb.width * 1.5
        bar_y = self.hb.centery - self.hb.height
        pygame.draw.rect(screen, 'red', (bar_x, bar_y, bar_width, 5))
        pygame.draw.rect(screen, 'green', (bar_x, bar_y, bar_width * self.health / self.max_health, 5))

    def update(self):
        self.move()
        self.range = pygame.Rect(self.hb.x - 100, self.hb.y - 10, self.hb.width + 200, self.hb.height + 10)


class Chicken(pygame.sprite.Sprite):
    def __init__(self, x, y, world, sheet, font):
        super().__init__()
        self.world = world
        self.sheet = sheet
        self.idle = [brighten_for_night(get_image(self.sheet, i, 0, 16, 16, 2, (0, 0, 0))) for i in range(1)]
        self.bullet = load('sprites/Seed1.png')
        self.bullet_mask = pygame.mask.from_surface(self.bullet)
        self.current_sprite = 0
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hb = pygame.Rect(
            self.rect.x + 20,
            self.rect.y + 20,
            self.rect.width - 20,
            self.rect.height - 25,
        )
        self.direction = 'right'
        self.spd = 4
        self.is_anim = 'idle'
        self.gravity = 1
        self.jump_height = 16
        self.velocity_y = 0
        self.on_ground = False
        self.c = font.render('!', True, 'black')
        self.range = pygame.Rect(self.hb.x - 100, self.hb.y, self.hb.width + 200, self.hb.height)
        self.max_health = 50
        self.health = self.max_health
        self.knockback_velocity_x = 0
        self.bullets = []
        self.cooldown = 120
        self.warning_frames = 30

    def take_hit(self, damage, knockback_direction):
        self.health = max(0, self.health - damage)
        self.knockback_velocity_x = knockback_direction * 8
        self.velocity_y = -4
        self.on_ground = False

    def shoot(self):
        origin = pygame.Vector2(self.hb.center)
        direction = pygame.Vector2(1 if player.hb.centerx >= self.hb.centerx else -1, 0)
        bullet_rect = self.bullet.get_rect()
        spawn_distance = self.rect.width / 2 + bullet_rect.width / 2
        bullet_position = origin + direction * spawn_distance

        bullet_offset_x = 0
        bullet_offset_y = -10
        bullet_position += pygame.Vector2(bullet_offset_x, bullet_offset_y)
        bullet_rect.center = (round(bullet_position.x), round(bullet_position.y))
        velocity = direction * (player.spd - 1)
        self.bullets.append([bullet_rect, pygame.Vector2(bullet_rect.topleft), velocity])
        self.cooldown = 120

    def update_bullets(self):
        player_mask = pygame.mask.from_surface(player.image)
        for bullet in self.bullets[:]:
            bullet_rect, bullet_position, velocity = bullet
            bullet_position += velocity
            bullet_rect.topleft = (round(bullet_position.x), round(bullet_position.y))
            screen.blit(self.bullet, bullet_rect)

            offset = (player.rect.x - bullet_rect.x, player.rect.y - bullet_rect.y)
            if self.bullet_mask.overlap(player_mask, offset) is not None:
                player.take_hit(10, 1 if velocity.x >= 0 else -1)
                self.bullets.remove(bullet)
            elif not screen.get_rect().colliderect(bullet_rect):
                self.bullets.remove(bullet)

    def block_bullets_with_sword(self, sword_mask, sword_rect):
        # The sword swing destroys bullets it touches.
        for bullet in self.bullets[:]:
            bullet_rect = bullet[0]
            offset = (bullet_rect.left - sword_rect.left, bullet_rect.top - sword_rect.top)
            if bullet_rect.colliderect(sword_rect) and sword_mask.overlap(self.bullet_mask, offset) is not None:
                self.bullets.remove(bullet)

    def move(self):
        self.velocity_y += self.gravity
        if self.velocity_y >= 15:
            self.velocity_y = 15
            self.on_ground = False

        self.hb.y += self.velocity_y

        if self.velocity_y > 0:
            self.on_ground = False
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.velocity_y = 0
                    self.hb.bottom = tr.top
                    self.on_ground = True

        if self.velocity_y < 0:
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    self.hb.top = tr.bottom
                    self.on_ground = False
                    self.velocity_y += self.gravity
                    self.rect.y += self.velocity_y

        # Face the player and shoot when in range.
        if self.range.colliderect(player.hb):
            self.direction = 'right' if player.hb.centerx >= self.hb.centerx else 'left'
            self.is_anim = 'idle'
            if self.cooldown > 0:
                self.cooldown -= 1
            if self.cooldown <= self.warning_frames:
                screen.blit(self.c, (self.hb.centerx - 10, self.hb.top - 50))
            if self.cooldown == 0:
                self.shoot()
        else:
            self.is_anim = 'idle'

        if self.is_anim == 'idle':
            self.current_sprite += 0.11
            if self.current_sprite >= len(self.idle):
                self.current_sprite = 0
            self.image = self.idle[int(self.current_sprite)]

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.y = self.hb.y - 25

        if abs(self.knockback_velocity_x) >= 1:
            knockback_step = int(round(self.knockback_velocity_x))
            self.hb.x += knockback_step
            for tile in self.world.tile_list:
                tr = tile[1]
                if self.hb.colliderect(tr):
                    if knockback_step > 0:
                        self.hb.right = tr.left
                    else:
                        self.hb.left = tr.right
                    self.knockback_velocity_x = 0
                    break
            else:
                self.knockback_velocity_x *= 0.75
        else:
            self.knockback_velocity_x = 0

        if self.hb.colliderect(player.hb):
            player_knockback_direction = 1 if player.hb.centerx >= self.hb.centerx else -1
            if player.take_hit(10, player_knockback_direction):
                self.take_hit(0, -player_knockback_direction)
            else:
                player.hb.x += player_knockback_direction * player.kb

        self.rect.x = self.hb.x - 22.5

    def draw_health_bar(self):
        bar_width = 2.5 * self.max_health
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 8
        pygame.draw.rect(screen, 'red', (bar_x, bar_y, bar_width, 5))
        pygame.draw.rect(screen, 'green', (bar_x, bar_y, bar_width * self.health / self.max_health, 5))

    def update(self):
        self.move()
        self.update_bullets()
        self.range = pygame.Rect(self.hb.x - 200, self.hb.y - 10, self.hb.width + 400, self.hb.height + 10)


class GiantFrog(pygame.sprite.Sprite):
    def __init__(self, world, font):
        super().__init__()
        self.world = world

        idle_sheet = load('GiantFrog2/Idle.png')
        hop_sheet = load('GiantFrog2/Jump.png')
        attack_sheet = load('GiantFrog2/ChargeAttack.png')
        self.idle_frames = [brighten_for_night(get_image(idle_sheet, i, 0, 40, 40, 2, (0, 0, 0))) for i in range(5)]
        self.hop_frames = [brighten_for_night(get_image(hop_sheet, i, 0, 40, 40, 2, (0, 0, 0))) for i in range(6)]

        self.charge_frames = [brighten_for_night(get_image(attack_sheet, i, 0, 40, 40, 2, (0, 0, 0))) for i in range(7)]
        self.attack_frames = [brighten_for_night(get_image(attack_sheet, i, 0, 40, 40, 2, (0, 0, 0))) for i in range(7, 10)]

        wave_sheet = load('GiantFrog2/Wave.png')
        self.wave_frames = [get_image(wave_sheet, i, 0, 32, 32, 4, (0, 0, 0)) for i in range(4)]
        self.wave_frame = 0
        self.wave_ticks = 0
        self.wave_ticks_per_frame = 5
        self.wave_active = False

        self.state = 'idle'
        self.state_frame = 0
        self.state_ticks = 0
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()

        self.rect.x = world.f_x
        self.rect.y = world.f_y
        self.hb = pygame.Rect(self.rect.x + 20, self.rect.y + 30, 40, 50)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = 'right'
        self.gravity = 1
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.knockback_velocity_x = 0

        self.c = font.render('!', True, 'black')
        self.aggro_distance = 700
        self.range = pygame.Rect(0, 0, 0, 0)
        self.show_warning = False

        self.max_health = 100
        self.health = self.max_health
        self.cooldown = 60
        self.warning_frames = 30
        self.hop_height = 12
        self.hop_speed = 10
        self.wave_damage = 15

    def take_hit(self, damage, knockback_direction):
        self.health = max(0, self.health - damage)
        self.knockback_velocity_x = knockback_direction * 8
        self.velocity_y = -4
        self.on_ground = False

    def set_image(self, frame):
        self.image = pygame.transform.flip(frame, self.direction == 'right', False)
        self.rect.size = self.image.get_size()
        self.rect.x = self.hb.x - 20
        self.mask = pygame.mask.from_surface(self.image)

        # Line the feet of the visible sprite up with the hitbox bottom.
        mask_rects = self.mask.get_bounding_rects()
        visible_bottom = max((rect.bottom for rect in mask_rects), default=self.image.get_height())
        self.rect.y = self.hb.bottom - visible_bottom + 20

    def start_hop(self):
        self.state = 'hop'
        self.state_frame = 0
        self.state_ticks = 0
        self.velocity_y = -self.hop_height

        self.direction = 'right' if player.hb.centerx >= self.hb.centerx else 'left'
        self.velocity_x = self.hop_speed if self.direction == 'right' else -self.hop_speed

        self.on_ground = False
        self.cooldown = 60

    def charge(self):
        self.state = 'charge'
        self.state_frame = 0
        self.state_ticks = 0
        self.velocity_x = 0

    def start_attack(self):
        self.state = 'attack'
        self.state_frame = 0
        self.state_ticks = 0
        self.wave_active = True
        self.wave_frame = 0
        self.wave_ticks = 0

        # Shockwave damages the player if they are close enough.
        wave_hitbox = pygame.Rect(self.hb.centerx - 90, self.hb.centery - 75, 180, 150)
        if wave_hitbox.colliderect(player.hb):
            direction = 1 if player.hb.centerx >= self.hb.centerx else -1
            player.take_hit(self.wave_damage, direction)

    def wave(self):
        if not self.wave_active:
            return

        frame = self.wave_frames[self.wave_frame]
        wave_x = self.hb.centerx - frame.get_width() // 2
        wave_y = self.hb.centery - frame.get_height() // 2
        screen.blit(frame, (wave_x, wave_y))

        self.wave_ticks += 1
        if self.wave_ticks >= self.wave_ticks_per_frame:
            self.wave_ticks = 0
            self.wave_frame += 1
            if self.wave_frame >= len(self.wave_frames):
                self.wave_active = False
                self.wave_frame = 0

    def move_horizontal(self, amount):
        if not amount:
            return

        self.hb.x += int(round(amount))
        for _, tile_rect in self.world.tile_list:
            if self.hb.colliderect(tile_rect):
                if amount > 0:
                    self.hb.right = tile_rect.left
                else:
                    self.hb.left = tile_rect.right
                self.velocity_x = 0
                return

    def move(self):
        self.range = pygame.Rect(
            self.hb.centerx - self.aggro_distance,
            self.hb.y - 180,
            self.aggro_distance * 2,
            self.hb.height + 360,
        )
        player_in_range = self.range.colliderect(player.hb)
        self.show_warning = False

        self.direction = 'right' if player.hb.centerx >= self.hb.centerx else 'left'

        if self.state == 'idle' and player_in_range:
            if self.cooldown > 0:
                self.cooldown -= 1
            self.show_warning = 0 < self.cooldown <= self.warning_frames
            if self.cooldown == 0 and self.on_ground:
                self.start_hop()

        self.velocity_y = min(self.velocity_y + self.gravity, 15)
        self.hb.y += int(round(self.velocity_y))
        self.on_ground = False
        for _, tile_rect in self.world.tile_list:
            if self.hb.colliderect(tile_rect):
                if self.velocity_y > 0:
                    self.hb.bottom = tile_rect.top
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.hb.top = tile_rect.bottom
                self.velocity_y = 0
                break

        if self.state == 'hop':
            self.move_horizontal(self.velocity_x)
            if self.on_ground:
                self.charge()

        if abs(self.knockback_velocity_x) >= 1:
            self.move_horizontal(self.knockback_velocity_x)
            self.knockback_velocity_x *= 0.75
        else:
            self.knockback_velocity_x = 0

        if self.hb.colliderect(player.hb):
            direction = 1 if player.hb.centerx >= self.hb.centerx else -1
            if player.take_hit(10, direction):
                self.knockback_velocity_x = -direction * 4
            else:
                player.hb.x += direction * player.kb

        self.rect.x = self.hb.x - 20

    def update(self):
        self.move()

        if self.state == 'idle':
            self.state_ticks += 1
            self.state_frame = (self.state_ticks // 8) % len(self.idle_frames)
            frame = self.idle_frames[self.state_frame]
        elif self.state == 'hop':
            self.state_ticks += 1
            self.state_frame = (self.state_ticks // 6) % len(self.hop_frames)
            frame = self.hop_frames[self.state_frame]
        elif self.state == 'charge':
            self.state_ticks += 1
            frame_ticks = 6
            self.state_frame = min(self.state_ticks // frame_ticks, len(self.charge_frames) - 1)
            frame = self.charge_frames[self.state_frame]
            if self.state_ticks >= len(self.charge_frames) * frame_ticks:
                self.start_attack()
        else:
            self.state_ticks += 1
            frame_ticks = 8
            self.state_frame = min(self.state_ticks // frame_ticks, len(self.attack_frames) - 1)
            frame = self.attack_frames[self.state_frame]
            if self.state_ticks >= len(self.attack_frames) * frame_ticks:
                self.state = 'idle'
                self.state_ticks = 0
                self.state_frame = 0

        self.set_image(frame)

    def draw_effects(self):
        self.wave()
        if self.show_warning:
            screen.blit(
                self.c,
                (self.rect.centerx - self.c.get_width() // 2, self.rect.top - self.c.get_height() - 8),
            )

        bar_width = self.rect.width
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 8
        pygame.draw.rect(screen, 'red', (bar_x, bar_y, bar_width, 5))
        pygame.draw.rect(screen, 'green', (bar_x, bar_y, bar_width * self.health / self.max_health, 5))


LEVEL = lvl.level1


class Door(pygame.sprite.Sprite):
    def __init__(self, world):
        super().__init__()
        self.open = load('sprites/door_open.png')
        self.close = load('sprites/door_close.png')
        self.image = self.close
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = world.d_x
        self.rect.y = world.d_y
        self.attack = True


tile_size = 40


class World:
    """Builds solid tiles and spawn points from a level grid.

    Tile codes: 1 dirt, 2 grass, 3 slime spawn, 4 player spawn,
    5 door, 6 chicken spawn, 7 giant frog spawn.
    """

    def __init__(self, data):
        self.tile_list = []
        self.sheet = load('sprites/world_tileset.png')
        self.sheet2 = load('sprites/slime_purple.png')
        grass = get_image(self.sheet, 0, 0, 16, 16, 2, (0, 0, 0))
        dirt = get_image(self.sheet, 0, 1, 16, 16, 2, (0, 0, 0))
        self.slime = []
        self.chicken = []
        self.p_x = 0
        self.p_y = 0
        self.d_x = 0
        self.d_y = 0
        self.f_x = 0
        self.f_y = 0

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    x = col_count * tile_size
                    y = row_count * tile_size
                    self.slime.append([x, y])
                elif tile == 4:
                    self.p_x = col_count * tile_size
                    self.p_y = row_count * tile_size
                elif tile == 5:
                    self.d_x = col_count * tile_size
                    self.d_y = row_count * tile_size
                elif tile == 6:
                    x = col_count * tile_size
                    y = row_count * tile_size
                    self.chicken.append([x, y])
                elif tile == 7:
                    self.f_x = col_count * tile_size
                    self.f_y = row_count * tile_size
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Sky:
    """Background gradient made of tileset rows 9-13."""

    def __init__(self, data):
        self.tile_list = []
        self.sheet = load('sprites/world_tileset.png')
        w = get_image(self.sheet, 0, 9, 16, 16, 2, (0, 0, 0))
        w_lb = get_image(self.sheet, 0, 10, 16, 16, 2, (0, 0, 0))
        lb_b = get_image(self.sheet, 0, 11, 16, 16, 2, (0, 0, 0))
        b_db = get_image(self.sheet, 0, 12, 16, 16, 2, (0, 0, 0))
        db = get_image(self.sheet, 0, 13, 16, 16, 2, (0, 0, 0))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    img = pygame.transform.scale(w, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 1:
                    img = pygame.transform.scale(w_lb, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(lb_b, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    img = pygame.transform.scale(b_db, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 4:
                    img = pygame.transform.scale(db, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Attack:
    """The player's weapon swing (sword or staff)."""

    def __init__(self, user, wpn):
        self.user = user
        self.frames_right = []
        self.frames_left = []
        sword_sheet = load(f'sprites/{wpn}.png')
        for frame_number in range(4):
            frame_right = sword_sheet.subsurface((frame_number * 32, 32, 32, 32)).copy()
            frame_left = sword_sheet.subsurface((frame_number * 32, 64, 32, 32)).copy()
            frame_right = pygame.transform.scale(frame_right, (64, 64))
            frame_left = pygame.transform.scale(frame_left, (64, 64))
            self.frames_right.append(pygame.transform.rotate(frame_right, -90))
            self.frames_left.append(pygame.transform.rotate(frame_left, 90))

        self.masks_right = [pygame.mask.from_surface(frame) for frame in self.frames_right]
        self.masks_left = [pygame.mask.from_surface(frame) for frame in self.frames_left]
        self.frame_index = None
        self.frame_ticks = 0

        if wpn == 'staff_':
            self.ticks_per_frame = 4
            self.damage = 8
        else:
            self.ticks_per_frame = 5
            self.damage = 12
        self.hit_targets = set()
        self.is_attack = False

    def start(self):
        # Ignore the press if a swing is already in progress.
        if self.frame_index is None:
            self.frame_index = 0
            self.frame_ticks = 0
            self.hit_targets.clear()

    def update(self, targets):
        global num
        if self.frame_index is None:
            return

        facing_left = self.user.direction == 'left'
        frames = self.frames_left if facing_left else self.frames_right
        masks = self.masks_left if facing_left else self.masks_right
        frame = frames[self.frame_index]
        attack_rect = frame.get_rect()
        attack_rect.centery = self.user.hb.centery + 10

        if facing_left:
            attack_rect.right = self.user.hb.right + 5
        else:
            attack_rect.left = self.user.hb.left - 5

        attack_mask = masks[self.frame_index]

        # Only the middle frames of the swing can hit.
        if self.frame_index in (1, 2):
            for target in list(targets):
                if isinstance(target, Chicken):
                    target.block_bullets_with_sword(attack_mask, attack_rect)
                if not isinstance(target, (Slime, Chicken, GiantFrog)) or target.health <= 0 or target in self.hit_targets:
                    continue

                target_mask = pygame.mask.from_surface(target.image)
                offset = (target.rect.left - attack_rect.left, target.rect.top - attack_rect.top)
                if attack_mask.overlap(target_mask, offset) is not None:
                    target.take_hit(self.damage, -1 if facing_left else 1)
                    self.hit_targets.add(target)
                    if target.health == 0:
                        target.kill()
                        if LEVEL in (lvl.level2, lvl.level3, lvl.level4):
                            num += 1

        screen.blit(frame, attack_rect)

        self.frame_ticks += 1
        if self.frame_ticks >= self.ticks_per_frame:
            self.frame_ticks = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames_right):
                self.frame_index = None
                self.hit_targets.clear()


try:
    font_b = pygame.font.Font('fonts/PixelOperator8-Bold.ttf', 45)
    font = pygame.font.Font('fonts/PixelOperator8.ttf', 20)
except FileNotFoundError:
    font_b = pygame.font.Font(None, 45)
    font = pygame.font.Font(None, 45)

slime_p = load('sprites/slime_purple.png')
slime_g = load('sprites/slime_green.png')
chicken_b = load('sprites/Chicken.png')
bgm = pygame.mixer.Sound('music/time_for_adventure.ogg')
sky = Sky(lvl.sky)
clock = pygame.time.Clock()
LEVEL = lvl.level1
quest = font.render('', True, 'black')
num = 0
total = 0

# ---- Character / weapon select screens ----
character_options = [
    ('knight', 'Knight'),
    ('arthurPendragon', 'Arthur Pendragon'),
    ('fisherKing', 'Fisher King'),
    ('gawain', 'Gawain'),
    ('guinevere', 'Guinevere'),
    ('ladyOfTheLake', 'Lady of the Lake'),
    ('lancelot', 'Lancelot'),
    ('merlin', 'Merlin'),
    ('mordred', 'Mordred'),
    ('morganLeFay', 'Morgan Le Fay'),
    ('percival', 'Percival'),
]
selected_character_index = 0
player_character = character_options[selected_character_index][0]
select_stage = 'character'
selector_title_font = pygame.font.Font(None, 44)
selector_font = pygame.font.Font(None, 22)
selector_cards = []
character_previews = {}
for index, (character, _) in enumerate(character_options):
    row, column = divmod(index, 5)
    if row == 2:
        column = 2
    selector_cards.append(pygame.Rect(36 + column * 188, 120 + row * 125, 176, 112))
    character_sheet = load(f'sprites/{character}.png')
    preview_row = 1 if character == 'mordred' else 0
    character_previews[character] = get_image(character_sheet, 0, preview_row, 32, 32, 1.5, (0, 0, 0))

wpn_options = [
    ('excalibur_', 'Sword'),
    ('staff_', 'Staff'),
]
wpn_stats = {
    'excalibur_': 'heavy hit - 12 dmg',
    'staff_': 'fast swing - 8 dmg',
}
weapon_cards = []
wpn_previews = {}
for index, (wpn, _) in enumerate(wpn_options):
    weapon_cards.append(pygame.Rect(width // 2 - 186 + index * 196, 210, 176, 112))
    wpn_sheet = load(f'sprites/{wpn}.png')
    wpn_previews[wpn] = get_image(wpn_sheet, 0, 0, 32, 32, 1.5, (0, 0, 0))
selected_wpn_index = 0
wpn_character = wpn_options[0][0]
selector_start_button = pygame.Rect(400, 510, 200, 55)

victory_coin = get_image(load('sprites/coin.png'), 0, 0, 16, 16, 2, (0, 0, 0))
bgm.set_volume(0.5)
bgm.play(loops=-1)


def lvl_rst():
    """(Re)build the world, player, door, weapon and enemies for LEVEL."""
    global world, player, door, attack, sprites, num, total
    world = World(LEVEL)
    player = Player(world, player_character)
    door = Door(world)
    attack = Attack(player, wpn_character)
    sprites = pygame.sprite.Group(door, player)

    if LEVEL == lvl.level5:
        sprites.add(GiantFrog(world, font_b))

    slime_sheet = slime_g
    for x, y in world.slime:
        sprites.add(Slime(x, y, world, slime_sheet, font))

    for x, y in world.chicken:
        sprites.add(Chicken(x, y, world, chicken_b, font))

    num = 0
    if LEVEL == lvl.level2:
        total = len(world.slime)
    else:
        total = 1


lvl_rst()


def draw_grid():
    for line in range(0, 26):
        pygame.draw.line(screen, pygame.Color('black'), (line * tile_size, 0), (line * tile_size, height))
    for line in range(0, 16):
        pygame.draw.line(screen, pygame.Color('black'), (0, line * tile_size), (width, line * tile_size))


def draw_character_select():
    screen.fill((100, 190, 225))
    title = selector_title_font.render('Choose your character', True, 'black')
    screen.blit(title, title.get_rect(center=(width // 2, 36)))
    instructions = selector_font.render('Click a character, then Start. You can use arrows and Enter too.', True, 'black')
    screen.blit(instructions, instructions.get_rect(center=(width // 2, 78)))

    for index, ((character, name), card) in enumerate(zip(character_options, selector_cards)):
        pygame.draw.rect(screen, (245, 245, 235), card)
        border_color = (255, 185, 35) if index == selected_character_index else (35, 45, 55)
        pygame.draw.rect(screen, border_color, card, 4 if index == selected_character_index else 2)
        preview = character_previews[character]
        screen.blit(preview, preview.get_rect(center=(card.centerx, card.y + 38)))
        label = selector_font.render(name, True, 'black')
        if label.get_width() > card.width - 8:
            label = pygame.font.Font(None, 18).render(name, True, 'black')
        screen.blit(label, label.get_rect(center=(card.centerx, card.y + 84)))

    pygame.draw.rect(screen, (95, 175, 90), selector_start_button)
    pygame.draw.rect(screen, (25, 45, 30), selector_start_button, 3)
    start_label = selector_font.render('START', True, 'black')
    screen.blit(start_label, start_label.get_rect(center=selector_start_button.center))


def draw_victory():
    # Vertical gradient background
    top = (255, 205, 90)
    bottom = (255, 243, 205)
    for y in range(height):
        t = y / height
        c = tuple(int(a + (b - a) * t) for a, b in zip(top, bottom))
        pygame.draw.line(screen, c, (0, y), (width, y))

    big_font = pygame.font.Font('fonts/PixelOperator8-Bold.ttf', 60)
    title = big_font.render('VICTORY!', True, (255, 185, 35))
    outline = big_font.render('VICTORY!', True, (0, 0, 0))
    trect = title.get_rect(center=(width // 2, 110))
    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)):
        screen.blit(outline, (trect.x + dx, trect.y + dy))
    screen.blit(title, trect)

    # Show the chosen hero
    sheet = load(f'sprites/{player_character}.png')
    idle_row = 1 if player_character == 'mordred' else 0
    hero = get_image(sheet, 0, idle_row, 32, 32, 4, (0, 0, 0))
    screen.blit(hero, hero.get_rect(center=(width // 2, 255)))

    hero_name = dict(character_options)[player_character]
    line1 = selector_font.render(f'{hero_name} has slain the Giant Frog!', True, (40, 30, 20))
    line2 = selector_font.render('The realm of Alden Grove is at peace... for now.', True, (40, 30, 20))
    screen.blit(line1, line1.get_rect(center=(width // 2, 330)))
    screen.blit(line2, line2.get_rect(center=(width // 2, 354)))

    esc_hint = selector_font.render('Press Esc to return to the character select.', True, (120, 80, 20))
    screen.blit(esc_hint, esc_hint.get_rect(center=(width // 2, 430)))

    coin = victory_coin
    screen.blit(coin, (width // 2 - 260, 320))
    screen.blit(coin, (width // 2 + 228, 320))


def draw_weapon_select():
    screen.fill((100, 190, 225))
    title = selector_title_font.render('Choose your weapon', True, 'black')
    screen.blit(title, title.get_rect(center=(width // 2, 36)))
    instructions = selector_font.render('Pick a weapon, then Start. Arrows or click. Esc goes back to characters.', True, 'black')
    screen.blit(instructions, instructions.get_rect(center=(width // 2, 78)))

    for index, ((wpn, name), card) in enumerate(zip(wpn_options, weapon_cards)):
        pygame.draw.rect(screen, (245, 245, 235), card)
        border_color = (255, 185, 35) if index == selected_wpn_index else (35, 45, 55)
        pygame.draw.rect(screen, border_color, card, 4 if index == selected_wpn_index else 2)
        preview = wpn_previews[wpn]
        screen.blit(preview, preview.get_rect(center=(card.centerx, card.y + 38)))
        label = selector_font.render(name, True, 'black')
        screen.blit(label, label.get_rect(center=(card.centerx, card.y + 80)))
        stat_font = pygame.font.Font(None, 17)
        stat_label = stat_font.render(wpn_stats[wpn], True, (90, 95, 105))
        screen.blit(stat_label, stat_label.get_rect(center=(card.centerx, card.y + 101)))

    pygame.draw.rect(screen, (95, 175, 90), selector_start_button)
    pygame.draw.rect(screen, (25, 45, 30), selector_start_button, 3)
    start_label = selector_font.render('START', True, 'black')
    screen.blit(start_label, start_label.get_rect(center=selector_start_button.center))


run = True


async def main():
    global run, LEVEL, select_stage, selected_character_index, player_character
    global selected_wpn_index, wpn_character, num, total, quest, advance_pressed

    while run:
        await asyncio.sleep(0)
        screen.fill((0, 255, 255))
        advance_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # ---- Menus (character / weapon select, victory) ----
            if select_stage != 'play':
                if select_stage == 'victory':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        LEVEL = lvl.level1
                        select_stage = 'character'
                    continue

                if event.type == pygame.KEYDOWN:
                    if select_stage == 'character':
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            selected_character_index = (selected_character_index - 1) % len(character_options)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            selected_character_index = (selected_character_index + 1) % len(character_options)
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            selected_character_index = (selected_character_index - 5) % len(character_options)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            selected_character_index = (selected_character_index + 5) % len(character_options)
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            player_character = character_options[selected_character_index][0]
                            select_stage = 'weapon'
                    else:
                        if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                            selected_wpn_index = (selected_wpn_index + 1) % len(wpn_options)
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            wpn_character = wpn_options[selected_wpn_index][0]
                            select_stage = 'play'
                            lvl_rst()
                        elif event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_b):
                            select_stage = 'character'
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if select_stage == 'character':
                        for index, card in enumerate(selector_cards):
                            if card.collidepoint(event.pos):
                                selected_character_index = index
                                break
                        if selector_start_button.collidepoint(event.pos):
                            player_character = character_options[selected_character_index][0]
                            select_stage = 'weapon'
                    else:
                        for index, card in enumerate(weapon_cards):
                            if card.collidepoint(event.pos):
                                selected_wpn_index = index
                                break
                        if selector_start_button.collidepoint(event.pos):
                            wpn_character = wpn_options[selected_wpn_index][0]
                            select_stage = 'play'
                            lvl_rst()
                continue

            # ---- In-game input ----
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    advance_pressed = True
                if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE) and player.on_ground:
                    player.velocity_y = -player.jump_height
                    player.on_ground = False
                    player.is_anim = 'jump'
                if event.key in (pygame.K_x, pygame.K_s, pygame.K_DOWN):
                    attack.start()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                attack.start()

        if not run:
            break

        if select_stage != 'play':
            if select_stage == 'character':
                draw_character_select()
            elif select_stage == 'victory':
                draw_victory()
            else:
                draw_weapon_select()
            pygame.display.update()
            clock.tick(60)
            continue

        # ---- Draw / update the world ----
        sky.draw()
        world.draw()

        sprites.update()
        sprites.draw(screen)
        for sprite in sprites:
            if isinstance(sprite, GiantFrog):
                sprite.draw_effects()
            elif isinstance(sprite, Chicken):
                sprite.draw_health_bar()
        attack.update(sprites)

        controls = font.render('Movement: A/D or left/right arrows. Jump: W, Up, or Space.', True, 'black')
        attack_controls = font.render('Attack: X, S, DOWN.', True, 'black')
        if LEVEL == lvl.level1:
            screen.blit(attack_controls, (0, 45))
            screen.blit(controls, (0, 20))

        # ---- Quests ----
        if LEVEL == lvl.level1:
            num = 0
            total = 1
            quest = font.render(f'Jump over the obstacles and reach the door:{num}/{total}', True, 'black')
            screen.blit(quest, (0, 70))
            if player.hb.colliderect(door.rect):
                num += 1
        if LEVEL == lvl.level2:
            total = len(world.slime)
            quest = font.render(f'Quest: Kill slime: {num}/{total}', True, 'black')
            screen.blit(quest, (0, 20))
        if LEVEL == lvl.level3:
            total = len(world.chicken)
            quest = font.render(f'Quest: Kill chicken: {num}/{total}', True, 'black')
            screen.blit(quest, (0, 20))
        if LEVEL == lvl.level4:
            total = len(world.slime) + len(world.chicken)
            quest = font.render(f'Quest: Kill enemies: {num}/{total}', True, 'black')
            screen.blit(quest, (0, 20))

        # ---- Door / level progression ----
        at_door = door.rect.colliderect(player.hb)
        boss_dead = LEVEL == lvl.level5 and not any(isinstance(s, GiantFrog) for s in sprites)
        ready_at_door = LEVEL in (lvl.level1, lvl.level2, lvl.level3) and at_door and num >= total
        ready_boss = LEVEL == lvl.level5 and at_door and boss_dead
        ready_after_kills = LEVEL == lvl.level4 and num >= 3 and at_door
        if ready_at_door or ready_after_kills or ready_boss:
            continue_text = font.render('Press P.', True, 'black')
            c_font = continue_text.get_rect()
            screen.blit(continue_text, (door.rect.centerx - 80, door.rect.top - 20))

        if advance_pressed and at_door and LEVEL == lvl.level5 and boss_dead:
            select_stage = 'victory'
        elif advance_pressed and at_door and LEVEL == lvl.level4 and num >= 3:
            LEVEL = lvl.level5
            lvl_rst()
        elif advance_pressed and at_door and LEVEL == lvl.level1 and num >= total:
            LEVEL = lvl.level2
            lvl_rst()
        elif advance_pressed and at_door and LEVEL == lvl.level2 and num >= total:
            LEVEL = lvl.level3
            lvl_rst()
        elif advance_pressed and at_door and LEVEL == lvl.level3 and num >= total:
            LEVEL = lvl.level4
            lvl_rst()

        # ---- Game over ----
        keys = pygame.key.get_pressed()
        if (player.h1 == player.empty and player.h2 == player.empty and player.h3 == player.empty) \
                or player.hb.top > height:
            screen.fill('red')
            screen.blit(player.deadl1, player.deadl1.get_rect(center=(width // 2, 220)))
            screen.blit(player.deadl2, player.deadl2.get_rect(center=(width // 2, 290)))
            if keys[pygame.K_r] and LEVEL == LEVEL:
                LEVEL = LEVEL
                lvl_rst()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


asyncio.run(main())