import pygame

import constants


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type, animation_list, fake_coin=False):
        pygame.sprite.Sprite.__init__(self)
        self.type = type # 0: coin, 1: potion
        self.frame_index = 0
        self.animation_list = animation_list
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_animation_update = pygame.time.get_ticks()
        self.fake = fake_coin

    def update(self, player, scroll, sounds):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.last_animation_update > constants.ANIMATION_COOLDOWN_PERIOD:
            self.frame_index += 1
            self.last_animation_update = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

        if player.rect.colliderect(self.rect):
            if self.type == 0: # coin
                player.score += 1
                sounds[self.type].play()
            elif self.type == 1: # red potion
                player.health += 5
                sounds[self.type].play()
                if player.health > constants.PLAYER_INIT_HEALTH:
                    player.health = constants.PLAYER_INIT_HEALTH

            self.kill()

        # add scroll update
        # it affect only real coins
        if not self.fake:
            self.rect.centerx += scroll[0]
            self.rect.centery += scroll[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)