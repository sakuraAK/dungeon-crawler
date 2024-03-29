import math

import pygame
import constants


class Character:

    def __init__(self, x, y, health, animation_list, character_index):
        self.animation_list = animation_list
        self.frame_index = 0
        self.last_animation_update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.moving = False
        self.image = self.animation_list[character_index][1 if self.moving else 0][self.frame_index]
        self.flip = False
        self.character_index = character_index
        self.health = health
        self.alive = True
        self.score = 0



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

        # camera scroll logic
        scroll =[0, 0]
        # move screen right
        if self.rect.right >= constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD:
            scroll[0] = -(self.rect.right - (constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD))
            self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
        # move screen left
        if self.rect.left <= constants.SCROLL_THRESHOLD:
            scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
            self.rect.left = constants.SCROLL_THRESHOLD

        # move screen up
        if self.rect.top <= constants.SCROLL_THRESHOLD:
                scroll[1] = constants.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = constants.SCROLL_THRESHOLD
        # move screen down
        if self.rect.bottom >= constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD:
                scroll[1] = -(self.rect.bottom - (constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD))
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
        return scroll

    def ai(self, scroll):
        self.rect.centerx += scroll[0]
        self.rect.centery += scroll[1]

    def update(self):
        animation_cooldown = constants.ANIMATION_COOLDOWN_PERIOD

        # handle animation
        # update image
        self.image = self.animation_list[self.character_index][1 if self.moving else 0][self.frame_index]
        if pygame.time.get_ticks() - self.last_animation_update_time > animation_cooldown:
            self.frame_index += 1
            self.last_animation_update_time = pygame.time.get_ticks()
            # self.frame_index  = self.frame_index % len(self.animation_list)
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)