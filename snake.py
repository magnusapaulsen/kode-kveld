import sys, pygame, random

pygame.init()

'----- Constants -----'
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
cell = 25

clock = pygame.time.Clock()
fps = 60

'----- Classes -----'
class Snake():
    def __init__(self):
        self.body = [(10 * cell, 10 * cell), (9 * cell, 10 * cell), (8 * cell, 10 * cell)]
        self.direction = 'Right'
        self.growing = False
        self.image = pygame.image.load('assets/snake/snake.png').convert_alpha()

    def move(self):
        x, y = self.body[0]

        if self.direction == 'Up':
            y -= cell
        elif self.direction == 'Down':
            y += cell
        elif self.direction == 'Left':
            x -= cell
        elif self.direction == 'Right':
            x += cell

        new_head = (x, y)
        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True
        
    def draw(self, screen):
        for segment in self.body:
            screen.blit(self.image, segment)

    def check_collision(self):
        head = self.body[0]

        #Wall collisions
        if head[0] <= 0 or head[0 >= width] or head[1] <= 0 or head[1] >= height:
            return True
        
        #Self collision
        if head in self.body[1:]:
            return True
        return False
    
class Food:
    def __init__(self):
        self.image = pygame.image.load('assets/snake/apple.png').convert_alpha()
        self.position = self.random_position()

    def random_position(self):
        return (random.randrange(0, width // cell) * cell, random.randrange(0, height // cell) * cell)
    
    def respawn(self):
        self.position = self.random_position()
    
    def draw(self, screen):
        screen.blit(self.image, self.position)
