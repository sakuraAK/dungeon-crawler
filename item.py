import pygame

import constants


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.type = type # 0: coin, 1: potion
        self.frame_index = 0
        self.animation_list = animation_list
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_animation_update = pygame.time.get_ticks()

    def update(self, player):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.last_animation_update > constants.ANIMATION_COOLDOWN_PERIOD:
            self.frame_index += 1
            self.last_animation_update = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

        if player.rect.colliderect(self.rect):
            if self.type == 0: # coin
                player.score += 1
            elif self.type == 1: # red potion
                player.health += 5
                if player.health > constants.PLAYER_INIT_HEALTH:
                    player.health = constants.PLAYER_INIT_HEALTH

            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)