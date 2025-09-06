'''
Other things to think about:
    - Game states, separate loops for each state
    - Asset management
    - UI / HUD
    - Animation with Animation Manager or frame counter
    - Music and sound
    - Saving stats in JSON
    - Level management
'''
import sys, pygame # Import modules

pygame.init() # Initialize Pygame

'----- Constants -----'
width, height = 500, 500 # Variables for screen size
screen = pygame.display.set_mode((width, height)) # Create game window

clock = pygame.time.Clock() # Create game clock
fps = 60 # Variable for refresh rate

'----- Classes -----'

'----- Instances -----'

'----- Game Loop -----'
running = True # Variable for game state
while running:
    '----- Event -----'
    for event in pygame.event.get(): # Check all inputs
        if event.type == pygame.QUIT: # Check if input tells us to quit
            running = False # End the loop

    '----- Update -----'

    '----- Draw -----'

    pygame.display.flip() # Update what is shown to the player, double buffering
    clock.tick(fps) # Control refresh rate

pygame.quit() # If we leave the game loop, shut down Pygame
sys.exit() # End the program