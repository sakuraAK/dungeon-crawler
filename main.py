import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS
from character import  Character

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()

# player movement variables
move_left = False
move_right = False
move_up = False
move_down = False

# create player

player = Character(100, 100)

# game loop
run = True
while run:
    # control game speed
    clock.tick(FPS)

    # clearing the screen
    screen.fill(BG)

    # calculate player movements
    dx = 0
    dy = 0
    if move_right:
        dx = 5
    if move_left:
        dx = -5
    if move_up:
        dy = -5
    if move_down:
        dy = 5

    # move player
    player.move(dx, dy)

    # draw player
    player.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # handle keyboard events
        # handle button pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True
        # handle button release event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False

    # render the display
    pygame.display.update()

pygame.quit()
