import sys, pygame, random

pygame.init()

'----- Constants -----'
width, height = 400, 600
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

'----- Classes -----'
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

pygame.quit()
sys.exit()