import sys, pygame, random # Import modules

pygame.init() # Initialize Pygame

'----- Constants -----'
width, height = 400, 600 # Variables for screen size
screen = pygame.display.set_mode((width, height)) # Create game window

clock = pygame.time.Clock() # Create game clock
fps = 60 # Variable for refresh rate

spawn_timer = 0 # Variable that decides when to spawn a new enemy
enemy_spawn_cooldown = fps * 2 # Variable that decides the spawn rate
enemy_spawn_cooldown_min = fps // 2 # Variable that decides the minimum spawn rate

font = pygame.font.SysFont(None, 50) # Variable holding my font, it is just a basic font
score = 0 # Variable for my score

'----- Classes -----'
class Player(pygame.sprite.Sprite): # Create the player class with parent class Sprite
    def __init__(self, x, y, s): # Initialize the player with x-position, y-position and speed
        super().__init__() # Initialize the parent class Sprite
        self.image = pygame.image.load('assets/player.png').convert_alpha() # Create a surface holding the image of the player
        self.rect = self.image.get_rect() # Create a rectangle from the player's surface, to be used in collisions and logic
        self.rect.x, self.rect.y = x, y # Set position of the rectangle to the x-position and y-position we had as arguments
        self.speed = s # Set speed to the speed we had as an argument
    
    def update(self): # Player's update function
        keys = pygame.key.get_pressed() # Get the status of all keys on the keyboard

        if keys[pygame.K_UP] and self.rect.top > 0: # If up-arrow is pressed:
            self.rect.y -= self.speed # Rectangles y-position is reduced by the players speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self): # Function for shooting
        bullet = Bullet(self.rect.centerx - 10, self.rect.top - 10, 7) # Initialize bullet at the center-top of the player with a speed of 7
        bullet_group.add(bullet) # Add the bullet to the bullet-sprite group
        all_group.add(bullet) # Add the bullet to the all-sprite group
        

class Enemy(pygame.sprite.Sprite): # Create the enemy class with parent class Sprite
    def __init__(self, x, y, s): # Initialize the enemy with x-position, y-position and speed
        super().__init__() # Initialize the parent class Sprite
        self.image = pygame.image.load('assets/enemy.png').convert_alpha() # Create surface for holding the image of the enemy
        self.rect = self.image.get_rect() # Create a rectangle from the enemy's surface, to be used in collisions and logic
        self.rect.x, self.rect.y = x, y # Set position of the rectangle to the x-position and y-position we had as arguments
        self.speed = s # Set speed to the speed we had as an argument

    def update(self): # Enemy's update function
        self.rect.y += self.speed # Change enemy's y-position by +speed each frame (moving downward)
        if self.rect.top > height: # If the top of the enemy is below the screen:
            self.kill() # Remove the enemy

class Bullet(pygame.sprite.Sprite): # Create the bullet class with parent class Sprite
    def __init__(self, x, y, s): # Initialize the bullet with x-position, y-position and speed
        super().__init__() # Initialize the parent class Sprite
        self.image = pygame.image.load('assets/bullet.png').convert_alpha() # Create the surface for holding the image of the bullet
        self.rect = self.image.get_rect() # Create a rectangle from the bullet's surface, to be used in collisions and logic
        self.rect.x, self.rect.y = x, y # Set position of the rectangle to the x-position and y-position we had as arguments
        self.speed = s # Set speed to the speed we had as arguments

    def update(self): # Bullet's update function
        self.rect.y -= self.speed # Change bullet's y- position by -speed each fram (moving upward)
        if self.rect.bottom < 0: # If the bottom of the bullet is above the screen:
            self.kill() # Remove the bullet

'----- Functions -----'
def spawn_enemy(): # Function for spawning enemies
    enemy = Enemy(random.randint(0, width - (width // 10)), - (height // 10), 3) # Create an instance of the enemy class
    all_group.add(enemy) # Add the instance of the enemy to the all-sprite group
    enemy_group.add(enemy) # Add the instance of the enemy to the enemy-sprite group

'----- Instances -----'
player = Player(180, 470, 5) # Create an instance of the player class

'----- Groups -----'
all_group = pygame.sprite.Group() # Create the all-sprite group
player_group = pygame.sprite.Group() # Create the player-sprite group
enemy_group = pygame.sprite.Group() # Create the enemy-sprite group
bullet_group = pygame.sprite.Group() # Create the bullet-sprite group

all_group.add(player) # Add the player to the all-sprite group
player_group.add(player) # Add the player to the player-sprite group

'----- Game Loop -----'
running = True # Variable for game state
while running:

    '----- Event -----'
    for event in pygame.event.get(): # Check all inputs
        if event.type == pygame.QUIT: # Check if input tells us to quit
            running = False # End the loop

        if event.type == pygame.KEYDOWN: # If key is pressed:
            if event.key == pygame.K_SPACE: # If the key is the spacebar
                player.shoot() # Call the player's shoot-function

    '----- Update -----'
    spawn_timer += 1 # Each frame add 1 to the spawn timer
    if spawn_timer >= enemy_spawn_cooldown: # Check if we should spawn a new enemy
        spawn_enemy() # Call the spawn enemy_function
        spawn_timer = 0 # Reset the spawn timer to 0
        if enemy_spawn_cooldown > enemy_spawn_cooldown_min: # If the spawn timer cooldown is still within the accepted range:
            enemy_spawn_cooldown -= 1 # Reduce it by 1 (Enemies will spawn faster the longer we play)

    all_group.update() # Call the update function of all classes

    '----- Collisions -----'
    bullet_enemy_hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True) # Check if a bullet has hit an enemy, if yes, remove both the bullet and the enemy
    enemy_player_hits = pygame.sprite.groupcollide(enemy_group, player_group, True, True) # Check if an enemy has hit the player, if yes, remove both the enemy and the player
    
    if bullet_enemy_hits: # If a bullet hits an enemy
        score += 1 # Add 1 to the score

    if enemy_player_hits: # If the player hits an enemy:
        running = False # End the loop

    '----- Draw -----'
    screen.fill('#000000') # Fill the screen with black
    all_group.draw(screen) # Draw all the sprites on the screen

    screen.blit(font.render(str(score), True, ('#ffffff')), (200, 100)) # Put the score on the screen

    pygame.display.flip() # Update what is shown to the player, double buffering
    clock.tick(fps) # Control refresh rate

pygame.quit() # If we leave the game loop, shut down Pygame
sys.exit() # End the program