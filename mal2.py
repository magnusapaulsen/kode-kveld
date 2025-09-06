import sys, pygame, random # Import modules

pygame.init() # Initialize Pygame

'----- Constants -----'
width, height = 400, 600 # Variables for screen size
screen = pygame.display.set_mode((width, height)) # Create game window

clock = pygame.time.Clock() # Create game clock
fps = 60 # Variable for refresh rate

spawn_timer = 0
enemy_spawn_cooldown = fps * 2
enemy_spawn_cooldown_min = fps // 2 

bullet_size = 20

font = pygame.font.SysFont(None, 50)
score = 0

'----- Classes -----'
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        super().__init__()
        #self.image = pygame.Surface((w, h))
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = s
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx - 10, self.rect.top - 10, 7)
        bullet_group.add(bullet)
        all_group.add(bullet)
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        super().__init__()
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = s

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        super().__init__()
        self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = s

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

'----- Functions -----'
def spawn_enemy():
    enemy = Enemy(random.randint(0, width - (width // 10)), - (height // 10), 3)
    all_group.add(enemy)
    enemy_group.add(enemy)

'----- Instances -----'
player = Player(180, 470, 5)

'----- Groups -----'
all_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

all_group.add(player)
player_group.add(player)

'----- Game Loop -----'
running = True # Variable for game state
while running:

    '----- Event -----'
    for event in pygame.event.get(): # Check all inputs
        if event.type == pygame.QUIT: # Check if input tells us to quit
            running = False # End the loop

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    '----- Update -----'
    spawn_timer +=1
    if spawn_timer >= enemy_spawn_cooldown:
        spawn_enemy()
        spawn_timer = 0
        if enemy_spawn_cooldown > enemy_spawn_cooldown_min:
            enemy_spawn_cooldown -= 1
            print(enemy_spawn_cooldown)

    all_group.update()

    '----- Collisions -----'
    bullet_enemy_hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
    enemy_player_hits = pygame.sprite.groupcollide(enemy_group, player_group, True, True)
    
    if bullet_enemy_hits:
        score += 1

    if enemy_player_hits:
        running = False

    '----- Draw -----'
    screen.fill('#000000')
    all_group.draw(screen)

    screen.blit(font.render(str(score), True, ('#ffffff')), (200, 100))

    pygame.display.flip() # Update what is shown to the player, double buffering
    clock.tick(fps) # Control refresh rate

pygame.quit() # If we leave the game loop, shut down Pygame
sys.exit() # End the program