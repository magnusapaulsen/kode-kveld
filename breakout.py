import sys, pygame, random

pygame.init()

'----- Constants -----'
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

bounce_factor = 3 # Decides how much the balls trajectory will be influenced by the collision point on the paddle

'----- Classes -----'
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        super().__init__()
        self.image = pygame.Surface((100, 10)) # Create a surface for the paddle
        self.image.fill('#ffffff') # Color in the surface
        self.rect = self.image.get_rect() # Create a rectangle of the surface
        self.rect.center = (x, y) # Set starting position of the paddle
        self.speed = s # Set speed of the paddle

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r, s):
        super().__init__()
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA) # Create a transparent surface for the ball
        pygame.draw.circle(self.image, '#0000ff', (r, r), r) # Draw a circle on the surface
        self.rect = self.image.get_rect() # Create a rectangle around the surface
        self.rect.center = (x, y) # Set starting position of the ball
        self.speed = s # Set speed of the ball
        
        self.x_v = random.choice([-1, 1] * self.speed) # Set starting x-velocity of the ball
        self.y_v = self.speed # Set starting y-velocity of the ball

    def update(self):
        old = ball.rect.copy() # Store rectangle of the previous position
        self.rect.x += self.x_v # Move the rectangle of the ball
        self.rect.y += self.y_v 

        # Clamp, bounce and reset
        if self.rect.left < 0:
            self.rect.left = 0
            self.x_v = -self.x_v
        if self.rect.right > width:
            self.rect.right = width
            self.x_v = -self.x_v
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_v = -self.y_v
        if self.rect.top > height:
            self.rect.center = (width // 2, height // 2)
            self.x_v = random.choice([-1, 1]) * self.speed
            self.y_v = self.speed

        # Check for collisions
        hits = pygame.sprite.spritecollide(self, block_sprites, True)
        for block in hits:
            # Check where on the block the ball hit
            # If it hit the top or bottom
            if (old.bottom <= block.rect.top and self.rect.bottom > block.rect.top) or (old.top >= block.rect.bottom and self.rect.top < block.rect.bottom):
                self.y_v = -self.y_v
            # If it hit the sides
            elif (old.right <= block.rect.left and self.rect.right > block.rect.left) or (old.left >= block.rect.right and self.rect.left < block.rect.right):
                self.x_v = -self.x_v

        # Collision and bounce of paddle
        if pygame.sprite.groupcollide(paddle_sprites, ball_sprites, False, False):
            self.y_v = -self.y_v

            # Adjust bounce based on collision point
            collision_point = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            ball.x_v = collision_point * bounce_factor

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill('#ff0000')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

'----- Groups -----'
all_sprites = pygame.sprite.Group()
paddle_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()

'----- Instances -----'
paddle = Paddle(width // 2, height - 20, 5)
all_sprites.add(paddle)
paddle_sprites.add(paddle)

ball = Ball(width // 2, height // 2, 10, 3)
all_sprites.add(ball)
ball_sprites.add(ball)

# Loop for creating all the blocks
for y in range(50, 150, 30):
    for x in range(60, 560, 60):
        block = Block(x, y)
        all_sprites.add(block)
        block_sprites.add(block)
'----- Game Loop -----'
running = True
while running:
    '----- Event -----'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    '----- Update -----'
    paddle.update(pygame.key.get_pressed())
    ball.update()

    '----- Draw -----'
    screen.fill('#000000')
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()