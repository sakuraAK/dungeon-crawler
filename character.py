import math

import pygame
import constants


class Character:

    def __init__(self, x, y, animation_list, character_index):
        self.animation_list = animation_list
        self.frame_index = 0
        self.last_animation_update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.moving = False
        self.image = self.animation_list[character_index][1 if self.moving else 0][self.frame_index]
        self.flip = False
        self.character_index = character_index



    def move(self, dx, dy):
        # determine if moving
        if dx != 0 or dy != 0:
            self.moving = True
        else:
            self.moving = False

        if dx < 0:
            # left
            self.flip = False
        if dx > 0:
            # right
            self.flip = True
        if dx != 0 and dy != 0: # moving diagonally
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy
    def update(self):
        animation_cooldown = 200

        # handle animation
        # update image
        self.image = self.animation_list[self.character_index][1 if self.moving else 0][self.frame_index]
        if pygame.time.get_ticks() - self.last_animation_update_time > animation_cooldown:
            self.frame_index += 1
            self.last_animation_update_time = pygame.time.get_ticks()
            # self.frame_index  = self.frame_index % len(self.animation_list)
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0


    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)