import pygame, sys, random, time
from pygame.locals import *

# Initializing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

# Other Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Modified Coin class to support random weights and size scaling based on weight
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly assign a weight value to the coin
        self.weight = random.choice([1, 2, 5])
        self.original_image = pygame.image.load("Coin.png")
        # Scale coin size based on its weight (heavier coins appear larger)
        scale = 20 + self.weight * 5
        self.image = pygame.transform.scale(self.original_image, (scale, scale))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        # When the coin goes off-screen, reset its position
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# New user event for spawning additional coins
COIN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_EVENT, 1500)  # Spawn a coin every 1.5 seconds if needed

# New variables for increasing enemy speed when N coins are collected
COINS_FOR_SPEED_UP = 10      # Increase speed every 10 coins collected
last_coin_speed_milestone = 0

# Adding a new User event for speed increment over time (kept from original code)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Function to spawn a new coin if the number of coins on screen is less than a limit
def spawn_coin():
    if len(coins) < 3:  # Limit the number of coins on the screen
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5      
        if event.type == COIN_EVENT:
            spawn_coin()  # Spawn new coin periodically
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    coins_display = font_small.render(str(COINS_COLLECTED), True, ORANGE)
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 30, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    # Check collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Check collision between player and coins; remove collided coins
    collided_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collided_coins:
        # Increase coins collected based on the coin's weight
        COINS_COLLECTED += coin.weight

    # Increase enemy speed when player collects every N coins
    if COINS_COLLECTED // COINS_FOR_SPEED_UP > last_coin_speed_milestone:
        SPEED += 1  # Increase speed increment
        last_coin_speed_milestone = COINS_COLLECTED // COINS_FOR_SPEED_UP

    pygame.display.update()
    FramePerSec.tick(FPS)
