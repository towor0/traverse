import pygame
import time
from controller import Controller
import os

# initiate pygame
pygame.init()
# clock and previous time for delta time calculation
clock = pygame.time.Clock()
prev_time = time.time()

# define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# create pygame window and instance initiation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
controller = Controller()
running = True

# mouse setup
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

# sound setup
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("assets", "cave_ambience.wav"))

# game loop
while running:
    # 60 frames cap
    clock.tick(60)
    # allows for frame independence
    now = time.time()
    dt = (now - prev_time) * 60
    prev_time = now
    # check if the player wants to quit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # update all instances
    controller.update(dt, events)
    # draw all instances
    window.fill((0, 0, 0))
    controller.draw(window)
    screen.blit(window, (0, 0))
    pygame.display.flip()
# quit pygame
pygame.quit()
