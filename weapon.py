import math
import random

import pygame

from constants import ARROW_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Weapon:

    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.arrow_image = arrow_image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 500
        arrow = None
        self.rect.center = player.rect.center
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # negative because y increases when going down
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #shoot arrow
        #get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) > shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        # reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return arrow


    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2),
                                  self.rect.centery - int(self.image.get_height()/2)))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle)) * ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * ARROW_SPEED) # negative because in pygame y increases when going down



    def update(self, enemy_list):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # check if arrow is visible
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
            or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # check collision with enemies
        for enemy in enemy_list:
            if enemy.alive and enemy.rect.colliderect(self.rect):
                damage = 10 + random.randint(-5, 5)
                enemy.health -= damage
                self.kill()
                break

    def draw(self, surface):
        surface.blit(self.image, self.rect)