import sys, pygame, random

pygame.init()

'----- Constants -----'
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

# Load image of midline, create a rect of it and place it at the center of the screen
midline_image = pygame.image.load('assets/midline.png').convert_alpha()
midline_rect = midline_image.get_rect()
midline_rect.x, midline_rect.y = 295, 0

# Collision settings
bounce_factor = 5 # Decides how much the balls trajectory will be influenced by the collision point on the paddle

'----- Classes -----'
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, y_v, s, ct):
        super().__init__()
        self.image = pygame.image.load('assets/paddle.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.y_v = y_v # Set starting velocity of paddle (0)
        self.speed = s # Set movement speed of paddle
        self.control_type = ct # Set control type of the paddle (Player/Computer)

    def move(self, move_up, move_down): # Movement function for player
        self.y_v = 0 # Reset y-velocity before we set it again
        if move_up and self.rect.top > 0: # Check input and position
            self.y_v = -self.speed # Set y-velocity
        elif move_down and self.rect.bottom < height: # Check input and position
            self.y_v = self.speed # Set y-velocity
        self.rect.y += self.y_v # Change position based on velocity

    def auto_move(self): # Movement function for computer
        self.y_v = 0 # Reset y-velocity before we set it again
        if ball.rect.centery < self.rect.centery and self.rect.top > 0: # Check y-position relative to ball and clamp
            self.y_v = -self.speed # Set y-velocity in direction of ball
        elif ball.rect.centery > self.rect.centery and self.rect.bottom < height: 
            self.y_v = self.speed
        self.rect.y += self.y_v # Change position based on velocity

    def update(self):
        '''
        I could check if computer, then do else, get input, then if player or player 2.
        This way I only have to check the input once for 2-player.

        Input should be flipped for player and player2 WS / UpDown
        '''
        if self.control_type == 'Player': # Check control type
            keys = pygame.key.get_pressed() # Get input
            self.move(keys[pygame.K_w], keys[pygame.K_s]) # Run the movement function based on the input
        elif self.control_type == 'Player2':
            keys = pygame.key.get_pressed()
            self.move(keys[pygame.K_UP], keys[pygame.K_DOWN])
        elif self.control_type == 'Computer': # If control type is computer
            self.auto_move() # Run auto move function


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        super().__init__()
        self.image = pygame.image.load('assets/ball.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = s

        self.y_v = random.choice([-1, 1]) * self.speed # Set random starting orientation for ball + or - in either direction
        self.x_v = random.choice([-1, 1]) * self.speed

    def update(self):
        # Move according to velocity
        self.rect.x += self.x_v
        self.rect.y += self.y_v

        # Check y-position to reverse movement on edges, bounce
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.y_v = -self.y_v
        
        # Reset to middle with random direction if ball goes beyond paddle
        if self.rect.right < 0 or self.rect.left > width:
            self.rect.center = (width//2, height//2)
            self.y_v = random.choice([-1, 1] * self.speed)
            self.y_v = random.choice([-1, 1] * self.speed)


'----- Functions -----'


'----- Groups -----'
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()
paddle_sprites = pygame.sprite.Group()

'----- Instances -----'
player = Paddle(20, 160, 0, 4, 'Player')
all_sprites.add(player)
player_sprites.add(player)
paddle_sprites.add(player)

enemy = Paddle(560, 160, 0, 4, 'Player2')
all_sprites.add(enemy)
enemy_sprites.add(enemy)
paddle_sprites.add(enemy)

ball = Ball(width//2, height//2, 5)
all_sprites.add(ball)
ball_sprites.add(ball)

'----- Game Loop -----'
running = True
while running:
    
    '----- Event -----'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    '----- Update -----'
    all_sprites.update()

    for paddle in paddle_sprites:
        if ball.rect.colliderect(paddle.rect): # Check for collision between ball and paddle
            ball.x_v = -ball.x_v # Reverse x-direction

            collision_point = (ball.rect.centery - paddle.rect.centery) / (paddle.rect.height/2) # Find out where ball hit relative to paddles center
            ball.y_v = collision_point * bounce_factor # Change trajectory of ball based on collision point on paddle and a bounce factor

            ball.y_v += paddle.y_v * 0.5 # Add to the balls velocity when the paddle hits while moving

    '----- Draw -----'
    screen.fill('#000000') # Reset background
    screen.blit(midline_image, midline_rect) # Add midline to the center
    all_sprites.draw(screen) # Draw all sprites to the screen

    pygame.display.flip() # Update screen
    clock.tick(fps) # Control frame rate

pygame.quit() # Uninitialize Pygame
sys.exit() # Stop program