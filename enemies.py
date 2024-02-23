import pygame.time
import random
import constants

from character import Character

class Zombie(Character):
    def __init__(self, x, y, animation_list):
        super().__init__(x, y, animation_list, 1)
        self.internal_clock = pygame.time.get_ticks()
        self.internal_clock_1 = pygame.time.get_ticks()
        self.dx = 0
        self.dy = 0

    def move(self):
        # self.dx = random.randint(0, 2) * constants.SPEED * 0.5
        # self.dy = random.randint(0, 2) * constants.SPEED * 0.5
        change_direction_after = 400
        if pygame.time.get_ticks() - self.internal_clock > change_direction_after:
            self.dx = - self.dx
            self.dy = - self.dy
            self.internal_clock = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.internal_clock_1 > change_direction_after * 4:
            self.dy = random.randint(0, 1) * constants.SPEED * 0.5
            self.dx = random.randint(0, 1) * constants.SPEED * 0.5
            self.internal_clock_1 = pygame.time.get_ticks()

        super().move(self.dx, self.dy)

