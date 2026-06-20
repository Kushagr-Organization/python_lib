import pygame
from sprites import *  # You should have Player, Block, etc. here
from config import *   # This should include WIN_WIDTH, WIN_HEIGHT, FPS, etc.
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH1,WIN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def createTilemap(self):
            for i, row in enumerate(tilemap):
                for j, column in enumerate(row):
                    if column == "B":
                        Block(self, j, i)
                    if column =="P":
                        Player(self, j, i)


    def new(self):
        self.createTilemap()
        # Start a new game
        self.playing = True

        # Sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()


        # Create the player
        self.player = Player(self, 1, 2)  # You must define Player in sprites.py
        self.all_sprites.add(self.player)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        # Optional: add Game Over screen
        pass

    def intro_screen(self):
        # Optional: add intro/menu screen
        pass

# Run the game
g = Game()
g.intro_screen()
while g.running:
    g.new()
    g.main()
    g.game_over()

pygame.quit()
sys.exit()



















