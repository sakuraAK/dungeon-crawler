import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")



# game loop
run = True
while run:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
