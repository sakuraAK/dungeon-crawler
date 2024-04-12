import math

import pygame
import constants
from weapon import Fireball


class Character:

    def __init__(self, x, y, health, animation_list, character_index):
        self.animation_list = animation_list
        self.frame_index = 0
        self.last_animation_update_time = pygame.time.get_ticks()
        self.boss = False

        size_x = 40
        size_y = 40
        if character_index == 2:
            self.boss = True
            size_x = 60
            size_y = 70

        self.rect = pygame.Rect(0, 0, size_x, size_y)
        self.rect.center = (x, y + 15)
        self.moving = False
        self.image = self.animation_list[character_index][1 if self.moving else 0][self.frame_index]
        self.flip = False
        self.character_index = character_index
        self.health = health
        self.score = 0
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.stunned = False

    def move(self, dx, dy, obstacle_tiles, exit_tile):
        screen_scroll = [0, 0]
        exit_reached = False
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # check for collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        # check for collision with map in y direction
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        # logic only applicable to player
        if self.character_index == 0:
            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH

            # move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH

            # if exit_reached
            if self.rect.colliderect(exit_tile[1]):
                exit_reached = True

        return screen_scroll, exit_reached

    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image):
        clipped_line = ()
        stun_cooldown = 200
        ai_dx = 0
        ai_dy = 0
        fireball = None

        # reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        # check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        # check distance to player
        dist = math.sqrt(
            ((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))
        if not clipped_line and dist > constants.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:
                # move towards player
                self.move(ai_dx, ai_dy, obstacle_tiles, None)
                # attack player
                if dist < constants.ATTACK_RANGE and player.hit is False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()

                # boss attacks with fireball
                fireball_cooldown = 800
                if self.boss and dist < constants.FIREBALL_RANGE \
                        and pygame.time.get_ticks() - self.last_shot >= fireball_cooldown:
                    self.last_shot = pygame.time.get_ticks()
                    fireball = Fireball(fireball_image, self.rect.centerx, self.rect.centery, \
                                        player.rect.centerx, player.rect.centery)




            # check if hit
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False


            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False

            return fireball

    def update(self):
        animation_cooldown = constants.ANIMATION_COOLDOWN_PERIOD

        # handle animation
        # update image
        if self.alive:
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
        # pygame.draw.rect(surface, constants.RED, self.rect, 1)